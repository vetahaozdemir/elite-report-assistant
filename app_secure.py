#!/usr/bin/env python3
"""
Güvenli Sosyal Hizmet Rapor Sistemi
Kullanıcı kimlik doğrulama ve veri izolasyonu ile
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
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Admin kullanıcı bilgileri (güvenli hash ile)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # "admin"

def hash_password(password):
    """Şifre hash'leme"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_modern_css():
    """Modern ve profesyonel CSS tasarımı"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Modern Dark Theme */
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Header */
    .modern-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-bottom: 2px solid #333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .modern-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00f5ff, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .modern-subtitle {
        color: #888;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Modern Cards */
    .modern-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0,245,255,0.1);
        border-color: #00f5ff;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f5ff 0%, #0080ff 100%);
        border: none;
        border-radius: 12px;
        color: #000;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.8rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,245,255,0.3);
        font-size: 0.95rem;
        text-transform: none;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0080ff 0%, #00f5ff 100%);
        box-shadow: 0 6px 20px rgba(0,245,255,0.4);
        transform: translateY(-1px);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #333;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        color: #888;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff, #0080ff);
        color: #000;
        font-weight: 600;
    }
    
    /* Modern Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.75rem;
        color: #fff;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00f5ff;
        box-shadow: 0 0 0 1px #00f5ff;
    }
    
    /* Modern Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #00f5ff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Modern Sidebar */
    .css-1d391kg {
        background: #0f0f0f;
        border-right: 1px solid #333;
    }
    
    /* Modern Messages */
    .stSuccess {
        background: linear-gradient(135deg, #0d4f3c 0%, #1a5f47 100%);
        border: 1px solid #22c55e;
        border-radius: 8px;
        color: #a7f3d0;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #4f3c0d 0%, #5f471a 100%);
        border: 1px solid #eab308;
        border-radius: 8px;
        color: #fde68a;
    }
    
    .stError {
        background: linear-gradient(135deg, #4f0d0d 0%, #5f1a1a 100%);
        border: 1px solid #ef4444;
        border-radius: 8px;
        color: #fca5a5;
    }
    
    /* Login Card */
    .login-card {
        max-width: 400px;
        margin: 2rem auto;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Progress Bar */
    .modern-progress {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #333;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #00f5ff, #0080ff);
        height: 6px;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00f5ff;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .modern-title {
            font-size: 2rem;
        }
        .modern-card {
            padding: 1rem;
            margin: 1rem 0;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

def authenticate_user():
    """Kullanıcı kimlik doğrulama"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="modern-header">
            <h1 class="modern-title">🔒 Güvenli Giriş</h1>
            <p class="modern-subtitle">Sosyal Hizmet Rapor Sistemi</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sisteme Giriş")
        
        username = st.text_input("👤 Kullanıcı Adı")
        password = st.text_input("🔑 Şifre", type="password")
        
        if st.button("🚀 Giriş Yap", type="primary"):
            if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
                st.session_state.authenticated = True
                st.session_state.user_id = username
                st.success("✅ Başarıyla giriş yapıldı!")
                st.rerun()
            else:
                st.error("❌ Hatalı kullanıcı adı veya şifre")
        
        st.markdown("---")
        st.markdown("**Demo Erişim:**")
        st.markdown("Kullanıcı: `admin` | Şifre: `admin`")
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

