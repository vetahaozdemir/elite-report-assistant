"""
Sohbet tabanlı rapor oluşturma sistemi
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any
import os
import json
from datetime import datetime

class ReportChatbot:
    """Sohbet tabanlı rapor oluşturan chatbot"""
    
    def __init__(self, api_key: str = None):
        """
        ReportChatbot initialization
        
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
        
        # Rapor türleri ve soru şablonları
        self.report_types = {
            "sosyal_inceleme": {
                "name": "Sosyal İnceleme Raporu",
                "description": "Aile ve çevre koşullarının değerlendirildiği kapsamlı rapor",
                "questions": [
                    "Merhaba! Size Sosyal İnceleme Raporu konusunda yardımcı olacağım. Öncelikle kişi hakkında temel bilgileri alabilir miyim? (Ad, yaş, medeni durum, aile yapısı)",
                    "Ailenin sosyoekonomik durumu nasıl? (Gelir, meslek, ekonomik sıkıntılar var mı?)",
                    "Konut koşulları nasıl? (Ev tipi, temizlik, uygunluk, güvenlik)",
                    "Aile üyelerinin sağlık durumu hakkında bilgi verebilir misiniz?",
                    "Eğitim durumları nasıl? (Okul, kurs, mesleki gelişim)",
                    "Sosyal çevre ve komşuluk ilişkileri nasıl?",
                    "Şu anda yaşanan temel sorunlar nelerdir?",
                    "Daha önce herhangi bir sosyal hizmet desteği alındı mı?",
                    "Ailenin güçlü yanları ve yetenekleri nelerdir?",
                    "Size nasıl bir destek sağlanmasını önerirsiniz?"
                ]
            },
            "ilk_gorusme": {
                "name": "İlk Görüşme Raporu", 
                "description": "Başvuru sahibi ile yapılan ilk görüşmenin detayları",
                "questions": [
                    "İlk Görüşme Raporu için birlikte çalışalım. Görüşme tarihi ve yeri nedir?",
                    "Görüşme yaklaşık ne kadar sürdü?",
                    "Kişi neden başvuruda bulundu? Ana ihtiyacı nedir?",
                    "Kişinin bu durumdan beklentileri nelerdir?",
                    "Görüşme sırasında kişinin genel davranışları, ruh hali nasıldı?",
                    "Kişinin iletişim tarzı ve işbirliği düzeyi nasıl?",
                    "Ailevi ve sosyal durumu hakkında gözlemleriniz neler?",
                    "İlk değerlendirmenize göre öncelikli ihtiyaçlar neler?",
                    "Sonraki görüşme için planınız nedir?",
                    "Acil müdahale gerektiren bir durum var mı?"
                ]
            },
            "aile_danismanligi": {
                "name": "Aile Danışmanlığı Raporu",
                "description": "Aile danışmanlığı sürecinin değerlendirildiği rapor", 
                "questions": [
                    "Aile Danışmanlığı Raporu hazırlayalım. Aile yapısı ve üyeler hakkında bilgi verir misiniz?",
                    "Ailenin karşılaştığı temel problem nedir? Ne zaman başladı?",
                    "Aile üyeleri arasındaki ilişkiler ve roller nasıl?",
                    "Aile içi iletişim nasıl? Çatışma alanları var mı?",
                    "Ailenin güçlü yanları ve başarıyla üstesinden geldiği durumlar neler?",
                    "Risk faktörleri nelerdir? (Şiddet, madde kullanımı, ekonomik zorluk vs.)",
                    "Daha önce danışmanlık alındı mı? Sonuçları nasıldı?",
                    "Ailenin değişim motivasyonu nasıl?",
                    "Kısa vadeli hedefler neler olmalı?",
                    "Uzun vadeli hedefler ve beklentiler nelerdir?"
                ]
            },
            "cocuk_koruma": {
                "name": "Çocuk Koruma Raporu",
                "description": "Çocuğun güvenliği ve refahı ile ilgili değerlendirme raporu",
                "questions": [
                    "Çocuk Koruma Raporu için değerlendirme yapalım. Çocuk hakkında temel bilgiler nelerdir? (Yaş, cinsiyet, okul durumu)",
                    "Çocuğun bakım verenleri kimlerdir? Aile yapısı nasıl?",
                    "Çocuğa yönelik risk faktörleri nelerdir?",
                    "Çocuğun kendi ifadesi alındı mı? Neler söyledi?",
                    "Çocuğun fiziksel durumu nasıl? (Beslenme, temizlik, sağlık)",
                    "Duygusal ve davranışsal durumu nasıl? (Korku, kaygı, uyum)",
                    "Okul durumu ve akademik performansı nasıl?",
                    "Çocuğu koruyan faktörler nelerdir? (Destekçi yetişkinler, sosyal ağ)",
                    "Acil koruyucu müdahale gerekli mi?",
                    "Çocuğun güvenliği için önerileriniz nelerdir?"
                ]
            }
        }
        
        # Sohbet durumları
        self.session_state = {}
    
    def start_conversation(self, report_type: str, session_id: str) -> Dict:
        """
        Yeni bir sohbet başlat
        
        Args:
            report_type (str): Rapor türü
            session_id (str): Oturum ID'si
            
        Returns:
            Dict: İlk mesaj ve durum
        """
        if report_type not in self.report_types:
            return {
                "success": False,
                "message": "Geçersiz rapor türü",
                "available_types": list(self.report_types.keys())
            }
        
        report_info = self.report_types[report_type]
        
        # Oturum durumunu başlat
        self.session_state[session_id] = {
            "report_type": report_type,
            "current_question": 0,
            "answers": [],
            "questions": report_info["questions"],
            "completed": False,
            "started_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "message": f"🎯 {report_info['name']} oluşturma sürecine başlıyoruz!\n\n📝 {report_info['description']}\n\n{report_info['questions'][0]}",
            "question_number": 1,
            "total_questions": len(report_info["questions"]),
            "progress": 0
        }
    
    def process_answer(self, session_id: str, answer: str) -> Dict:
        """
        Kullanıcı cevabını işle ve sonraki soruyu gönder
        
        Args:
            session_id (str): Oturum ID'si
            answer (str): Kullanıcının cevabı
            
        Returns:
            Dict: Sonraki soru veya rapor tamamlama durumu
        """
        if session_id not in self.session_state:
            return {
                "success": False,
                "message": "Oturum bulunamadı. Lütfen yeniden başlayın."
            }
        
        session = self.session_state[session_id]
        
        if session["completed"]:
            return {
                "success": False,
                "message": "Bu rapor zaten tamamlanmış."
            }
        
        # Cevabı kaydet
        session["answers"].append({
            "question": session["questions"][session["current_question"]],
            "answer": answer.strip(),
            "timestamp": datetime.now().isoformat()
        })
        
        # Sonraki soruya geç
        session["current_question"] += 1
        
        # Tüm sorular tamamlandı mı?
        if session["current_question"] >= len(session["questions"]):
            session["completed"] = True
            return {
                "success": True,
                "completed": True,
                "message": "✅ Tüm sorular tamamlandı! Rapor oluşturuluyor...",
                "progress": 100
            }
        
        # Sonraki soruyu gönder
        next_question = session["questions"][session["current_question"]]
        progress = (session["current_question"] / len(session["questions"])) * 100
        
        return {
            "success": True,
            "completed": False,
            "message": next_question,
            "question_number": session["current_question"] + 1,
            "total_questions": len(session["questions"]),
            "progress": progress
        }
    
    def generate_report(self, session_id: str, context: str = None, learning_system=None) -> Dict:
        """
        Toplanan cevaplardan rapor oluştur
        
        Args:
            session_id (str): Oturum ID'si
            context (str): Ek bağlam bilgisi
            
        Returns:
            Dict: Oluşturulan rapor
        """
        if session_id not in self.session_state:
            return {
                "success": False,
                "message": "Oturum bulunamadı"
            }
        
        session = self.session_state[session_id]
        
        if not session["completed"]:
            return {
                "success": False,
                "message": "Önce tüm soruları cevaplayın"
            }
        
        report_info = self.report_types[session["report_type"]]
        
        # Prompt oluştur
        prompt = f"""
Sen bir sosyal hizmet uzmanısın ve {report_info['name']} hazırlıyorsun.

Aşağıdaki soru-cevap seansından profesyonel bir rapor oluştur:

RAPOR TÜRÜ: {report_info['name']}
AÇIKLAMA: {report_info['description']}

SORU-CEVAP VERİLERİ:
"""
        
        # Soru-cevapları ekle
        for i, qa in enumerate(session["answers"], 1):
            prompt += f"\n{i}. {qa['question']}\nCevap: {qa['answer']}\n"
        
        # Ek bağlam varsa ekle
        if context:
            prompt += f"\nEK BAĞLAM BİLGİSİ:\n{context}\n"
        
        # Öğrenme sistemi bağlamı ekle
        if learning_system:
            learning_context = learning_system.get_learning_context(session["report_type"])
            if learning_context:
                prompt += f"\n{learning_context}"
        
        # Rapor yazma talimatları
        prompt += f"""

RAPOR YAZMA TALİMATLARI:

1. YAPISAL GEREKSINIMLER:
   - Rapor başlığı ve tarih
   - Giriş bölümü (başvuru/görüşme nedeni)
   - Ana değerlendirme bölümleri (her konu için alt başlık)
   - Sonuç ve öneriler bölümü
   - Raporu hazırlayan sosyal hizmet uzmanı bilgisi

2. DİL VE ÜSLUP:
   - Profesyonel ve objektif dil
   - Açık ve anlaşılır ifadeler
   - Sosyal hizmet terminolojisi
   - Gözlemlere dayalı açıklamalar

3. İÇERİK PRİNSİPLERİ:
   - Tüm cevapları sistematik şekilde değerlendir
   - Risk ve koruyucu faktörleri belirle
   - Güçlü yanları vurgula
   - Somut ve uygulanabilir öneriler sun
   - Gizlilik ve etik kurallara uygun yaklaşım

4. RAPOR UZUNLUĞU:
   - En az 1000-1500 kelime
   - Detaylı analiz ve değerlendirme
   - Her bölüm için yeterli açıklama

Lütfen bu bilgilere dayanarak kapsamlı ve profesyonel {report_info['name']} hazırla.
"""
        
        try:
            # Gemini'den rapor oluştur
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Rapor oluşturulamadı")
            
            # Metadata hazırla
            metadata = {
                "report_type": session["report_type"],
                "report_name": report_info["name"],
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_duration": self._calculate_duration(session["started_at"]),
                "questions_answered": len(session["answers"]),
                "word_count": len(response.text.split()),
                "character_count": len(response.text)
            }
            
            return {
                "success": True,
                "content": response.text,
                "metadata": metadata,
                "session_summary": self._create_session_summary(session)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Rapor oluşturma hatası: {str(e)}"
            }
    
    def get_session_status(self, session_id: str) -> Dict:
        """Oturum durumunu getir"""
        if session_id not in self.session_state:
            return {"exists": False}
        
        session = self.session_state[session_id]
        report_info = self.report_types[session["report_type"]]
        
        return {
            "exists": True,
            "report_type": session["report_type"],
            "report_name": report_info["name"],
            "current_question": session["current_question"],
            "total_questions": len(session["questions"]),
            "progress": (session["current_question"] / len(session["questions"])) * 100,
            "completed": session["completed"],
            "answers_count": len(session["answers"])
        }
    
    def reset_session(self, session_id: str) -> bool:
        """Oturumu sıfırla"""
        if session_id in self.session_state:
            del self.session_state[session_id]
            return True
        return False
    
    def get_available_report_types(self) -> Dict:
        """Mevcut rapor türlerini döndür"""
        return {
            key: {
                "name": info["name"],
                "description": info["description"],
                "question_count": len(info["questions"])
            }
            for key, info in self.report_types.items()
        }
    
    def _calculate_duration(self, start_time: str) -> str:
        """Oturum süresini hesapla"""
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.now()
            duration = end - start
            return str(duration).split('.')[0]  # Microseconds'ı kaldır
        except:
            return "Bilinmeyen"
    
    def _create_session_summary(self, session: Dict) -> Dict:
        """Oturum özeti oluştur"""
        return {
            "report_type": session["report_type"],
            "total_questions": len(session["questions"]),
            "answered_questions": len(session["answers"]),
            "completion_rate": len(session["answers"]) / len(session["questions"]) * 100,
            "started_at": session["started_at"],
            "duration": self._calculate_duration(session["started_at"])
        }