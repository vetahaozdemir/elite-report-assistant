"""
PDF'lerden akıllı soru çıkarma sistemi
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import os
import json
from datetime import datetime
from .pdf_processor import PDFProcessor

class SmartQuestionGenerator:
    """PDF raporlarından otomatik soru oluşturan AI sistemi"""
    
    def __init__(self, api_key: str = None):
        """
        SmartQuestionGenerator initialization
        
        Args:
            api_key (str): Gemini API anahtarı
        """
        if api_key:
            genai.configure(api_key=api_key)
        elif os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        else:
            raise ValueError("GEMINI_API_KEY gerekli")
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.pdf_processor = PDFProcessor()
    
    def analyze_pdf_structure(self, pdf_path: str) -> Dict:
        """
        PDF'in yapısını analiz et ve soru çıkarma için hazırla
        
        Args:
            pdf_path (str): PDF dosya yolu
            
        Returns:
            Dict: Analiz sonucu
        """
        try:
            # PDF'den metin çıkar
            processed_data = self.pdf_processor.process_pdf_file(pdf_path)
            full_text = processed_data['full_text']
            
            if len(full_text) < 500:
                return {
                    "success": False,
                    "message": "PDF çok kısa, analiz için yetersiz metin"
                }
            
            # AI ile yapısal analiz
            analysis_prompt = f"""
Aşağıdaki sosyal hizmet raporunu analiz et ve yapısını çıkar:

RAPOR METNİ:
{full_text[:3000]}...

Bu raporda hangi konular ele alınmış? Aşağıdaki kategorilere göre analiz et:

1. DEMOGRAFİK BİLGİLER: Yaş, cinsiyet, medeni durum, aile yapısı
2. SOSYOEKONOMIK DURUM: Gelir, meslek, barınma, ekonomik zorluklar
3. SAĞLIK DURUMU: Fiziksel ve mental sağlık, tedavi geçmişi
4. EĞİTİM DURUMU: Eğitim seviyesi, mesleki beceriler
5. SOSYAL ÇEVRE: Aile ilişkileri, sosyal destek ağı, toplumsal bağlar
6. MEVCUT PROBLEMLER: Yaşanan zorluklar, krizler, acil ihtiyaçlar
7. GÜÇLÜ YANLAR: Kişisel kaynaklar, yetenekler, başarılar
8. MÜDAHAlE GEÇMİŞİ: Önceki hizmetler, tedaviler, destekler
9. HEDEFLER VE PLANLAR: Kısa/uzun vadeli hedefler, eylem planları
10. RİSK DEĞERLENDİRMESİ: Güvenlik, koruma ihtiyaçları

JSON formatında yanıt ver:
{{
  "detected_categories": ["kategori1", "kategori2", ...],
  "report_type_suggestion": "önerilen rapor türü adı",
  "complexity_level": "basit/orta/karmaşık",
  "key_themes": ["tema1", "tema2", ...],
  "target_population": "hedef grup tanımı"
}}
"""
            
            response = self.model.generate_content(analysis_prompt)
            
            if response.text:
                # JSON parse etmeye çalış
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    analysis_result = json.loads(json_match.group())
                    
                    return {
                        "success": True,
                        "analysis": analysis_result,
                        "full_text_length": len(full_text),
                        "metadata": processed_data['metadata']
                    }
            
            return {
                "success": False,
                "message": "Yapısal analiz başarısız"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Analiz hatası: {str(e)}"
            }
    
    def generate_questions_from_pdfs(self, pdf_paths: List[str], report_type_name: str = None) -> Dict:
        """
        Birden fazla PDF'den kapsamlı soru listesi oluştur
        
        Args:
            pdf_paths (List[str]): PDF dosya yolları listesi
            report_type_name (str): Rapor türü adı önerisi
            
        Returns:
            Dict: Oluşturulan sorular ve analiz
        """
        try:
            all_analyses = []
            combined_themes = set()
            combined_categories = set()
            
            # Her PDF'i analiz et
            for pdf_path in pdf_paths:
                analysis = self.analyze_pdf_structure(pdf_path)
                if analysis["success"]:
                    all_analyses.append(analysis)
                    
                    analysis_data = analysis["analysis"]
                    combined_themes.update(analysis_data.get("key_themes", []))
                    combined_categories.update(analysis_data.get("detected_categories", []))
            
            if not all_analyses:
                return {
                    "success": False,
                    "message": "Hiçbir PDF analiz edilemedi"
                }
            
            # Birleşik analiz sonucu
            combined_analysis = {
                "total_pdfs": len(all_analyses),
                "common_themes": list(combined_themes),
                "common_categories": list(combined_categories),
                "analyses": all_analyses
            }
            
            # AI ile soru oluştur
            questions_result = self._generate_smart_questions(combined_analysis, report_type_name)
            
            return {
                "success": True,
                "questions": questions_result["questions"],
                "report_type_suggestion": questions_result["report_type_suggestion"],
                "analysis_summary": combined_analysis,
                "question_rationale": questions_result["rationale"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Soru oluşturma hatası: {str(e)}"
            }
    
    def _generate_smart_questions(self, combined_analysis: Dict, report_type_name: str = None) -> Dict:
        """
        Birleşik analizden akıllı sorular oluştur
        """
        try:
            themes_str = ", ".join(combined_analysis["common_themes"])
            categories_str = ", ".join(combined_analysis["common_categories"])
            
            question_prompt = f"""
Sen bir sosyal hizmet uzmanı ve rapor tasarım uzmanısın. Aşağıdaki analiz sonuçlarına dayanarak profesyonel bir rapor türü için sorular oluştur:

