"""
Öğrenir rapor sistemi - Feedback loop ile sürekli gelişim
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import google.generativeai as genai

class LearningSystem:
    """AI'ın sürekli öğrenmesini sağlayan sistem"""
    
    def __init__(self, api_key: str = None):
        """
        LearningSystem initialization
        
        Args:
            api_key (str): Gemini API anahtarı
        """
        if api_key:
            genai.configure(api_key=api_key)
        elif os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Feedback veritabanı
        self.feedback_file = "./data/feedback_database.json"
        self.improvements_file = "./data/improvements_log.json"
        
        # Feedback veritabanını başlat
        self._init_feedback_db()
    
    def _init_feedback_db(self):
        """Feedback veritabanını başlat"""
        os.makedirs("./data", exist_ok=True)
        
        if not os.path.exists(self.feedback_file):
            initial_data = {
                "feedbacks": [],
                "report_versions": {},
                "improvement_metrics": {
                    "total_feedbacks": 0,
                    "positive_feedbacks": 0,
                    "improvement_rate": 0.0
                }
            }
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.improvements_file):
            with open(self.improvements_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def save_report_feedback(self, 
                           original_report: str, 
                           revised_report: str, 
                           feedback_type: str, 
                           user_comments: str,
                           report_type: str) -> Dict:
        """
        Kullanıcı geri bildirimini kaydet
        
        Args:
            original_report (str): Orijinal rapor
            revised_report (str): Revize edilmiş rapor
            feedback_type (str): "positive", "negative", "neutral"
            user_comments (str): Kullanıcı yorumları
            report_type (str): Rapor türü
            
        Returns:
            Dict: Kaydetme sonucu
        """
        try:
            # Mevcut verileri yükle
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Yeni feedback
            feedback = {
                "id": len(data["feedbacks"]) + 1,
                "timestamp": datetime.now().isoformat(),
                "report_type": report_type,
                "original_report": original_report,
                "revised_report": revised_report,
                "feedback_type": feedback_type,
                "user_comments": user_comments,
                "improvements_detected": self._analyze_improvements(original_report, revised_report)
            }
            
            # Feedback'i ekle
            data["feedbacks"].append(feedback)
            
            # Metrikleri güncelle
            data["improvement_metrics"]["total_feedbacks"] += 1
            if feedback_type == "positive":
                data["improvement_metrics"]["positive_feedbacks"] += 1
            
            data["improvement_metrics"]["improvement_rate"] = (
                data["improvement_metrics"]["positive_feedbacks"] / 
                data["improvement_metrics"]["total_feedbacks"]
            ) * 100
            
            # Kaydet
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Öğrenme analizi yap
            self._trigger_learning_analysis()
            
            return {
                "success": True,
                "feedback_id": feedback["id"],
                "message": "Geri bildirim kaydedildi ve sistem öğrendi!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Geri bildirim kaydedilemedi: {str(e)}"
            }
    
    def _analyze_improvements(self, original: str, revised: str) -> List[str]:
        """İyileştirmeleri analiz et"""
        try:
            prompt = f"""
Aşağıdaki iki raporu karşılaştır ve revize edilmiş raporda hangi iyileştirmeler yapıldığını listele:

ORİJİNAL RAPOR:
{original[:1000]}...

REVİZE EDİLMİŞ RAPOR:
{revised[:1000]}...

İyileştirme kategorilerini listele (maksimum 5 madde):
- Dil ve üslup iyileştirmeleri
- İçerik zenginleştirmeleri  
- Yapısal düzenlemeler
- Mesleki terminoloji kullanımı
- Diğer iyileştirmeler

Sadece iyileştirme kategorilerini liste halinde döndür.
"""
            
            response = self.model.generate_content(prompt)
            if response.text:
                # Response'u satırlara böl ve temizle
                improvements = [
                    line.strip().replace("- ", "").replace("* ", "")
                    for line in response.text.split("\n")
                    if line.strip() and not line.strip().startswith("#")
                ]
                return improvements[:5]  # Maksimum 5 iyileştirme
            
        except Exception as e:
            print(f"İyileştirme analizi hatası: {e}")
        
        return ["Manuel revizyon yapıldı"]
    
    def _trigger_learning_analysis(self):
        """Öğrenme analizini tetikle"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            recent_feedbacks = data["feedbacks"][-10:]  # Son 10 feedback
            
            if len(recent_feedbacks) >= 5:  # En az 5 feedback varsa analiz yap
                insights = self._generate_learning_insights(recent_feedbacks)
                self._save_learning_insights(insights)
                
        except Exception as e:
            print(f"Öğrenme analizi hatası: {e}")
    
    def _generate_learning_insights(self, feedbacks: List[Dict]) -> Dict:
        """Öğrenme içgörülerini oluştur"""
        try:
            # Feedback'lerden pattern'ları çıkar
            feedback_summary = ""
            for fb in feedbacks:
                feedback_summary += f"Rapor Türü: {fb['report_type']}\n"
                feedback_summary += f"Feedback: {fb['feedback_type']}\n"
                feedback_summary += f"İyileştirmeler: {', '.join(fb['improvements_detected'])}\n"
                feedback_summary += f"Yorumlar: {fb['user_comments']}\n\n"
            
            prompt = f"""
Aşağıdaki kullanıcı geri bildirimlerini analiz et ve gelecekteki raporları iyileştirmek için öneriler oluştur:

{feedback_summary}

Şu konularda analiz yap ve öneriler ver:
1. En sık rastlanan iyileştirme alanları
2. Rapor türüne göre önemli noktalar
3. Dil ve üslup konusunda gözlemler
4. Gelecekteki raporlar için somut öneriler

JSON formatında yanıt ver:
{{
  "common_improvements": ["liste"],
  "report_type_insights": {{"tür": "öneri"}},
  "language_observations": ["liste"],
  "future_recommendations": ["liste"]
}}
"""
            
            response = self.model.generate_content(prompt)
            if response.text:
                # JSON parse etmeye çalış
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            
        except Exception as e:
            print(f"İçgörü oluşturma hatası: {e}")
        
        return {
            "common_improvements": ["Genel iyileştirmeler yapıldı"],
            "report_type_insights": {},
            "language_observations": ["Dil ve üslup geliştirildi"],
            "future_recommendations": ["Sürekli geri bildirim alınmalı"]
        }
    
    def _save_learning_insights(self, insights: Dict):
        """Öğrenme içgörülerini kaydet"""
        try:
            with open(self.improvements_file, 'r', encoding='utf-8') as f:
                improvements = json.load(f)
            
            new_insight = {
                "timestamp": datetime.now().isoformat(),
                "insights": insights,
                "feedback_count": self.get_feedback_count()
            }
            
            improvements.append(new_insight)
            
            # Son 50 insight'ı tut
            if len(improvements) > 50:
                improvements = improvements[-50:]
            
            with open(self.improvements_file, 'w', encoding='utf-8') as f:
                json.dump(improvements, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"İçgörü kaydetme hatası: {e}")
    
    def get_learning_context(self, report_type: str) -> str:
        """Belirli rapor türü için öğrenilmiş bağlamı al"""
        try:
            if not os.path.exists(self.improvements_file):
                return ""
            
            with open(self.improvements_file, 'r', encoding='utf-8') as f:
                improvements = json.load(f)
            
            if not improvements:
                return ""
            
            # Son insight'ları al
            recent_insights = improvements[-3:]  # Son 3 öğrenme
            
            context = "SİSTEM ÖĞRENMELERİ (Geçmiş geri bildirimlerden):\n\n"
            
            for insight in recent_insights:
                insights_data = insight["insights"]
                
                # Genel iyileştirmeler
                if insights_data.get("common_improvements"):
                    context += "Sık İyileştirme Alanları:\n"
                    for improvement in insights_data["common_improvements"]:
                        context += f"- {improvement}\n"
                    context += "\n"
                
                # Rapor türü spesifik
                if report_type in insights_data.get("report_type_insights", {}):
                    context += f"{report_type.title()} Özel Önerileri:\n"
                    context += f"- {insights_data['report_type_insights'][report_type]}\n\n"
                
                # Dil gözlemleri
                if insights_data.get("language_observations"):
                    context += "Dil ve Üslup Önerileri:\n"
                    for obs in insights_data["language_observations"]:
                        context += f"- {obs}\n"
                    context += "\n"
            
            return context
            
        except Exception as e:
            print(f"Öğrenme bağlamı alma hatası: {e}")
            return ""
    
    def get_feedback_count(self) -> int:
        """Toplam feedback sayısını al"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return len(data["feedbacks"])
        except:
            return 0
    
    def get_statistics(self) -> Dict:
        """İstatistikleri al"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats = data["improvement_metrics"].copy()
            stats["latest_feedbacks"] = data["feedbacks"][-5:] if data["feedbacks"] else []
            
            return stats
            
        except Exception as e:
            return {
                "total_feedbacks": 0,
                "positive_feedbacks": 0,
                "improvement_rate": 0.0,
                "latest_feedbacks": []
            }