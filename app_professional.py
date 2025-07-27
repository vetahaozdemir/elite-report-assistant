#!/usr/bin/env python3
"""
Sosyal Hizmet Rapor Sistemi - Profesyonel Versiyon
"""

import streamlit as st
import os
import uuid
import json
import tempfile
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

def load_professional_css():
    """Profesyonel ve sofistike CSS tasarımı"""
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    
    /* Ana tema - Profesyonel renk paleti */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
        font-family: 'IBM Plex Sans', sans-serif;
        color: #1e293b;
    }
    
    /* Ana başlık - Minimal ve profesyonel */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-bottom: 3px solid #0ea5e9;
    }
    
    .main-title {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Kart tasarımları - Clean ve modern */
    .professional-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .professional-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-color: #0ea5e9;
    }
    
    /* Buton tasarımları - Profesyonel */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        font-family: 'IBM Plex Sans', sans-serif;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(14, 165, 233, 0.2);
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        box-shadow: 0 4px 8px rgba(14, 165, 233, 0.3);
        transform: translateY(-1px);
    }
    
    /* Sekme tasarımları */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.25rem;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        font-weight: 500;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0ea5e9;
        color: white;
    }
    
    /* Form elemanları */
    .stTextInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    /* Metrik kartları */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Başarı mesajları */
    .stSuccess {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        color: #166534;
    }
    
    /* Uyarı mesajları */
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        color: #9a3412;
    }
    
    /* Hata mesajları */
    .stError {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        color: #dc2626;
    }
    
    /* Streamlit branding gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobil uyumlu */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        .professional-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
    
    /* İlerleme çubuğu */
    .progress-container {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #0ea5e9, #06b6d4);
        height: 8px;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    </style>
    """, unsafe_allow_html=True)

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
            st.error("❌ GEMINI_API_KEY bulunamadı. Lütfen yapılandırmanızı kontrol edin.")
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ API yapılandırma hatası: {str(e)}")
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

Lütfen bu rapor türü için 8-12 arasında soru hazırla. Sorular şu kriterlere uymalı:
- Demografik bilgilerden başlayarak detaya doğru ilerlesin
- Açık uçlu sorular olsun (detaylı yanıt gerektiren)
- Sosyal hizmet terminolojisini kullansın
- Anlaşılır ve uygulanabilir olsun
- Türkçe olsun

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
        
        # Varsayılan sorular
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

Rapor şu yapıda olmalı:
1. ÖZET
2. KİŞİSEL BİLGİLER
3. MEVCUT DURUM DEĞERLENDİRMESİ
4. SORUN TANIMLAMA
5. GÜÇLÜ YANLAR VE KAYNAKLAR
6. ÖNERİLER VE MÜDAHALE PLANI
7. SONUÇ

Profesyonel, objektif ve yapılandırılmış bir dil kullan. Türkçe yaz.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def main():
    """Ana uygulama"""
    load_professional_css()
    
    # Profesyonel başlık
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">📋 Sosyal Hizmet Rapor Sistemi</h1>
        <p class="main-subtitle">Yapay Zeka Destekli Profesyonel Rapor Oluşturma Platformu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API konfigürasyonu
    model = configure_api()
    
    # Session state başlatma
    if 'report_types' not in st.session_state:
        st.session_state.report_types = {}
    if 'current_chat' not in st.session_state:
        st.session_state.current_chat = []
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'current_answers' not in st.session_state:
        st.session_state.current_answers = []
    
    # Ana sekmeler
    tab1, tab2, tab3 = st.tabs(["🔧 Rapor Türü Yönetimi", "📝 Rapor Oluştur", "📊 İstatistikler"])
    
    with tab1:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.header("🔧 Akıllı Rapor Türü Oluşturucu")
        st.markdown("**Örnek raporlarınızı yükleyerek yapay zeka ile otomatik soru setleri oluşturun**")
        
        st.subheader("📤 Örnek Rapor Yükleme")
        uploaded_files = st.file_uploader(
            "Aynı türden 2-5 adet örnek rapor yükleyin",
            type=['pdf'],
            accept_multiple_files=True,
            help="Yapay zeka bu örnekleri analiz ederek uygun sorular oluşturacak"
        )
        
        report_name = st.text_input("📋 Rapor Türü Adı", placeholder="Örn: Aile Danışmanlığı Değerlendirme Raporu")
        
        if st.button("🤖 Yapay Zeka ile Soru Oluştur", type="primary"):
            if uploaded_files and report_name:
                with st.spinner("🔄 Dosyalar analiz ediliyor ve sorular oluşturuluyor..."):
                    all_text = ""
                    
                    # PDF'leri işle
                    for uploaded_file in uploaded_files:
                        pdf_data = simple_pdf_processor(uploaded_file)
                        if pdf_data:
                            all_text += pdf_data["text"] + "\n\n"
                    
                    if all_text:
                        # AI ile sorular oluştur
                        questions = generate_questions_from_text(model, all_text, report_name)
                        
                        if questions:
                            # Report type'ı kaydet
                            st.session_state.report_types[report_name] = {
                                'questions': questions,
                                'created_at': datetime.now().isoformat(),
                                'pdf_count': len(uploaded_files)
                            }
                            
                            st.success(f"✅ '{report_name}' başarıyla oluşturuldu! {len(questions)} adet soru hazırlandı.")
                            
                            # Soruları göster
                            st.subheader("📋 Oluşturulan Sorular:")
                            for i, q in enumerate(questions, 1):
                                st.write(f"**{i}.** {q}")
                        else:
                            st.error("❌ Dosyalardan soru oluşturulamadı")
                    else:
                        st.error("❌ PDF dosyalarından metin çıkarılamadı")
            else:
                st.warning("⚠️ Lütfen PDF dosyalarını yükleyin ve rapor adını girin")
        
        # Mevcut rapor türleri
        if st.session_state.report_types:
            st.subheader("📂 Kayıtlı Rapor Türleri")
            for name, data in st.session_state.report_types.items():
                with st.expander(f"📄 {name} ({len(data['questions'])} soru) - {data['created_at'][:10]}"):
                    for i, q in enumerate(data['questions'], 1):
                        st.write(f"**{i}.** {q}")
                    
                    if st.button(f"🗑️ {name} Sil", key=f"delete_{name}"):
                        del st.session_state.report_types[name]
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.header("📝 Akıllı Rapor Oluşturma")
        st.markdown("**Hazırladığınız soru setlerini kullanarak detaylı raporlar oluşturun**")
        
        if not st.session_state.report_types:
            st.warning("⚠️ Önce 'Rapor Türü Yönetimi' sekmesinden bir rapor türü oluşturun")
        else:
            # Rapor türü seçimi
            selected_type = st.selectbox(
                "📊 Rapor Türünü Seçin",
                options=list(st.session_state.report_types.keys()),
                help="Önceden oluşturduğunuz rapor türlerinden birini seçin"
            )
            
            if selected_type:
                questions = st.session_state.report_types[selected_type]['questions']
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info(f"📋 Seçilen rapor türü: **{selected_type}** ({len(questions)} soru)")
                with col2:
                    if st.button("🆕 Yeni Rapor Başlat", type="primary"):
                        st.session_state.current_questions = questions
                        st.session_state.current_answers = [""] * len(questions)
                        st.session_state.current_chat = []
                        st.rerun()
                
                # Soru-cevap arayüzü
                if st.session_state.current_questions:
                    current_q_index = len([a for a in st.session_state.current_answers if a.strip()])
                    total_questions = len(st.session_state.current_questions)
                    
                    # İlerleme çubuğu
                    progress = current_q_index / total_questions
                    st.markdown(f"""
                    <div class="progress-container">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span><strong>İlerleme:</strong> {current_q_index}/{total_questions} soru</span>
                            <span><strong>%{progress*100:.0f}</strong></span>
                        </div>
                        <div style="background: #e2e8f0; border-radius: 4px; height: 8px;">
                            <div class="progress-bar" style="width: {progress*100}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if current_q_index < total_questions:
                        # Mevcut soru
                        st.subheader(f"Soru {current_q_index + 1}")
                        current_question = st.session_state.current_questions[current_q_index]
                        
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
                            <strong>🤖 Sistem:</strong> {current_question}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Cevap input
                        answer = st.text_area(
                            "Yanıtınız:", 
                            key=f"answer_{current_q_index}", 
                            height=120,
                            placeholder="Lütfen detaylı bir yanıt yazın..."
                        )
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("▶️ Devam Et", disabled=not answer.strip()):
                                st.session_state.current_answers[current_q_index] = answer
                                st.rerun()
                    
                    else:
                        # Tüm sorular tamamlandı
                        st.success("✅ Tüm sorular başarıyla yanıtlandı!")
                        
                        if st.button("📄 Profesyonel Rapor Oluştur", type="primary"):
                            with st.spinner("🔄 Raporunuz hazırlanıyor..."):
                                report = generate_report(
                                    model,
                                    st.session_state.current_questions,
                                    st.session_state.current_answers
                                )
                                
                                st.subheader("📄 Oluşturulan Rapor")
                                st.markdown(report)
                                
                                # İndirme butonu
                                report_filename = f"sosyal_hizmet_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                st.download_button(
                                    "📥 Raporu İndir",
                                    data=report,
                                    file_name=report_filename,
                                    mime="text/plain"
                                )
                                
                                # Yeni rapor başlatma
                                if st.button("🔄 Yeni Rapor Başlat"):
                                    st.session_state.current_questions = []
                                    st.session_state.current_answers = []
                                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.header("📊 Sistem İstatistikleri")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📋 Rapor Türleri", len(st.session_state.report_types))
        
        with col2:
            total_questions = sum(len(data['questions']) for data in st.session_state.report_types.values())
            st.metric("❓ Toplam Soru", total_questions)
        
        with col3:
            st.metric("🤖 Sistem Durumu", "✅ Aktif")
        
        if st.session_state.report_types:
            st.subheader("📈 Rapor Türleri Detayı")
            for name, data in st.session_state.report_types.items():
                st.markdown(f"""
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                    <strong>📄 {name}</strong><br>
                    <small>Soru sayısı: {len(data['questions'])} • Oluşturma: {data['created_at'][:10]} • PDF: {data['pdf_count']} dosya</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()