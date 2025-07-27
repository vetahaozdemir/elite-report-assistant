#!/usr/bin/env python3
"""
Sosyal Hizmet Rapor Asistanı - Ultra Elite Cloud Edition
(Streamlit Cloud için optimize edilmiş versiyon)
"""

import streamlit as st
import os
import uuid
import json
import tempfile
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="Elite Report Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_elite_css():
    """Ultra-elit CSS stilleri + PWA özellikleri"""
    
    # PWA Manifest
    st.markdown("""
    <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIkVsaXRlIFJhcG9yIEFzaXN0YW7EsSIsCiAgInNob3J0X25hbWUiOiAiRWxpdGVSZXBvcnQiLAogICJkZXNjcmlwdGlvbiI6ICJBSS1Qb3dlcmVkIFNvc3lhbCBIaXptZXQgUmFwb3IgQXNpc3RhbsSxIiwKICAic3RhcnRfdXJsIjogIi8iLAogICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICJiYWNrZ3JvdW5kX2NvbG9yIjogIiMwZjBmMjMiLAogICJ0aGVtZV9jb2xvciI6ICIjYTc4YmZhIiwKICAiaWNvbnMiOiBbCiAgICB7CiAgICAgICJzcmMiOiAiZGF0YTppbWFnZS9zdmcreG1sO2Jhc2U2NCxQSE4yWnlCM2FXUjBhRDBpTWpBd0lpQm9aV2xuYUhROUlqSXdNQ0lpSUhabGNuTnBiMjQ5SWpFdU1TSWdlRzFzYm5NOUltaDBkSEE2TDI5M2R5NTNNeTV2Y21jdk1qQXdNQzl6ZG1jaVBnbzhjbVZqZENCM2FXUjBhRDBpTWpBd0lpQm9aV2xuYUhROUlqSXdNQ0lpSUdacGJHdzlJaU5oTnpoaVptRWlMejRLUEM5emRtYysiLAogICAgICAic2l6ZXMiOiAiMTkyeDE5MiIsCiAgICAgICJ0eXBlIjogImltYWdlL3N2Zyt4bWwiCiAgICB9CiAgXQp9" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Ana tema - Premium Dark */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Elite başlık */
    .elite-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #a78bfa, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px #a78bfa); }
        to { filter: drop-shadow(0 0 30px #06b6d4); }
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(167, 139, 250, 0.3);
    }
    
    /* Premium buttons */
    .stButton > button {
        background: linear-gradient(135deg, #a78bfa, #06b6d4);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(167, 139, 250, 0.6);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 15, 35, 0.9);
        backdrop-filter: blur(20px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

def configure_api():
    """API konfigürasyonu"""
    try:
        # Streamlit secrets'dan API key al - doğru format
        api_key = None
        
        # General section'dan API key al
        if "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
            api_key = st.secrets["general"]["GEMINI_API_KEY"]
        # Direct access dene
        elif "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        # Environment variable dene
        else:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            st.error("❌ GEMINI_API_KEY bulunamadı. Lütfen Streamlit Cloud secrets'ınızı kontrol edin.")
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ API konfigürasyon hatası: {str(e)}")
        st.stop()

def simple_pdf_processor(uploaded_file):
    """Basit PDF işleyici"""
    try:
        import pypdf
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # PDF'den metin çıkar
        text = ""
        with open(tmp_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Geçici dosyayı sil
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
    """Metinden soru oluştur"""
    try:
        prompt = f"""
Sen bir sosyal hizmet uzmanısın. Aşağıdaki rapor metnini analiz et ve "{report_type_name}" türü için profesyonel sorular oluştur:

RAPOR METNİ:
{text[:3000]}...

Bu rapor türü için 8-12 arasında soru oluştur. Sorular:
- Demografik bilgilerden başlayıp detaya doğru gitsin
- Açık uçlu olsun (detaylı yanıt alacak şekilde)
- Sosyal hizmet terminolojisi kullansın
- Pratik ve anlaşılır olsun

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
        
        # Fallback sorular
        return [
            "Kişi/aile hakkında temel demografik bilgileri verebilir misiniz?",
            "Mevcut yaşam koşulları ve sosyal çevre nasıl?",
            "Karşılaştığınız temel problemler nelerdir?",
            "Hangi konularda desteğe ihtiyaç duyuyorsunuz?",
            "Daha önce hangi hizmetlerden yararlandınız?",
            "Kişisel güçlü yanlarınız ve kaynaklarınız nelerdir?",
            "Kısa vadeli hedefleriniz nelerdir?",
            "Bu süreçten beklentileriniz nelerdir?"
        ]
    except Exception as e:
        st.error(f"Soru oluşturma hatası: {str(e)}")
        return []

def generate_report(model, questions, answers):
    """Rapor oluştur"""
    try:
        qa_text = "\n".join([f"S: {q}\nC: {a}\n" for q, a in zip(questions, answers)])
        
        prompt = f"""
Aşağıdaki soru-cevapları profesyonel bir sosyal hizmet raporu formatında düzenle:

{qa_text}

Rapor şu bölümleri içermeli:
1. Kişisel Bilgiler
2. Mevcut Durum
3. Sorun Tanımı
4. Güçlü Yanlar
5. Öneriler
6. Sonuç

Profesyonel, açık ve objektif bir dil kullan.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def main():
    """Ana uygulama"""
    load_elite_css()
    
    # Elite başlık
    st.markdown('<h1 class="elite-header">🎯 Elite Report Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #a78bfa; font-size: 1.2rem; margin-bottom: 2rem;">AI-Powered Social Service Report System</p>', unsafe_allow_html=True)
    
    # API konfigürasyonu
    model = configure_api()
    
    # Session state initialization
    if 'report_types' not in st.session_state:
        st.session_state.report_types = {}
    if 'current_chat' not in st.session_state:
        st.session_state.current_chat = []
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'current_answers' not in st.session_state:
        st.session_state.current_answers = []
    
    # Ana sekmeler
    tab1, tab2, tab3 = st.tabs(["🧠 Smart Types", "💬 Create Report", "📊 Analytics"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🧠 AI-Powered Report Type Creator")
        
        st.subheader("📤 Upload PDF Samples")
        uploaded_files = st.file_uploader(
            "Upload 2-5 sample reports (same type)",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload sample reports of the same type for AI analysis"
        )
        
        report_name = st.text_input("📝 Report Type Name", placeholder="e.g., Family Assessment Report")
        
        if st.button("🧠 Generate with AI", type="primary"):
            if uploaded_files and report_name:
                with st.spinner("🤖 AI analyzing PDFs and generating questions..."):
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
                            
                            st.success(f"✅ '{report_name}' created with {len(questions)} AI-generated questions!")
                            
                            # Soruları göster
                            st.subheader("📋 Generated Questions:")
                            for i, q in enumerate(questions, 1):
                                st.write(f"{i}. {q}")
                        else:
                            st.error("❌ Could not generate questions from PDFs")
                    else:
                        st.error("❌ Could not extract text from PDFs")
            else:
                st.warning("⚠️ Please upload PDFs and enter report name")
        
        # Mevcut report types
        if st.session_state.report_types:
            st.subheader("📋 Existing Report Types")
            for name, data in st.session_state.report_types.items():
                with st.expander(f"📄 {name} ({len(data['questions'])} questions)"):
                    for i, q in enumerate(data['questions'], 1):
                        st.write(f"{i}. {q}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("💬 Intelligent Report Creation")
        
        if not st.session_state.report_types:
            st.warning("⚠️ First create a report type in Smart Types tab")
        else:
            # Report type seçimi
            selected_type = st.selectbox(
                "📊 Select Report Type",
                options=list(st.session_state.report_types.keys())
            )
            
            if selected_type:
                questions = st.session_state.report_types[selected_type]['questions']
                
                if st.button("🚀 Start New Report", type="primary"):
                    st.session_state.current_questions = questions
                    st.session_state.current_answers = [""] * len(questions)
                    st.session_state.current_chat = []
                    st.rerun()
                
                # Chat interface
                if st.session_state.current_questions:
                    current_q_index = len([a for a in st.session_state.current_answers if a])
                    
                    if current_q_index < len(st.session_state.current_questions):
                        # Mevcut soru
                        st.subheader(f"Question {current_q_index + 1}/{len(st.session_state.current_questions)}")
                        current_question = st.session_state.current_questions[current_q_index]
                        st.write(f"**🤖 AI:** {current_question}")
                        
                        # Cevap input
                        answer = st.text_area("Your Answer:", key=f"answer_{current_q_index}", height=100)
                        
                        if st.button("➡️ Next Question", disabled=not answer.strip()):
                            st.session_state.current_answers[current_q_index] = answer
                            st.rerun()
                    
                    else:
                        # Tüm sorular cevaplandı
                        st.success("✅ All questions completed!")
                        
                        if st.button("📄 Generate Report", type="primary"):
                            with st.spinner("🤖 AI generating your professional report..."):
                                report = generate_report(
                                    model,
                                    st.session_state.current_questions,
                                    st.session_state.current_answers
                                )
                                
                                st.subheader("📄 Generated Report")
                                st.markdown(report)
                                
                                # Download button
                                st.download_button(
                                    "📥 Download Report",
                                    data=report,
                                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📊 Analytics Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📋 Report Types", len(st.session_state.report_types))
        
        with col2:
            total_questions = sum(len(data['questions']) for data in st.session_state.report_types.values())
            st.metric("❓ Total Questions", total_questions)
        
        with col3:
            st.metric("🤖 AI Status", "✅ Active")
        
        if st.session_state.report_types:
            st.subheader("📈 Report Types Overview")
            for name, data in st.session_state.report_types.items():
                st.write(f"• **{name}**: {len(data['questions'])} questions (Created: {data['created_at'][:10]})")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()