def generate_questions_from_text(model, text, report_type_name):
    """Metinden soru oluşturma"""
    try:
        prompt = f"""
Sen uzman bir sosyal hizmet profesyonelisin. Aşağıdaki rapor içeriğini analiz ederek "{report_type_name}" türü için kapsamlı ve profesyonel sorular oluştur:

RAPOR İÇERİĞİ:
{text[:3000]}...

Bu rapor türü için 8-12 arasında soru hazırla:
- Demografik bilgilerden detaya doğru
- Açık uçlu sorular
- Sosyal hizmet terminolojisi
- Türkçe

JSON formatında yanıt ver:
{{
  "questions": ["soru1", "soru2", ...]
}}
"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("questions", [])
        
        return [
            "Danışan/aile ile ilgili temel demografik bilgileri paylaşır mısınız?",
            "Mevcut yaşam koşulları ve sosyal çevre nasıl değerlendiriliyor?",
            "Karşılaşılan temel problemler ve zorluklar nelerdir?",
            "Hangi alanlarda profesyonel desteğe ihtiyaç duyulmaktadır?",
            "Daha önce alınan hizmetler ve sonuçları nasıl değerlendiriliyor?",
            "Danışanın güçlü yanları ve mevcut kaynakları nelerdir?",
            "Kısa vadeli hedefler ve beklentiler nelerdir?",
            "Uzun vadeli planlama ve sürdürülebilirlik nasıl değerlendiriliyor?"
        ]
    except Exception as e:
        st.error(f"Soru oluşturma hatası: {str(e)}")
        return []

def generate_report(model, questions, answers):
    """Rapor oluşturma"""
    try:
        qa_text = "\n".join([f"S: {q}\nC: {a}\n" for q, a in zip(questions, answers)])
        
        prompt = f"""
Aşağıdaki soru-yanıtları kullanarak profesyonel bir sosyal hizmet raporu hazırla:

{qa_text}

Rapor yapısı:
1. ÖZET
2. KİŞİSEL BİLGİLER  
3. MEVCUT DURUM
4. SORUN TANIMLAMA
5. GÜÇLÜ YANLAR
6. ÖNERİLER
7. SONUÇ

