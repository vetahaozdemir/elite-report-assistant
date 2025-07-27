"""
Rapor oluşturma ve şablon yönetimi modülü
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import os
from datetime import datetime

class ReportGenerator:
    """Sosyal hizmet raporları oluşturan sınıf"""
    
    def __init__(self, api_key: str = None):
        """
        ReportGenerator initialization
        
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
        
        # Rapor şablonları
        self.report_templates = {
            "sosyal_inceleme": {
                "name": "Sosyal İnceleme Raporu",
                "description": "Aile ve çevre koşullarının değerlendirildiği kapsamlı rapor",
                "fields": [
                    {"name": "kisi_bilgileri", "label": "Kişi Bilgileri", "type": "text", "required": True},
                    {"name": "aile_yapisi", "label": "Aile Yapısı", "type": "textarea", "required": True},
                    {"name": "sosyoekonomik_durum", "label": "Sosyoekonomik Durum", "type": "textarea", "required": True},
                    {"name": "konut_koşullari", "label": "Konut Koşulları", "type": "textarea", "required": True},
                    {"name": "saglik_durumu", "label": "Sağlık Durumu", "type": "textarea", "required": False},
                    {"name": "egitim_durumu", "label": "Eğitim Durumu", "type": "textarea", "required": False},
                    {"name": "sosyal_cevre", "label": "Sosyal Çevre", "type": "textarea", "required": True},
                    {"name": "mevcut_sorunlar", "label": "Mevcut Sorunlar", "type": "textarea", "required": True},
                    {"name": "oneriler", "label": "Öneriler ve Müdahale Planı", "type": "textarea", "required": False}
                ]
            },
            "ilk_gorusme": {
                "name": "İlk Görüşme Raporu",
                "description": "Başvuru sahibi ile yapılan ilk görüşmenin detayları",
                "fields": [
                    {"name": "gorusme_tarihi", "label": "Görüşme Tarihi", "type": "date", "required": True},
                    {"name": "gorusme_yeri", "label": "Görüşme Yeri", "type": "text", "required": True},
                    {"name": "gorusme_suresi", "label": "Görüşme Süresi (dakika)", "type": "number", "required": False},
                    {"name": "basvuru_nedeni", "label": "Başvuru Nedeni", "type": "textarea", "required": True},
                    {"name": "beklentiler", "label": "Kişinin Beklentileri", "type": "textarea", "required": True},
                    {"name": "gözlemler", "label": "Gözlemler", "type": "textarea", "required": True},
                    {"name": "ilk_degerlendirme", "label": "İlk Değerlendirme", "type": "textarea", "required": True},
                    {"name": "sonraki_adimlar", "label": "Sonraki Adımlar", "type": "textarea", "required": True}
                ]
            },
            "aile_danismanligi": {
                "name": "Aile Danışmanlığı Raporu",
                "description": "Aile danışmanlığı sürecinin değerlendirildiği rapor",
                "fields": [
                    {"name": "aile_bilgileri", "label": "Aile Bilgileri", "type": "textarea", "required": True},
                    {"name": "problem_tanimi", "label": "Problem Tanımı", "type": "textarea", "required": True},
                    {"name": "aile_dinamikleri", "label": "Aile Dinamikleri", "type": "textarea", "required": True},
                    {"name": "iletisim_kaliplari", "label": "İletişim Kalıpları", "type": "textarea", "required": True},
                    {"name": "guçlu_yanlar", "label": "Ailenin Güçlü Yanları", "type": "textarea", "required": True},
                    {"name": "risk_faktorleri", "label": "Risk Faktörleri", "type": "textarea", "required": True},
                    {"name": "mudhale_plani", "label": "Müdahale Planı", "type": "textarea", "required": True},
                    {"name": "hedefler", "label": "Kısa ve Uzun Vadeli Hedefler", "type": "textarea", "required": True}
                ]
            },
            "cocuk_koruma": {
                "name": "Çocuk Koruma Raporu",
                "description": "Çocuğun güvenliği ve refahı ile ilgili değerlendirme raporu",
                "fields": [
                    {"name": "cocuk_bilgileri", "label": "Çocuk Bilgileri", "type": "text", "required": True},
                    {"name": "bakim_verenler", "label": "Bakım Verenler", "type": "textarea", "required": True},
                    {"name": "risk_degerlendirmesi", "label": "Risk Değerlendirmesi", "type": "textarea", "required": True},
                    {"name": "cocugun_ifadesi", "label": "Çocuğun İfadesi", "type": "textarea", "required": False},
                    {"name": "fiziksel_durum", "label": "Fiziksel Durum", "type": "textarea", "required": True},
                    {"name": "duygusal_durum", "label": "Duygusal Durum", "type": "textarea", "required": True},
                    {"name": "egitim_durumu", "label": "Eğitim Durumu", "type": "textarea", "required": True},
                    {"name": "koruyucu_faktorler", "label": "Koruyucu Faktörler", "type": "textarea", "required": True},
                    {"name": "acil_mudahale", "label": "Acil Müdahale Gerekliliği", "type": "textarea", "required": True}
                ]
            }
        }
    
    def get_report_types(self) -> Dict:
        """Mevcut rapor türlerini döndür"""
        return {key: template["name"] for key, template in self.report_templates.items()}
    
    def get_report_template(self, report_type: str) -> Optional[Dict]:
        """Belirtilen rapor türü için şablonu döndür"""
        return self.report_templates.get(report_type)
    
    def generate_prompt(self, report_type: str, form_data: Dict, context: str = None) -> str:
        """
        Rapor oluşturma için prompt hazırla
        
        Args:
            report_type (str): Rapor türü
            form_data (Dict): Form verisi
            context (str): Ek bağlam bilgisi
            
        Returns:
            str: Oluşturulan prompt
        """
        template = self.report_templates.get(report_type)
        if not template:
            raise ValueError(f"Bilinmeyen rapor türü: {report_type}")
        
        # Temel prompt yapısı
        prompt = f"""
Sen bir sosyal hizmet uzmanısın ve {template['name']} hazırlıyorsun.

RAPOR BİLGİLERİ:
"""
        
        # Form verilerini ekle
        for field in template["fields"]:
            field_name = field["name"]
            field_label = field["label"]
            value = form_data.get(field_name, "")
            
            if value and str(value).strip():
                prompt += f"\n{field_label}: {value}"
        
        # Ek bağlam varsa ekle
        if context:
            prompt += f"\n\nEK BAĞLAM BİLGİSİ:\n{context}"
        
        # Rapor yazma talimatları
        prompt += f"""

LÜTfen aşağıdaki kriterlere uyarak profesyonel bir {template['name']} hazırla:

1. YAPISAL İSTENTETİR:
   - Rapor başlığı ve tarih
   - Giriş bölümü
   - Ana değerlendirme bölümleri
   - Sonuç ve öneriler
   - Raporu hazırlayan kişi bilgisi

2. DİL VE ÜSLUP:
   - Profesyonel ve objektif dil kullan
   - Kısa ve net cümleler tercih et
   - Sosyal hizmet terminolojisini doğru kullan
   - Kişisel yorumlar yerine gözlemlere dayalı açıklamalar yap

3. İÇERİK KRİTERLERİ:
   - Verilen bilgileri sistematik şekilde organize et
   - Eksik bilgileri belirt
   - Risk ve koruyucu faktörleri vurgula
   - Somut öneriler sun
   - Gizlilik kurallarına uygun yaklaşım benimse

4. ÖZEL NOTLAR:
   - Rapor en az 800-1200 kelime olmalı
   - Başlıkları ve alt başlıkları net şekilde belirt
   - Maddeler halinde özetler kullan
   - Mesleki etik kurallara uygun ifadeler kullan

Lütfen şimdi bu bilgilere dayanarak detaylı ve profesyonel raporu hazırla.
"""
        
        return prompt
    
    def generate_report(self, report_type: str, form_data: Dict, context: str = None) -> Dict:
        """
        Rapor oluştur
        
        Args:
            report_type (str): Rapor türü
            form_data (Dict): Form verisi
            context (str): Ek bağlam
            
        Returns:
            Dict: Oluşturulan rapor ve metadata
        """
        try:
            # Prompt hazırla
            prompt = self.generate_prompt(report_type, form_data, context)
            
            # Gemini'den rapor oluştur
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Rapor oluşturulamadı")
            
            # Metadata hazırla
            template = self.report_templates[report_type]
            metadata = {
                "report_type": report_type,
                "report_name": template["name"],
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "word_count": len(response.text.split()),
                "character_count": len(response.text),
                "form_fields_count": len([k for k, v in form_data.items() if v])
            }
            
            return {
                "content": response.text,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            return {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    def validate_form_data(self, report_type: str, form_data: Dict) -> Dict:
        """
        Form verilerini doğrula
        
        Args:
            report_type (str): Rapor türü
            form_data (Dict): Form verisi
            
        Returns:
            Dict: Doğrulama sonucu
        """
        template = self.report_templates.get(report_type)
        if not template:
            return {"valid": False, "errors": ["Bilinmeyen rapor türü"]}
        
        errors = []
        warnings = []
        
        for field in template["fields"]:
            field_name = field["name"]
            field_label = field["label"]
            is_required = field.get("required", False)
            field_type = field.get("type", "text")
            
            value = form_data.get(field_name, "")
            
            # Zorunlu alan kontrolü
            if is_required and (not value or not str(value).strip()):
                errors.append(f"{field_label} alanı zorunludur")
            
            # Tip kontrolü
            if value and field_type == "number":
                try:
                    int(value)
                except ValueError:
                    errors.append(f"{field_label} sayısal değer olmalıdır")
            
            # Minimum uzunluk kontrolü
            if value and field_type == "textarea" and len(str(value).strip()) < 10:
                warnings.append(f"{field_label} daha detaylı olabilir")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_sample_data(self, report_type: str) -> Dict:
        """Örnek form verisi döndür"""
        samples = {
            "sosyal_inceleme": {
                "kisi_bilgileri": "Ahmet Yılmaz, 35 yaşında, evli, 2 çocuk babası",
                "aile_yapisi": "Çekirdek aile yapısında, eşi Ayşe Yılmaz (32) ve çocukları Elif (8) ve Can (5)",
                "sosyoekonomik_durum": "Aylık gelir 15.000 TL, inşaat işçisi, düzenli gelir problemi yaşamakta",
                "konut_koşullari": "3+1 kiralık daire, temiz ve düzenli, temel ihtiyaçlar karşılanabilir durumda",
                "saglik_durumu": "Genel sağlık durumu iyi, düzenli sağlık kontrolü yaptırmakta",
                "egitim_durumu": "İlkokul mezunu, mesleki gelişim konusunda istekli",
                "sosyal_cevre": "Mahalle ile iyi ilişkiler, akraba desteği mevcut",
                "mevcut_sorunlar": "İş güvencesizliği, zaman zaman ekonomik sıkıntı",
                "oneriler": "Mesleki kurs desteği, sosyal yardım programları değerlendirilebilir"
            },
            "ilk_gorusme": {
                "gorusme_tarihi": "2024-01-15",
                "gorusme_yeri": "Sosyal Hizmet Merkezi",
                "gorusme_suresi": "45",
                "basvuru_nedeni": "Ekonomik sıkıntı nedeniyle sosyal yardım başvurusu",
                "beklentiler": "Geçici ekonomik destek ve iş bulma konusunda rehberlik",
                "gözlemler": "Sakin ve işbirlikçi tavır, motivasyon yüksek",
                "ilk_degerlendirme": "Geçici zorluk yaşayan, desteklenebilir aile profili",
                "sonraki_adimlar": "Evde görüşme planlanacak, belge tamamlama"
            }
        }
        
        return samples.get(report_type, {})