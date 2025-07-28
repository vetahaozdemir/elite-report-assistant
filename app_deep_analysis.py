#!/usr/bin/env python3
"""
Sosyal Hizmet Rapor Sistemi - Derinlemesine Analiz Versiyonu
Emerald-Gray tema + Güvenli kullanıcı sistemi + Detaylı AI analizi
"""

import streamlit as st
import os
import uuid
import json
import tempfile
import hashlib
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Sosyal Hizmet Rapor Sistemi",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kullanıcı bilgileri
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("Taha_2123652".encode()).hexdigest()

# Normal kullanıcılar için demo hesap
DEMO_USERS = {
    "demo": hashlib.sha256("demo123".encode()).hexdigest(),
    "user1": hashlib.sha256("user123".encode()).hexdigest()
}

def hash_password(password):
    """Şifre hash'leme"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_emerald_theme():
    """Emerald-Gray temayı yükle (okuyucu.html'den esinlenme)"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Ana tema - Emerald & Gray */
    .stApp {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 50%, #f9fafb 100%);
        font-family: 'Poppins', sans-serif;
        color: #374151;
    }
    
    /* Modern Header */
    .emerald-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2.5rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.15);
        border-bottom: 3px solid #047857;
    }
    
    .emerald-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .emerald-subtitle {
        color: #d1fae5;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Modern Cards */
    .emerald-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        border-left: 4px solid #10b981;
    }
    
    .emerald-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.1);
        border-left-color: #047857;
    }
    
    /* Emerald Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
        font-size: 0.95rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
        transform: translateY(-1px);
    }
    
    /* Emerald Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #f9fafb;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        color: #6b7280;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'Poppins', sans-serif;
        transition: border-color 0.2s ease;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Modern Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #10b981;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #10b981;
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Login Card */
    .login-card {
        max-width: 420px;
        margin: 2rem auto;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #10b981;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #10b981;
        border-radius: 8px;
        color: #065f46;
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        color: #92400e;
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid #ef4444;
        border-radius: 8px;
        color: #dc2626;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .emerald-progress {
        background: #f3f4f6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #10b981;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #10b981, #059669);
        height: 8px;
        border-radius: 4px;
        transition: width 0.5s ease;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Question Card */
    .question-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }
    
    /* Analysis Card */
    .analysis-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #0ea5e9;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .emerald-title {
            font-size: 2rem;
        }
        .emerald-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .login-card {
            margin: 1rem;
            padding: 2rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

def authenticate_user():
    """Kullanıcı kimlik doğrulama sistemi"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="emerald-header">
            <h1 class="emerald-title">📋 Sosyal Hizmet Rapor Sistemi</h1>
            <p class="emerald-subtitle">Derinlemesine AI Analizi ile Güvenli Giriş</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sistem Girişi")
        st.markdown("*Verilerinizin güvenliği için kimlik doğrulama gereklidir*")
        
        username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin")
        password = st.text_input("🔑 Şifre", type="password", placeholder="Şifrenizi girin")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Giriş Yap", type="primary"):
                user_hash = hash_password(password)
                
                # Admin kontrolü
                if username == ADMIN_USERNAME and user_hash == ADMIN_PASSWORD_HASH:
                    st.session_state.authenticated = True
                    st.session_state.user_id = username
                    st.session_state.user_type = "admin"
                    st.success("✅ Admin olarak giriş yapıldı!")
                    st.rerun()
                
                # Normal kullanıcı kontrolü
                elif username in DEMO_USERS and user_hash == DEMO_USERS[username]:
                    st.session_state.authenticated = True
                    st.session_state.user_id = username
                    st.session_state.user_type = "user"
                    st.success("✅ Kullanıcı olarak giriş yapıldı!")
                    st.rerun()
                
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre")
        
        with col2:
            if st.button("👥 Demo Hesap"):
                st.session_state.authenticated = True
                st.session_state.user_id = "demo"
                st.session_state.user_type = "user"
                st.success("✅ Demo hesabıyla giriş yapıldı!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("**📝 Hesap Bilgileri:**")
        st.markdown("""
        - **Admin**: Derinlemesine analiz + rapor türü oluşturma + rapor yazma
        - **Kullanıcı**: Sadece rapor oluşturma yetkisi
        - **Demo**: Hızlı test için
        """)
        
        st.markdown("**🔒 Güvenlik:** Verileriniz kullanıcıya özeldir, başkaları göremez")
        st.markdown('</div>', unsafe_allow_html=True)
        
        return False
    
    return True

def get_user_data_key():
    """Kullanıcıya özel veri anahtarı"""
    return f"user_data_{st.session_state.user_id}"

def configure_api():
    """API konfigürasyonu"""
    try:
        api_key = None
        
        if "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
            api_key = st.secrets["general"]["GEMINI_API_KEY"]
        elif "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            st.error("❌ API anahtarı bulunamadı")
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ API hatası: {str(e)}")
        st.stop()

def simple_pdf_processor(uploaded_file):
    """PDF işleyici"""
    try:
        import pypdf
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        text = ""
        with open(tmp_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        os.unlink(tmp_path)
        
        return {
            "text": text,
            "pages": len(pdf_reader.pages),
            "title": uploaded_file.name
        }
    except Exception as e:
        st.error(f"PDF işleme hatası: {str(e)}")
        return None

def deep_analyze_reports(model, texts, report_type_name):
    """Raporları derinlemesine analiz et"""
    try:
        combined_text = "\n\n--- YENİ RAPOR ---\n\n".join(texts)
        
        analysis_prompt = f"""
Sen uzman bir sosyal hizmet profesyonelisin. Aşağıdaki {len(texts)} adet raporu derinlemesine analiz et ve "{report_type_name}" türü için kapsamlı bir değerlendirme yap:

RAPOR İÇERİKLERİ:
{combined_text[:6000]}...

KAPSAMLI ANALİZ YAP:

1. RAPOR YAPISI VE METODOLOJİ:
   - Bu raporlar hangi bölümlerden oluşuyor?
   - Bilgi toplama yöntemleri neler?
   - Hangi değerlendirme araçları kullanılmış?
   - Rapor yazım tarzı ve formatı nasıl?

2. İÇERİK VE KAPSAM ANALİZİ:
   - Hangi konular detaylı olarak inceleniyor?
   - En çok odaklanılan alanlar neler?
   - Hangi risk faktörleri değerlendiriliyor?
   - Sosyal, ekonomik, psikolojik hangi boyutlar var?

3. PROFESYONELLİK VE YAKLAŞIM:
   - Hangi sosyal hizmet teorileri/yaklaşımları kullanılmış?
   - Terminoloji düzeyi nasıl?
   - Objektiflik ve bilimsel yaklaşım var mı?
   - Kültürel duyarlılık nasıl?

4. SONUÇ VE ÖNERİ YAPISI:
   - Raporlar hangi tip sonuçlara ulaşıyor?
   - Nasıl öneriler veriliyor?
   - Eylem planları nasıl oluşturuluyor?
   - İzleme ve değerlendirme nasıl planlanıyor?

5. HEDEF KITLE VE CONTEXT:
   - Bu raporlar kimler için yazılıyor?
   - Hangi kurumsal yapıya hitap ediyor?
   - Yasal ve etik gereklilikler nasıl ele alınıyor?

DETAYLI JSON RAPOR ÇIKAR:
{{
  "report_structure": {{
    "sections": ["bölüm1", "bölüm2", ...],
    "methodology": "metodoloji açıklaması",
    "assessment_tools": ["araç1", "araç2", ...]
  }},
  "content_analysis": {{
    "primary_focus_areas": ["alan1", "alan2", ...],
    "risk_factors": ["risk1", "risk2", ...],
    "dimensions": ["boyut1", "boyut2", ...]
  }},
  "professional_approach": {{
    "theories_used": ["teori1", "teori2", ...],
    "terminology_level": "seviye",
    "objectivity": "değerlendirme",
    "cultural_sensitivity": "durum"
  }},
  "output_characteristics": {{
    "conclusion_style": "sonuç tarzı",
    "recommendation_type": "öneri türü",
    "action_plan_approach": "eylem planı yaklaşımı"
  }},
  "target_context": {{
    "target_audience": "hedef kitle",
    "institutional_context": "kurumsal bağlam",
    "legal_requirements": "yasal gereksinimler"
  }}
}}
"""
        
        analysis_response = model.generate_content(analysis_prompt)
        
        if analysis_response.text:
            import re
            json_match = re.search(r'\{.*\}', analysis_response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        
        return {"error": "Analiz başarısız"}
        
    except Exception as e:
        st.error(f"Derinlemesine analiz hatası: {str(e)}")
        return {"error": str(e)}

def generate_questions_from_analysis(model, analysis_result, report_type_name):
    """Derinlemesine analizden sorular oluştur"""
    try:
        question_prompt = f"""
Derinlemesine rapor analizi tamamlandı. Şimdi bu analiz sonuçlarına göre "{report_type_name}" türü için MÜKEMMELsoru seti oluştur:

DETAYLI ANALİZ SONUÇLARI:
{json.dumps(analysis_result, ensure_ascii=False, indent=2)}

SORU OLUŞTURMA PRİNCİPLERİ:

1. YAPISAL TAKLİT:
   - Analiz edilen raporların bölüm yapısını taklit et
   - Aynı metodoloji ve değerlendirme araçlarını gerektiren sorular
   - Profesyonellik düzeyini yansıtan sorular

2. İÇERİK DERİNLİĞİ:
   - Primary focus area'ları kapsayan detaylı sorular
   - Risk faktörlerini değerlendiren sorular
   - Tüm boyutları (sosyal, ekonomik, psikolojik) kapsayan

3. PROFESYONELLİK:
   - Analiz edilen teorik yaklaşımları yansıtan
   - Terminoloji düzeyine uygun
   - Objektif ve bilimsel yaklaşım gerektiren

4. ÇIKTI KALİTESİ:
   - Analiz edilen sonuç ve öneri tarzını üretecek
   - Eylem planı yaklaşımını destekleyecek
   - Hedef kitle ve kurumsal bağlama uygun

5. GENEL UYGULAMA:
   - Spesifik isim/yaş/adres KESİNLİKLE YOK
   - Her vaka için uygulanabilir
   - "Danışan", "birey", "aile" gibi genel terimler

KAPSAMLI SORU SETİ OLUŞTUR:
- 10-18 arasında soru
- Analiz edilen bölüm yapısına göre sıralama
- Her önemli alanı kapsayan
- Profesyonel derinlikte bilgi toplayacak

JSON formatında yanıt ver:
{{
  "questions": [
    "soru1",
    "soru2",
    ...
  ],
  "question_rationale": {{
    "structure_basis": "yapısal temel açıklaması",
    "content_coverage": "kapsam açıklaması",
    "expected_output": "beklenen çıktı açıklaması"
  }}
}}
"""
        
        response = model.generate_content(question_prompt)
        
        if response.text:
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("questions", [])
        
        # Fallback
        return [
            "Danışanın temel demografik ve sosyal bilgileri nelerdir?",
            "Mevcut yaşam koşulları ve çevresel faktörler nasıl değerlendiriliyor?",
            "Aile dinamikleri ve ilişki kalıpları hakkında ne gözlemlenmektedir?",
            "Sosyoekonomik durum ve kaynaklara erişim nasıldır?",
            "Karşılaşılan sorunların kök nedenleri nelerdir?",
            "Risk faktörleri ve koruyucu faktörler neler olarak belirlenmektedir?",
            "Güçlü yanlar ve mevcut kapasiteler nelerdir?",
            "Daha önceki müdahaleler ve sonuçları nasıl değerlendiriliyor?",
            "Öncelikli ihtiyaç alanları hangileridir?",
            "Kısa ve uzun vadeli hedefler nasıl belirlenmelidir?"
        ]
        
    except Exception as e:
        st.error(f"Soru oluşturma hatası: {str(e)}")
        return []

def generate_report(model, questions, answers):
    """Profesyonel rapor oluşturma"""
    try:
        qa_text = "\n".join([f"Soru: {q}\nYanıt: {a}\n" for q, a in zip(questions, answers)])
        
        prompt = f"""
Aşağıdaki soru-yanıtları kullanarak profesyonel bir sosyal hizmet raporu hazırla:

{qa_text}

RAPOR YAPISI (Detaylı ve Profesyonel):

1. RAPOR ÖZETİ
   - Ana bulgular
   - Önemli risk ve koruyucu faktörler
   - Öncelikli müdahale alanları

2. DEMOGRAFİK VE GENEL BİLGİLER
   - Kişisel bilgiler
   - Aile yapısı
   - Sosyal çevre

3. MEVCUT DURUM DEĞERLENDİRMESİ
   - Yaşam koşulları
   - Sosyoekonomik durum
   - Sağlık durumu

4. SORUN TANIMLAMA VE ANALİZ
   - Problem alanları
   - Kök nedenler
   - Etkileyen faktörler

5. RİSK VE KORUYUCU FAKTÖRLER
   - Risk değerlendirmesi
   - Güçlü yanlar
   - Mevcut kaynaklar

6. MÜDAHAlE ÖNERİLERİ VE EYLEM PLANI
   - Kısa vadeli hedefler
   - Uzun vadeli planlar
   - Önerilen hizmetler

7. İZLEME VE DEĞERLENDİRME
   - Başarı kriterleri
   - İzleme planı
   - Gözden geçirme tarihleri

Profesyonel, objektif, yapılandırılmış ve detaylı bir dil kullan. Tamamen Türkçe yaz.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def admin_report_types_tab(model, user_data):
    """Admin - Rapor türü yönetimi sekmesi - Derinlemesine analiz ile"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("🎯 Derinlemesine AI Analiz ile Rapor Türü Oluşturucu")
    st.markdown("*Raporlarınızı derinlemesine analiz ederek mükemmel soru setleri oluşturuyoruz*")
    
    st.subheader("📤 Örnek Rapor Yükleme")
    st.markdown("**En az 2-3, ideal olarak 3-5 adet aynı türden rapor yükleyin**")
    
    uploaded_files = st.file_uploader(
        "Aynı türden örnek raporlar",
        type=['pdf'],
        accept_multiple_files=True,
        help="AI bu raporları derinlemesine analiz ederek yapı, metodoloji ve yaklaşımları öğrenecek"
    )
    
    report_name = st.text_input("📋 Rapor Türü Adı", placeholder="Örn: Aile Danışmanlığı Değerlendirme Raporu")
    
    if st.button("🧠 Derinlemesine AI Analizi Başlat", type="primary"):
        if uploaded_files and report_name and len(uploaded_files) >= 2:
            with st.spinner("🔄 AI raporları derinlemesine analiz ediyor..."):
                all_texts = []
                
                # PDF'leri işle
                for uploaded_file in uploaded_files:
                    pdf_data = simple_pdf_processor(uploaded_file)
                    if pdf_data:
                        all_texts.append(pdf_data["text"])
                
                if all_texts:
                    # Derinlemesine analiz
                    st.markdown("### 🔍 Analiz Aşaması 1: Derinlemesine Rapor Analizi")
                    analysis_result = deep_analyze_reports(model, all_texts, report_name)
                    
                    if "error" not in analysis_result:
                        # Analiz sonuçlarını göster
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("**🎯 Analiz Tamamlandı!**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if "report_structure" in analysis_result:
                                st.markdown("**📊 Rapor Yapısı:**")
                                st.json(analysis_result["report_structure"])
                        
                        with col2:
                            if "content_analysis" in analysis_result:
                                st.markdown("**📝 İçerik Analizi:**")
                                st.json(analysis_result["content_analysis"])
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Soru oluşturma aşaması
                        st.markdown("### 🔍 Analiz Aşaması 2: Özelleştirilmiş Soru Oluşturma")
                        with st.spinner("🎯 Analiz sonuçlarına göre özelleştirilmiş sorular oluşturuluyor..."):
                            questions = generate_questions_from_analysis(model, analysis_result, report_name)
                            
                            if questions:
                                # Report type'ı kaydet
                                user_data['report_types'][report_name] = {
                                    'questions': questions,
                                    'created_at': datetime.now().isoformat(),
                                    'pdf_count': len(uploaded_files),
                                    'user_id': st.session_state.user_id,
                                    'analysis_result': analysis_result
                                }
                                
                                st.success(f"✅ '{report_name}' başarıyla oluşturuldu! {len(questions)} adet derinlemesine analiz sonucu soru hazırlandı.")
                                
                                with st.expander("📋 Oluşturulan Sorular"):
                                    for i, q in enumerate(questions, 1):
                                        st.write(f"**{i}.** {q}")
                                
                                # Analiz özetini göster
                                with st.expander("🔍 Analiz Özeti"):
                                    st.json(analysis_result)
                            else:
                                st.error("❌ Analiz tamamlandı ama sorular oluşturulamadı")
                    else:
                        st.error(f"❌ Derinlemesine analiz başarısız: {analysis_result.get('error', 'Bilinmeyen hata')}")
                else:
                    st.error("❌ PDF dosyalarından metin çıkarılamadı")
        else:
            if len(uploaded_files) < 2:
                st.warning("⚠️ Derinlemesine analiz için en az 2 PDF gerekli")
            else:
                st.warning("⚠️ Lütfen PDF dosyalarını yükleyin ve rapor türü adını girin")
    
    # Mevcut rapor türleri
    if user_data['report_types']:
        st.subheader("📂 Oluşturulan Rapor Türleri")
        for name, data in user_data['report_types'].items():
            with st.expander(f"📄 {name} ({len(data['questions'])} soru) - {data['created_at'][:10]}"):
                
                # Soruları göster
                st.markdown("**📋 Sorular:**")
                for i, q in enumerate(data['questions'], 1):
                    st.write(f"**{i}.** {q}")
                
                # Analiz sonuçları varsa göster
                if 'analysis_result' in data:
                    with st.expander("🔍 Derinlemesine Analiz Sonuçları"):
                        st.json(data['analysis_result'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📊 PDF: {data['pdf_count']} • Analiz: Detaylı")
                with col2:
                    if st.button(f"🗑️ Sil", key=f"delete_{name}"):
                        del user_data['report_types'][name]
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def report_creation_tab(model, user_data):
    """Rapor oluşturma sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("📝 Derinlemesine Analiz Destekli Rapor Oluşturma")
    st.markdown("*AI analizi ile hazırlanmış özelleştirilmiş soru setlerini kullanarak profesyonel raporlar oluşturun*")
    
    if not user_data['report_types']:
        if st.session_state.user_type == "admin":
            st.warning("⚠️ Önce 'Rapor Türü Yönetimi' sekmesinden derinlemesine analiz ile bir rapor türü oluşturun")
        else:
            st.warning("⚠️ Sistem yöneticisi henüz derinlemesine analiz ile rapor türü tanımlamamış")
    else:
        # Rapor türü seçimi
        selected_type = st.selectbox(
            "📊 AI Analizi ile Oluşturulan Rapor Türünü Seçin",
            options=list(user_data['report_types'].keys()),
            help="Derinlemesine AI analizi ile hazırlanmış rapor türlerinden birini seçin"
        )
        
        if selected_type:
            questions = user_data['report_types'][selected_type]['questions']
            
            # Rapor türü bilgilerini göster
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"📋 Seçilen: **{selected_type}** ({len(questions)} derinlemesine analiz sorusu)")
                if 'analysis_result' in user_data['report_types'][selected_type]:
                    with st.expander("🔍 Bu Rapor Türünün AI Analiz Özeti"):
                        analysis = user_data['report_types'][selected_type]['analysis_result']
                        if 'content_analysis' in analysis and 'primary_focus_areas' in analysis['content_analysis']:
                            st.markdown("**🎯 Ana Odak Alanları:**")
                            for area in analysis['content_analysis']['primary_focus_areas']:
                                st.write(f"• {area}")
            
            with col2:
                if st.button("🆕 Yeni Rapor Başlat", type="primary"):
                    user_data['current_questions'] = questions
                    user_data['current_answers'] = [""] * len(questions)
                    st.rerun()
            
            # Soru-cevap arayüzü
            if user_data['current_questions']:
                current_q_index = len([a for a in user_data['current_answers'] if a.strip()])
                total_questions = len(user_data['current_questions'])
                
                # İlerleme çubuğu
                progress = current_q_index / total_questions
                st.markdown(f"""
                <div class="emerald-progress">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                        <span><strong>📊 İlerleme:</strong> {current_q_index}/{total_questions} derinlemesine soru tamamlandı</span>
                        <span><strong>%{progress*100:.0f}</strong></span>
                    </div>
                    <div style="background: #e5e7eb; border-radius: 4px; height: 8px;">
                        <div class="progress-bar" style="width: {progress*100}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if current_q_index < total_questions:
                    # Mevcut soru
                    current_question = user_data['current_questions'][current_q_index]
                    
                    st.subheader(f"Soru {current_q_index + 1}/{total_questions}")
                    
                    st.markdown(f"""
                    <div class="question-card">
                        <strong>🤖 AI Analizi Sorusu:</strong> {current_question}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Cevap input
                    answer = st.text_area(
                        "✍️ Detaylı Yanıtınız:", 
                        key=f"answer_{current_q_index}", 
                        height=150,
                        placeholder="Derinlemesine analiz için lütfen soruyu mümkün olduğunca detaylı yanıtlayın..."
                    )
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("▶️ Devam Et", disabled=not answer.strip()):
                            user_data['current_answers'][current_q_index] = answer
                            st.rerun()
                    
                    with col2:
                        if answer.strip():
                            word_count = len(answer.split())
                            if word_count < 10:
                                st.warning(f"⚠️ Yanıt çok kısa ({word_count} kelime). Daha detaylı yanıt verin.")
                            else:
                                st.success(f"✅ İyi yanıt ({word_count} kelime). Devam edebilirsiniz.")
                
                else:
                    # Tüm sorular tamamlandı
                    st.success("🎉 Tüm derinlemesine analiz soruları başarıyla yanıtlandı!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📄 Profesyonel Rapor Oluştur", type="primary"):
                            with st.spinner("🔄 AI derinlemesine analiz sonuçlarını kullanarak profesyonel rapor hazırlıyor..."):
                                report = generate_report(
                                    model,
                                    user_data['current_questions'],
                                    user_data['current_answers']
                                )
                                
                                st.subheader("📄 Derinlemesine Analiz ile Oluşturulan Rapor")
                                st.markdown("---")
                                st.markdown(report)
                                st.markdown("---")
                                
                                # İndirme butonu
                                report_filename = f"derinlemesine_analiz_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                st.download_button(
                                    "📥 Profesyonel Raporu İndir",
                                    data=report,
                                    file_name=report_filename,
                                    mime="text/plain"
                                )
                    
                    with col2:
                        if st.button("🔄 Yeni Rapor Başlat"):
                            user_data['current_questions'] = []
                            user_data['current_answers'] = []
                            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def statistics_tab(user_data):
    """İstatistikler sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    
    title = "📊 Derinlemesine Analiz Sistem İstatistikleri" if st.session_state.user_type == "admin" else "📊 Kişisel İstatistikler"
    st.header(title)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 AI Analiz Rapor Türleri", len(user_data['report_types']))
    
    with col2:
        total_questions = sum(len(data['questions']) for data in user_data['report_types'].values())
        st.metric("❓ Toplam Derinlemesine Soru", total_questions)
    
    with col3:
        status = "🧠 Derinlemesine AI" if st.session_state.user_type == "admin" else "👤 Kullanıcı"
        st.metric("🔍 Analiz Türü", status)
    
    if user_data['report_types']:
        st.subheader("📈 Derinlemesine Analiz Rapor Türleri")
        for name, data in user_data['report_types'].items():
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid #e5e7eb; border-left: 4px solid #10b981;">
                <strong>📄 {name}</strong><br>
                <small>📊 {len(data['questions'])} derinlemesine soru • 📅 {data['created_at'][:10]} • 📁 {data['pdf_count']} PDF analizi</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def admin_panel_tab(user_data):
    """Admin panel sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("⚙️ Derinlemesine Analiz Admin Paneli")
    
    st.markdown("### 🔐 Güvenlik ve Analiz Durumu")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Derinlemesine AI Analizi Aktif")
        st.success("✅ Veri İzolasyonu Aktif")
        st.success("✅ Şifreli Kimlik Doğrulama")
    
    with col2:
        st.info("🧠 Raporlar derinlemesine analiz ediliyor")
        st.info("🎯 Özelleştirilmiş sorular oluşturuluyor")
        st.info("📊 Kullanıcılar sadece kendi verilerini görür")
    
    st.markdown("### 📊 Sistem Bilgileri")
    col1, col2 = st.columns(2)
    
    with col1:
        st.code(f"👤 Kullanıcı: {st.session_state.user_id}")
        st.code(f"🔑 Yetki: {st.session_state.user_type}")
        st.code(f"📅 Giriş: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    with col2:
        st.code(f"🗂️ Veri Anahtarı: {get_user_data_key()}")
        st.code(f"📋 Analiz Edilmiş Türler: {len(user_data['report_types'])}")
        st.code(f"🔍 Analiz Türü: Derinlemesine AI")
    
    st.markdown("### 🧹 Veri Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Tüm Analiz Sonuçlarını Sil"):
            user_data['report_types'] = {}
            st.success("✅ Derinlemesine analiz sonuçları temizlendi")
    
    with col2:
        if st.button("🔄 Mevcut Rapor Oturumunu Sıfırla"):
            user_data['current_questions'] = []
            user_data['current_answers'] = []
            st.success("✅ Oturum sıfırlandı")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Ana uygulama"""
    load_emerald_theme()
    
    # Kimlik doğrulama
    if not authenticate_user():
        return
    
    # Kullanıcı tipine göre başlık
    user_type_text = "🧠 Derinlemesine AI Admin Panel" if st.session_state.user_type == "admin" else "👤 Kullanıcı Panel"
    
    # Header
    st.markdown(f"""
    <div class="emerald-header">
        <h1 class="emerald-title">📋 Sosyal Hizmet Rapor Sistemi</h1>
        <p class="emerald-subtitle">{user_type_text} - Hoş geldin, {st.session_state.user_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Çıkış butonu
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()
    
    # API konfigürasyonu
    model = configure_api()
    
    # Kullanıcıya özel session state
    user_key = get_user_data_key()
    if user_key not in st.session_state:
        st.session_state[user_key] = {
            'report_types': {},
            'current_chat': [],
            'current_questions': [],
            'current_answers': []
        }
    
    user_data = st.session_state[user_key]
    
    # Kullanıcı tipine göre sekmeler
    if st.session_state.user_type == "admin":
        # Admin - Tüm sekmeler
        tab1, tab2, tab3, tab4 = st.tabs(["🧠 Derinlemesine AI Analiz", "📝 Rapor Oluştur", "📊 İstatistikler", "⚙️ Admin Panel"])
        
        with tab1:
            admin_report_types_tab(model, user_data)
        
        with tab4:
            admin_panel_tab(user_data)
    else:
        # Normal kullanıcı - Sadece rapor oluşturma
        tab1, tab2 = st.tabs(["📝 Rapor Oluştur", "📊 İstatistiklerim"])
    
    # Ortak sekmeler
    with tab2 if st.session_state.user_type == "admin" else tab1:
        report_creation_tab(model, user_data)
    
    with tab3 if st.session_state.user_type == "admin" else tab2:
        statistics_tab(user_data)

if __name__ == "__main__":
    main()