ANALIZ SONUÇLARI:
- Analiz edilen PDF sayısı: {combined_analysis["total_pdfs"]}
- Ortak temalar: {themes_str}
- Ortak kategoriler: {categories_str}
{"- Önerilen rapor türü: " + report_type_name if report_type_name else ""}

SORU OLUŞTURMA PRİNSİPLERİ:
1. MANTIKLI SIRALAMA: Demografikten detaya doğru
2. AÇIK UÇLU SORULAR: Detaylı yanıt alacak şekilde
3. PROFESYONEL DİL: Sosyal hizmet terminolojisi
4. KAPSAMLI: Tüm önemli alanları kapsayacak
5. PRATİK: 7-12 soru arası, fazla yorucu olmayacak

SORU ÖRNEKLERİ:
- "Kişi/aile hakkında temel demografik bilgileri verebilir misiniz?"
- "Mevcut sosyoekonomik durum ve yaşam koşulları nasıl?"
- "Karşılaştığınız temel problemler ve zorluklar nelerdir?"

JSON formatında yanıt ver:
{{
  "report_type_suggestion": "önerilen rapor türü adı",
  "questions": [
    "soru1",
    "soru2",
    ...
  ],
  "rationale": {{
    "question_count": X,
    "focus_areas": ["alan1", "alan2"],
    "target_duration": "tahmini süre",
    "complexity": "basit/orta/karmaşık"
  }}
}}

ÖNEMLI: Sorular Türkçe, profesyonel ve sosyal hizmet pratiğine uygun olmalı.
"""
            
            response = self.model.generate_content(question_prompt)
            
            if response.text:
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            
            # Fallback: varsayılan soru seti
            return self._create_fallback_questions(combined_analysis)
            
        except Exception as e:
            print(f"Soru oluşturma hatası: {e}")
            return self._create_fallback_questions(combined_analysis)
    
    def _create_fallback_questions(self, analysis: Dict) -> Dict:
        """Hata durumunda varsayılan soru seti oluştur"""
        
        categories = analysis.get("common_categories", [])
        
        base_questions = [
            "Kişi/aile hakkında temel bilgileri verebilir misiniz?",
            "Mevcut yaşam koşulları ve sosyal çevre nasıl?",
            "Karşılaştığınız temel problemler nelerdir?",
            "Hangi konularda desteğe ihtiyaç duyuyorsunuz?",
            "Daha önce hangi hizmetlerden yararlandınız?",
            "Kişisel güçlü yanlarınız ve kaynaklarınız nelerdir?",
            "Kısa vadeli hedefleriniz nelerdir?",
            "Bu süreçten beklentileriniz nelerdir?"
        ]
        
        # Kategorilere göre ek sorular
        additional_questions = {
            "SAĞLIK DURUMU": "Sağlık durumunuz ve tedavi geçmişiniz hakkında bilgi verebilir misiniz?",
            "EĞİTİM DURUMU": "Eğitim ve mesleki durumunuz nasıl?",
            "RİSK DEĞERLENDİRMESİ": "Güvenlik ve koruma ihtiyaçlarınız var mı?"
        }
        
        # Uygun ek soruları ekle
        final_questions = base_questions.copy()
        for category in categories:
            if category in additional_questions:
                final_questions.append(additional_questions[category])
        
        return {
            "report_type_suggestion": "Genel Sosyal Hizmet Değerlendirmesi",
            "questions": final_questions[:10],  # Max 10 soru
            "rationale": {
                "question_count": len(final_questions[:10]),
                "focus_areas": categories,
                "target_duration": "15-20 dakika",
                "complexity": "orta"
            }
        }
    
    def optimize_questions(self, existing_questions: List[str], pdf_paths: List[str]) -> Dict:
        """
        Mevcut soruları PDF'lere göre optimize et
        
        Args:
            existing_questions (List[str]): Mevcut sorular
            pdf_paths (List[str]): Referans PDF'ler
            
        Returns:
            Dict: Optimize edilmiş sorular
        """
        try:
            # PDF'leri analiz et
            analysis_result = self.generate_questions_from_pdfs(pdf_paths)
            
            if not analysis_result["success"]:
                return {
                    "success": False,
                    "message": "PDF analizi başarısız"
                }
            
            suggested_questions = analysis_result["questions"]
            
            # Mevcut ve önerilen soruları karşılaştır
            optimization_prompt = f"""
Mevcut sorular ile PDF analizinden çıkan öneriler arasında karşılaştırma yap ve optimize et:

MEVCUT SORULAR:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(existing_questions)])}

ÖNERİLEN SORULAR (PDF analizinden):
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(suggested_questions)])}

OPTIMIZASYON YAP:
1. En iyi soruları seç
2. Eksik alanları tamamla
3. Mükerrer soruları birleştir
4. Sıralamayi optimize et
5. 8-12 soru arasında tut

JSON formatında yanıt ver:
{{
  "optimized_questions": ["soru1", "soru2", ...],
  "changes_made": ["değişiklik1", "değişiklik2", ...],
  "improvement_reasons": ["neden1", "neden2", ...]
}}
"""
            
            response = self.model.generate_content(optimization_prompt)
            
            if response.text:
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return {
                        "success": True,
                        "optimized_questions": result["optimized_questions"],
                        "changes_made": result.get("changes_made", []),
                        "improvement_reasons": result.get("improvement_reasons", [])
                    }
            
            return {
                "success": False,
                "message": "Optimizasyon yanıtı parse edilemedi"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Optimizasyon hatası: {str(e)}"
            }