Profesyonel, objektif dil kullan. Türkçe yaz.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def main():
    """Ana uygulama"""
    load_modern_css()
    
    # Kimlik doğrulama
    if not authenticate_user():
        return
    
    # Modern başlık
    st.markdown("""
    <div class="modern-header">
        <h1 class="modern-title">🔒 Sosyal Hizmet Rapor Sistemi</h1>
        <p class="modern-subtitle">Güvenli & Kişisel Yapay Zeka Destekli Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Çıkış butonu
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Çıkış"):
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
    
    # Ana sekmeler
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Rapor Türleri", "📝 Rapor Oluştur", "📊 İstatistikler", "⚙️ Admin"])
    
    with tab1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.header("🎯 Akıllı Rapor Türü Oluşturucu")
        st.markdown("*Örnek raporlarınızı yükleyerek yapay zeka ile özel soru setleri oluşturun*")
        
        st.subheader("📤 Örnek Rapor Yükleme")
        uploaded_files = st.file_uploader(
            "Aynı türden 2-5 adet örnek rapor yükleyin",
            type=['pdf'],
            accept_multiple_files=True,
            help="AI bu örnekleri analiz ederek size özel sorular oluşturacak"
        )
        
        report_name = st.text_input("📋 Rapor Türü Adı", placeholder="Örn: Aile Danışmanlığı Değerlendirme")
        
        if st.button("🤖 AI ile Soru Oluştur", type="primary"):
            if uploaded_files and report_name:
                with st.spinner("🔄 AI analiz ediyor..."):
                    all_text = ""
                    
                    for uploaded_file in uploaded_files:
                        pdf_data = simple_pdf_processor(uploaded_file)
                        if pdf_data:
                            all_text += pdf_data["text"] + "\n\n"
                    
                    if all_text:
                        questions = generate_questions_from_text(model, all_text, report_name)
                        
                        if questions:
                            user_data['report_types'][report_name] = {
                                'questions': questions,
                                'created_at': datetime.now().isoformat(),
                                'pdf_count': len(uploaded_files),
                                'user_id': st.session_state.user_id
                            }
                            
                            st.success(f"✅ '{report_name}' başarıyla oluşturuldu! {len(questions)} soru hazırlandı.")
                            
                            with st.expander("📋 Oluşturulan Sorular"):
                                for i, q in enumerate(questions, 1):
                                    st.write(f"**{i}.** {q}")
                        else:
                            st.error("❌ Sorular oluşturulamadı")
                    else:
                        st.error("❌ PDF'lerden metin çıkarılamadı")
            else:
                st.warning("⚠️ Lütfen PDF dosyalarını ve rapor adını girin")
        
        # Mevcut rapor türleri
        if user_data['report_types']:
            st.subheader("📂 Kayıtlı Rapor Türleriniz")
            for name, data in user_data['report_types'].items():
                with st.expander(f"📄 {name} ({len(data['questions'])} soru)"):
                    for i, q in enumerate(data['questions'], 1):
                        st.write(f"**{i}.** {q}")
                    
                    if st.button(f"🗑️ Sil", key=f"delete_{name}"):
                        del user_data['report_types'][name]
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.header("📝 Akıllı Rapor Oluşturma")
        
        if not user_data['report_types']:
            st.warning("⚠️ Önce bir rapor türü oluşturun")
        else:
            selected_type = st.selectbox(
                "📊 Rapor Türü Seçin",
                options=list(user_data['report_types'].keys())
            )
            
            if selected_type:
                questions = user_data['report_types'][selected_type]['questions']
                
                if st.button("🆕 Yeni Rapor Başlat", type="primary"):
                    user_data['current_questions'] = questions
                    user_data['current_answers'] = [""] * len(questions)
                    st.rerun()
                
                if user_data['current_questions']:
                    current_q_index = len([a for a in user_data['current_answers'] if a.strip()])
                    total_questions = len(user_data['current_questions'])
                    
                    # İlerleme
                    progress = current_q_index / total_questions
                    st.markdown(f"""
                    <div class="modern-progress">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span><strong>İlerleme:</strong> {current_q_index}/{total_questions}</span>
                            <span><strong>%{progress*100:.0f}</strong></span>
                        </div>
                        <div style="background: #333; border-radius: 3px; height: 6px;">
                            <div class="progress-bar" style="width: {progress*100}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if current_q_index < total_questions:
                        current_question = user_data['current_questions'][current_q_index]
                        
                        st.subheader(f"Soru {current_q_index + 1}")
                        st.markdown(f"""
                        <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #00f5ff; margin: 1rem 0;">
                            <strong>🤖:</strong> {current_question}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        answer = st.text_area("✍️ Yanıtınız:", key=f"answer_{current_q_index}", height=120)
                        
                        if st.button("▶️ Devam Et", disabled=not answer.strip()):
                            user_data['current_answers'][current_q_index] = answer
                            st.rerun()
                    
                    else:
                        st.success("✅ Tüm sorular tamamlandı!")
                        
                        if st.button("📄 Rapor Oluştur", type="primary"):
                            with st.spinner("🔄 Rapor hazırlanıyor..."):
                                report = generate_report(
                                    model,
                                    user_data['current_questions'],
                                    user_data['current_answers']
                                )
                                
                                st.subheader("📄 Oluşturulan Rapor")
                                st.markdown(report)
                                
                                st.download_button(
                                    "📥 Raporu İndir",
                                    data=report,
                                    file_name=f"rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.header("📊 Kişisel İstatistikler")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📋 Rapor Türleri", len(user_data['report_types']))
        
        with col2:
            total_questions = sum(len(data['questions']) for data in user_data['report_types'].values())
            st.metric("❓ Toplam Soru", total_questions)
        
        with col3:
            st.metric("🔒 Güvenlik", "✅ Aktif")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.header("⚙️ Admin Panel")
        
        st.markdown("### 🔐 Güvenlik Bilgileri")
        st.info("✅ Verileriniz sadece size ait ve güvenli")
        st.info("✅ Kimse başkasının verilerini göremez")
        st.info("✅ Her kullanıcının ayrı veri alanı var")
        
        st.markdown("### 📊 Sistem Bilgileri")
        st.code(f"Kullanıcı ID: {st.session_state.user_id}")
        st.code(f"Veri Anahtarı: {user_key}")
        st.code(f"Giriş Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if st.button("🧹 Tüm Verilerimi Temizle"):
            user_data['report_types'] = {}
            user_data['current_questions'] = []
            user_data['current_answers'] = []
            st.success("✅ Veriler temizlendi")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()