#!/usr/bin/env python3
"""
Sosyal Hizmet Rapor Sistemi - Son Versiyon
Emerald-Gray tema + Güvenli kullanıcı sistemi
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
    
    /* Focus ring style */
    .focus-ring-style {
        transition: all 0.2s ease;
    }
    .focus-ring-style:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
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
            <p class="emerald-subtitle">Güvenli Giriş Portalı</p>
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
        - **Admin**: Tam yetki (rapor türü oluşturma + rapor yazma)
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

def generate_questions_from_text(model, text, report_type_name):
    """Metinden soru oluşturma"""
    try:
        prompt = f"""
Sen uzman bir sosyal hizmet profesyonelisin. Aşağıdaki rapor içeriğini analiz ederek "{report_type_name}" türü için kapsamlı ve profesyonel sorular oluştur:

RAPOR İÇERİĞİ:
{text[:3000]}...

Bu rapor türü için 8-12 arasında soru hazırla:
- Demografik bilgilerden detaya doğru sıralama
- Açık uçlu ve detaylı yanıt gerektiren sorular
- Sosyal hizmet terminolojisi kullanan
- Anlaşılır ve uygulanabilir
- Tamamen Türkçe

JSON formatında yanıt ver:
{{
  "questions": [
    "soru1",
    "soru2",
    ...
  ]
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
    """Profesyonel rapor oluşturma"""
    try:
        qa_text = "\n".join([f"Soru: {q}\nYanıt: {a}\n" for q, a in zip(questions, answers)])
        
        prompt = f"""
Aşağıdaki soru-yanıtları kullanarak profesyonel bir sosyal hizmet raporu hazırla:

{qa_text}

Rapor yapısı:
1. RAPOR ÖZETİ
2. KİŞİSEL VE DEMOGRAFİK BİLGİLER
3. MEVCUT DURUM DEĞERLENDİRMESİ
4. SORUN TANIMLAMA VE ANALİZ
5. GÜÇLÜ YANLAR VE KAYNAKLAR
6. MÜDAHAlE ÖNERİLERİ VE PLAN
7. SONUÇ VE DEĞERLENDİRME

Profesyonel, objektif ve yapılandırılmış bir dil kullan. Tamamen Türkçe yaz.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def main():
    """Ana uygulama"""
    load_emerald_theme()
    
    # Kimlik doğrulama
    if not authenticate_user():
        return
    
    # Kullanıcı tipine göre başlık
    user_type_text = "👑 Admin Panel" if st.session_state.user_type == "admin" else "👤 Kullanıcı Panel"
    
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
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Rapor Türü Yönetimi", "📝 Rapor Oluştur", "📊 İstatistikler", "⚙️ Admin Panel"])
        
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

def admin_report_types_tab(model, user_data):
    """Admin - Rapor türü yönetimi sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("🎯 Akıllı Rapor Türü Oluşturucu")
    st.markdown("*Sadece admin yetkisiyle rapor türleri oluşturabilirsiniz*")
    
    st.subheader("📤 Örnek Rapor Yükleme")
    uploaded_files = st.file_uploader(
        "Aynı türden 2-5 adet örnek rapor yükleyin",
        type=['pdf'],
        accept_multiple_files=True,
        help="AI bu örnekleri analiz ederek profesyonel sorular oluşturacak"
    )
    
    report_name = st.text_input("📋 Rapor Türü Adı", placeholder="Örn: Aile Danışmanlığı Değerlendirme Raporu")
    
    if st.button("🤖 AI ile Soru Oluştur", type="primary"):
        if uploaded_files and report_name:
            with st.spinner("🔄 AI dosyaları analiz ediyor ve sorular oluşturuyor..."):
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
                        
                        st.success(f"✅ '{report_name}' başarıyla oluşturuldu! {len(questions)} adet profesyonel soru hazırlandı.")
                        
                        with st.expander("📋 Oluşturulan Sorular"):
                            for i, q in enumerate(questions, 1):
                                st.write(f"**{i}.** {q}")
                    else:
                        st.error("❌ Dosyalardan soru oluşturulamadı")
                else:
                    st.error("❌ PDF dosyalarından metin çıkarılamadı")
        else:
            st.warning("⚠️ Lütfen PDF dosyalarını yükleyin ve rapor türü adını girin")
    
    # Mevcut rapor türleri
    if user_data['report_types']:
        st.subheader("📂 Oluşturulan Rapor Türleri")
        for name, data in user_data['report_types'].items():
            with st.expander(f"📄 {name} ({len(data['questions'])} soru) - {data['created_at'][:10]}"):
                for i, q in enumerate(data['questions'], 1):
                    st.write(f"**{i}.** {q}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📊 PDF Sayısı: {data['pdf_count']}")
                with col2:
                    if st.button(f"🗑️ Sil", key=f"delete_{name}"):
                        del user_data['report_types'][name]
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def report_creation_tab(model, user_data):
    """Rapor oluşturma sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("📝 Akıllı Rapor Oluşturma")
    st.markdown("*Hazırlanmış soru setlerini kullanarak detaylı raporlar oluşturun*")
    
    if not user_data['report_types']:
        if st.session_state.user_type == "admin":
            st.warning("⚠️ Önce 'Rapor Türü Yönetimi' sekmesinden bir rapor türü oluşturun")
        else:
            st.warning("⚠️ Sistem yöneticisi henüz rapor türü tanımlamamış")
    else:
        # Rapor türü seçimi
        selected_type = st.selectbox(
            "📊 Rapor Türünü Seçin",
            options=list(user_data['report_types'].keys()),
            help="Mevcut rapor türlerinden birini seçerek soru-cevap sürecini başlatın"
        )
        
        if selected_type:
            questions = user_data['report_types'][selected_type]['questions']
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"📋 Seçilen: **{selected_type}** ({len(questions)} soru)")
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
                        <span><strong>📊 İlerleme:</strong> {current_q_index}/{total_questions} soru tamamlandı</span>
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
                        <strong>🤖 Sistem:</strong> {current_question}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Cevap input
                    answer = st.text_area(
                        "✍️ Yanıtınız:", 
                        key=f"answer_{current_q_index}", 
                        height=120,
                        placeholder="Lütfen soruyu detaylı şekilde yanıtlayın..."
                    )
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("▶️ Devam Et", disabled=not answer.strip()):
                            user_data['current_answers'][current_q_index] = answer
                            st.rerun()
                    
                    with col2:
                        if answer.strip():
                            st.success("✅ Yanıt hazır, devam edebilirsiniz")
                
                else:
                    # Tüm sorular tamamlandı
                    st.success("🎉 Tüm sorular başarıyla yanıtlandı!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📄 Profesyonel Rapor Oluştur", type="primary"):
                            with st.spinner("🔄 AI raporunuzu hazırlıyor..."):
                                report = generate_report(
                                    model,
                                    user_data['current_questions'],
                                    user_data['current_answers']
                                )
                                
                                st.subheader("📄 Oluşturulan Rapor")
                                st.markdown("---")
                                st.markdown(report)
                                st.markdown("---")
                                
                                # İndirme butonu
                                report_filename = f"sosyal_hizmet_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                st.download_button(
                                    "📥 Raporu İndir",
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
    
    title = "📊 Sistem İstatistikleri" if st.session_state.user_type == "admin" else "📊 Kişisel İstatistikler"
    st.header(title)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 Rapor Türleri", len(user_data['report_types']))
    
    with col2:
        total_questions = sum(len(data['questions']) for data in user_data['report_types'].values())
        st.metric("❓ Toplam Soru", total_questions)
    
    with col3:
        status = "👑 Admin" if st.session_state.user_type == "admin" else "👤 Kullanıcı"
        st.metric("🔒 Yetki Seviyesi", status)
    
    if user_data['report_types']:
        st.subheader("📈 Rapor Türleri Detayı")
        for name, data in user_data['report_types'].items():
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid #e5e7eb; border-left: 4px solid #10b981;">
                <strong>📄 {name}</strong><br>
                <small>📊 {len(data['questions'])} soru • 📅 {data['created_at'][:10]} • 📁 {data['pdf_count']} PDF</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def admin_panel_tab(user_data):
    """Admin panel sekmesi"""
    st.markdown('<div class="emerald-card">', unsafe_allow_html=True)
    st.header("⚙️ Admin Kontrol Paneli")
    
    st.markdown("### 🔐 Güvenlik Durumu")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Veri İzolasyonu Aktif")
        st.success("✅ Şifreli Kimlik Doğrulama")
        st.success("✅ Admin Yetkileri Aktif")
    
    with col2:
        st.info("✅ Kullanıcılar sadece kendi verilerini görür")
        st.info("✅ Normal kullanıcılar sadece rapor oluşturur")
        st.info("✅ Rapor türü oluşturma sadece admin'e özel")
    
    st.markdown("### 📊 Sistem Bilgileri")
    col1, col2 = st.columns(2)
    
    with col1:
        st.code(f"👤 Kullanıcı: {st.session_state.user_id}")
        st.code(f"🔑 Yetki: {st.session_state.user_type}")
        st.code(f"📅 Giriş: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    with col2:
        st.code(f"🗂️ Veri Anahtarı: {get_user_data_key()}")
        st.code(f"📋 Rapor Türü: {len(user_data['report_types'])}")
        st.code(f"🔒 Güvenlik: SHA-256")
    
    st.markdown("### 🧹 Veri Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Tüm Rapor Türlerini Sil"):
            user_data['report_types'] = {}
            st.success("✅ Rapor türleri temizlendi")
    
    with col2:
        if st.button("🔄 Mevcut Rapor Oturumunu Sıfırla"):
            user_data['current_questions'] = []
            user_data['current_answers'] = []
            st.success("✅ Oturum sıfırlandı")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()