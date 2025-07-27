#!/usr/bin/env python3
"""
Sosyal Hizmet Rapor Asistanı - Ultra Elite Premium Edition
"""

import streamlit as st
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from utils.chatbot import ReportChatbot
from utils import DocumentIndexer, VectorDatabase
from utils.learning_system import LearningSystem
from utils.smart_question_generator import SmartQuestionGenerator

# Çevre değişkenlerini yükle
load_dotenv()

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
    
    /* Glassmorphism ana container */
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Elite başlık */
    .elite-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .elite-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    .elite-header h1 {
        background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 30px rgba(167, 139, 250, 0.3);
    }
    
    .elite-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: 0.5rem;
    }
    
    /* Premium navigasyon */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .nav-button:hover {
        background: rgba(167, 139, 250, 0.2) !important;
        border-color: rgba(167, 139, 250, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(167, 139, 250, 0.2) !important;
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.3), rgba(6, 182, 212, 0.3)) !important;
        border-color: rgba(167, 139, 250, 0.5) !important;
        box-shadow: 0 0 30px rgba(167, 139, 250, 0.4) !important;
    }
    
    /* Elite kartlar */
    .elite-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .elite-card:hover {
        transform: translateY(-5px);
        border-color: rgba(167, 139, 250, 0.3);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(167, 139, 250, 0.2);
    }
    
    .elite-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    
    /* Metrik kartları */
    .metric-elite {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.1), rgba(6, 182, 212, 0.1));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-elite:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(167, 139, 250, 0.3);
    }
    
    .metric-elite h3 {
        color: #a78bfa;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
    }
    
    .metric-elite p {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        margin: 0.5rem 0 0 0;
    }
    
    /* Premium butonlar */
    .stButton > button {
        background: linear-gradient(135deg, #a78bfa 0%, #06b6d4 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(167, 139, 250, 0.4) !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #0891b2 100%) !important;
    }
    
    /* Elite form elemanları */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 20px rgba(167, 139, 250, 0.3) !important;
    }
    
    /* Sohbet mesajları */
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(6, 182, 212, 0.2));
        margin-left: 3rem;
        border-left: 4px solid #a78bfa;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.05);
        margin-right: 3rem;
        border-left: 4px solid #06b6d4;
    }
    
    /* İlerleme çubuğu */
    .progress-elite {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #a78bfa 0%, #06b6d4 100%) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(167, 139, 250, 0.5) !important;
    }
    
    /* Form container */
    .form-elite {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    /* Labels */
    .stMarkdown label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Success/Error mesajları */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Elite animasyonlar */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(167, 139, 250, 0.3); }
        50% { box-shadow: 0 0 30px rgba(167, 139, 250, 0.6); }
    }
    
    .glow-animation {
        animation: glow 3s ease-in-out infinite;
    }
    
    /* Floating elements */
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nav-container {
            flex-direction: column;
            align-items: center;
        }
        
        .elite-header h1 {
            font-size: 2rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #a78bfa, #06b6d4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6, #0891b2);
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Session state başlangıç değerlerini ayarla"""
    if 'api_initialized' not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.session_state.chatbot = ReportChatbot(api_key=api_key)
            st.session_state.vector_db = VectorDatabase(api_key=api_key)
            st.session_state.indexer = DocumentIndexer(st.session_state.vector_db)
            st.session_state.learning_system = LearningSystem(api_key=api_key)
            st.session_state.question_generator = SmartQuestionGenerator(api_key=api_key)
            st.session_state.api_initialized = True
        else:
            st.session_state.api_initialized = False
    
    # Rapor türleri veritabanı
    if 'report_types_db' not in st.session_state:
        st.session_state.report_types_db = load_report_types_db()
    
    # Navigasyon
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Sohbet durumu
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False

def load_report_types_db():
    """Rapor türleri veritabanını yükle"""
    db_path = Path("./data/report_types.json")
    
    if db_path.exists():
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "report_types": {},
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

def save_report_types_db(data):
    """Rapor türleri veritabanını kaydet"""
    os.makedirs("./data", exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    
    with open("./data/report_types.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_elite_header():
    """Ultra-elit başlık"""
    st.markdown("""
    <div class="elite-header floating">
        <h1>🎯 Elite Report Assistant</h1>
        <p class="elite-subtitle">AI-Powered Professional Social Service Report Generator</p>
    </div>
    """, unsafe_allow_html=True)

def show_elite_navigation():
    """Premium navigasyon menüsü"""
    pages = {
        "home": {"icon": "🏠", "label": "Dashboard", "desc": "Ana kontrol paneli"},
        "smart_types": {"icon": "🧠", "label": "Smart Types", "desc": "AI destekli rapor türleri"},
        "create_report": {"icon": "💬", "label": "Create Report", "desc": "Rapor oluşturma"},
        "archive": {"icon": "📚", "label": "Archive AI", "desc": "Akıllı arşiv yönetimi"},
        "analytics": {"icon": "📊", "label": "Analytics", "desc": "Gelişmiş analitik"}
    }
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(pages))
    
    for i, (page_key, page_info) in enumerate(pages.items()):
        with cols[i]:
            active_class = "active" if st.session_state.current_page == page_key else ""
            
            if st.button(
                f"{page_info['icon']} {page_info['label']}", 
                key=f"nav_{page_key}",
                help=page_info['desc']
            ):
                st.session_state.current_page = page_key
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_elite_dashboard():
    """Elite dashboard"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Sistem durumu metrikleri
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        api_status = "🟢" if st.session_state.api_initialized else "🔴"
        st.markdown(f"""
        <div class="metric-elite glow-animation">
            <h3>{api_status}</h3>
            <p>API Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        report_count = len(st.session_state.report_types_db.get("report_types", {}))
        st.markdown(f"""
        <div class="metric-elite">
            <h3>{report_count}</h3>
            <p>Report Types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.api_initialized:
            stats = st.session_state.vector_db.get_collection_stats()
            doc_count = stats.get('document_count', 0)
        else:
            doc_count = 0
        
        st.markdown(f"""
        <div class="metric-elite">
            <h3>{doc_count}</h3>
            <p>AI Knowledge Base</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.session_state.api_initialized:
            learning_stats = st.session_state.learning_system.get_statistics()
            feedback_count = learning_stats.get('total_feedbacks', 0)
        else:
            feedback_count = 0
        
        st.markdown(f"""
        <div class="metric-elite">
            <h3>{feedback_count}</h3>
            <p>AI Learning Data</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Hızlı başlangıç kartları
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="elite-card">
            <h3>🧠 AI-Powered Report Types</h3>
            <p>Upload your sample reports and let AI automatically generate optimized questions and report structures.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Create Smart Type", use_container_width=True):
            st.session_state.current_page = "smart_types"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="elite-card">
            <h3>💬 Intelligent Chat Interface</h3>
            <p>Create professional reports through natural conversation with context-aware AI assistance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 Start Creating", use_container_width=True):
            st.session_state.current_page = "create_report"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # API uyarısı
    if not st.session_state.api_initialized:
        st.markdown("""
        <div class="elite-card" style="border-color: #ef4444;">
            <h3>⚠️ API Configuration Required</h3>
            <p>Please configure your GEMINI_API_KEY in the .env file to enable all features.</p>
        </div>
        """, unsafe_allow_html=True)

def show_smart_types_page():
    """AI destekli rapor türleri sayfası"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🧠 AI-Powered Report Type Generator")
    
    # Mevcut rapor türleri
    report_types = st.session_state.report_types_db.get("report_types", {})
    
    if report_types:
        st.markdown("### 📋 Current Report Types")
        
        for type_id, type_data in report_types.items():
            st.markdown(f"""
            <div class="elite-card">
                <h4>📝 {type_data['name']}</h4>
                <p>{type_data['description']}</p>
                <p><strong>Questions:</strong> {len(type_data['questions'])} | <strong>Documents:</strong> {type_data.get('document_count', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Edit", key=f"edit_{type_id}"):
                    st.session_state.editing_type = type_id
                    st.rerun()
            with col2:
                if st.button("🧠 AI Optimize", key=f"optimize_{type_id}"):
                    optimize_report_type(type_id, type_data)
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{type_id}"):
                    del st.session_state.report_types_db["report_types"][type_id]
                    save_report_types_db(st.session_state.report_types_db)
                    st.success("Report type deleted!")
                    st.rerun()
    
    st.markdown("---")
    
    # AI ile yeni rapor türü oluşturma
    st.markdown("### 🤖 AI-Generated Report Type")
    
    st.markdown("""
    <div class="form-elite">
        <h4>Upload Sample Reports for AI Analysis</h4>
        <p>Upload 2-5 sample reports and AI will automatically:</p>
        <ul>
            <li>Analyze report structure and content</li>
            <li>Generate optimized questions</li>
            <li>Suggest report type name and description</li>
            <li>Create a complete report template</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload sample PDF reports:",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload 2-5 sample reports for AI analysis"
    )
    
    if uploaded_files and len(uploaded_files) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            suggested_name = st.text_input(
                "Report Type Name (optional):",
                placeholder="AI will suggest if empty"
            )
        
        with col2:
            if st.button("🧠 Generate with AI", use_container_width=True, type="primary"):
                generate_smart_report_type(uploaded_files, suggested_name)
    
    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("Please upload at least 2 sample reports for better AI analysis.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def generate_smart_report_type(uploaded_files, suggested_name):
    """AI ile rapor türü oluştur"""
    if not st.session_state.api_initialized:
        st.error("AI services not available. Please check API configuration.")
        return
    
    with st.spinner("🧠 AI is analyzing your reports..."):
        # Geçici dosyalar oluştur
        temp_paths = []
        for uploaded_file in uploaded_files:
            temp_path = f"./data/temp_ai_{uploaded_file.name}"
            os.makedirs("./data", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_paths.append(temp_path)
        
        try:
            # AI ile soru oluştur
            result = st.session_state.question_generator.generate_questions_from_pdfs(
                temp_paths, 
                suggested_name
            )
            
            if result["success"]:
                # Sonuçları göster
                st.markdown("### 🎉 AI Analysis Complete!")
                
                questions = result["questions"]
                report_type_name = result["report_type_suggestion"]
                rationale = result["question_rationale"]
                
                st.markdown(f"""
                <div class="elite-card glow-animation">
                    <h4>📝 Suggested Report Type: {report_type_name}</h4>
                    <p><strong>Generated Questions:</strong> {len(questions)}</p>
                    <p><strong>Focus Areas:</strong> {', '.join(rationale.get('focus_areas', []))}</p>
                    <p><strong>Estimated Duration:</strong> {rationale.get('target_duration', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Önerilen soruları göster
                with st.expander("📋 View Generated Questions", expanded=True):
                    for i, question in enumerate(questions, 1):
                        st.write(f"{i}. {question}")
                
                # Onay formu
                with st.form("confirm_ai_type"):
                    st.markdown("### ✅ Confirm and Save")
                    
                    final_name = st.text_input(
                        "Report Type Name:",
                        value=report_type_name
                    )
                    
                    final_description = st.text_area(
                        "Description:",
                        value=f"AI-generated report type based on {len(uploaded_files)} sample documents. "
                              f"Focuses on: {', '.join(rationale.get('focus_areas', []))}",
                        height=100
                    )
                    
                    if st.form_submit_button("💾 Save Report Type", use_container_width=True):
                        save_ai_generated_type(final_name, final_description, questions)
            else:
                st.error(f"AI analysis failed: {result['message']}")
                
        except Exception as e:
            st.error(f"AI generation error: {str(e)}")
        finally:
            # Geçici dosyaları temizle
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

def save_ai_generated_type(name, description, questions):
    """AI tarafından oluşturulan rapor türünü kaydet"""
    type_id = f"ai_type_{len(st.session_state.report_types_db['report_types']) + 1}_{int(datetime.now().timestamp())}"
    
    new_type = {
        "name": name,
        "description": description,
        "questions": questions,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "document_count": 0,
        "ai_generated": True,
        "generation_method": "smart_pdf_analysis"
    }
    
    st.session_state.report_types_db["report_types"][type_id] = new_type
    save_report_types_db(st.session_state.report_types_db)
    
    st.success(f"🎉 AI-generated report type '{name}' saved successfully!")
    st.balloons()
    st.rerun()

def optimize_report_type(type_id, type_data):
    """Mevcut rapor türünü AI ile optimize et"""
    if not st.session_state.api_initialized:
        st.error("AI services not available.")
        return
    
    # Bu rapor türü için yüklenen PDF'leri bul
    # (Bu basit versiyonda tüm PDF'leri kullanıyoruz)
    with st.spinner("🧠 AI is optimizing your report type..."):
        try:
            # Mevcut soruları ve AI önerilerini karşılaştır
            # Bu örnekte basit bir optimizasyon yapıyoruz
            st.info("🚧 AI optimization feature coming soon! This will analyze your existing reports and suggest improvements.")
            
        except Exception as e:
            st.error(f"Optimization error: {str(e)}")

def show_create_report_page():
    """Elite rapor oluşturma sayfası"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 💬 Elite Report Creator")
    
    if not st.session_state.api_initialized:
        st.markdown("""
        <div class="elite-card" style="border-color: #ef4444;">
            <h3>⚠️ AI Services Unavailable</h3>
            <p>Please configure API settings to use the report creator.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    report_types = st.session_state.report_types_db.get("report_types", {})
    
    if not report_types:
        st.markdown("""
        <div class="elite-card">
            <h3>🧠 No Report Types Available</h3>
            <p>Create your first AI-powered report type to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Create Smart Type", use_container_width=True):
            st.session_state.current_page = "smart_types"
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Rapor türü seçimi veya sohbet arayüzü
    if not st.session_state.conversation_started:
        st.markdown("### 🎯 Select Report Type")
        
        cols = st.columns(2)
        
        for i, (type_id, type_data) in enumerate(report_types.items()):
            with cols[i % 2]:
                ai_badge = "🧠 AI-Generated" if type_data.get("ai_generated", False) else "👤 Manual"
                
                st.markdown(f"""
                <div class="elite-card">
                    <h4>📋 {type_data['name']}</h4>
                    <p>{type_data['description']}</p>
                    <p><span style="color: #a78bfa;">{ai_badge}</span></p>
                    <p><strong>Questions:</strong> {len(type_data['questions'])} | <strong>Knowledge:</strong> {type_data.get('document_count', 0)} docs</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚀 Start Report", key=f"start_{type_id}", use_container_width=True):
                    start_elite_conversation(type_id, type_data)
    else:
        show_elite_chat_interface()
    
    st.markdown("</div>", unsafe_allow_html=True)

def start_elite_conversation(type_id, type_data):
    """Elite sohbeti başlat"""
    # Chatbot'a dinamik rapor türü ekle
    st.session_state.chatbot.report_types[type_id] = {
        "name": type_data["name"],
        "description": type_data["description"],
        "questions": type_data["questions"]
    }
    
    # Sohbeti başlat
    result = st.session_state.chatbot.start_conversation(type_id, st.session_state.session_id)
    
    if result["success"]:
        st.session_state.current_report_type = type_id
        st.session_state.conversation_started = True
        st.session_state.chat_history = []
        
        # İlk mesajı ekle
        st.session_state.chat_history.append({
            "message": result["message"],
            "is_user": False,
            "timestamp": datetime.now().isoformat(),
            "question_number": result["question_number"],
            "progress": result["progress"]
        })
        
        st.rerun()
    else:
        st.error(f"Error: {result['message']}")

def show_elite_chat_interface():
    """Elite sohbet arayüzü"""
    # İlerleme bilgisi
    session_status = st.session_state.chatbot.get_session_status(st.session_state.session_id)
    
    if session_status["exists"]:
        progress = session_status['progress'] / 100
        
        st.markdown(f"""
        <div class="progress-elite">
            <h4>📝 {session_status['report_name']}</h4>
            <p>Question {session_status['current_question']} of {session_status['total_questions']} • {session_status['progress']:.0f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progress)
        
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🔄 Reset", key="reset_elite"):
                reset_elite_conversation()
                st.rerun()
    
    # Sohbet geçmişi
    for chat_item in st.session_state.chat_history:
        if chat_item["is_user"]:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {chat_item["message"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI Assistant:</strong> {chat_item["message"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Kullanıcı girişi
    if session_status["exists"] and not session_status["completed"]:
        user_input = st.chat_input("Type your response...")
        
        if user_input:
            process_elite_input(user_input)
    
    elif session_status["completed"]:
        show_elite_report_results()

def process_elite_input(user_input):
    """Elite kullanıcı girişini işle"""
    # Kullanıcı mesajını ekle
    st.session_state.chat_history.append({
        "message": user_input,
        "is_user": True,
        "timestamp": datetime.now().isoformat()
    })
    
    # Cevabı işle
    result = st.session_state.chatbot.process_answer(st.session_state.session_id, user_input)
    
    if result["success"]:
        if result["completed"]:
            # Tüm sorular tamamlandı
            st.session_state.chat_history.append({
                "message": result["message"],
                "is_user": False,
                "timestamp": datetime.now().isoformat(),
                "completed": True
            })
            
            generate_elite_report()
        else:
            # Sonraki soru
            st.session_state.chat_history.append({
                "message": result["message"],
                "is_user": False,
                "timestamp": datetime.now().isoformat(),
                "question_number": result["question_number"],
                "progress": result["progress"]
            })
    else:
        st.session_state.chat_history.append({
            "message": f"❌ Error: {result['message']}",
            "is_user": False,
            "timestamp": datetime.now().isoformat()
        })
    
    st.rerun()

def generate_elite_report():
    """Elite rapor oluştur"""
    with st.spinner("🧠 AI is crafting your professional report..."):
        # Bağlam oluştur
        context = None
        if st.session_state.indexer:
            recent_answers = [item["message"] for item in st.session_state.chat_history[-5:] if item["is_user"]]
            if recent_answers:
                search_query = " ".join(recent_answers)[:200]
                search_results = st.session_state.indexer.search_documents(search_query, n_results=3)
                if search_results:
                    context = "KNOWLEDGE BASE INSIGHTS:\n\n"
                    for i, result in enumerate(search_results, 1):
                        context += f"{i}. {result['document'][:300]}...\n\n"
        
        # Rapor oluştur
        report_result = st.session_state.chatbot.generate_report(
            st.session_state.session_id,
            context,
            st.session_state.learning_system
        )
    
    if report_result["success"]:
        report_message = f"""
✨ **Professional Report Generated Successfully!**

📊 **Report Statistics:**
- 📝 Word count: {report_result['metadata']['word_count']}
- 📋 Questions answered: {report_result['metadata']['questions_answered']}
- ⏱️ Session duration: {report_result['metadata']['session_duration']}

🎯 **Your report is ready for download and review.**
"""
        
        st.session_state.chat_history.append({
            "message": report_message,
            "is_user": False,
            "timestamp": datetime.now().isoformat(),
            "report_data": report_result,
            "is_final_report": True
        })
    else:
        st.session_state.chat_history.append({
            "message": f"❌ Report generation failed: {report_result['message']}",
            "is_user": False,
            "timestamp": datetime.now().isoformat()
        })

def show_elite_report_results():
    """Elite rapor sonuçları"""
    st.markdown("""
    <div class="elite-card glow-animation">
        <h3>🎉 Report Completed Successfully!</h3>
        <p>Your professional report has been generated with AI assistance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Son mesajda rapor verisi var mı kontrol et
    if st.session_state.chat_history:
        last_item = st.session_state.chat_history[-1]
        if last_item.get("is_final_report") and "report_data" in last_item:
            report_data = last_item["report_data"]
            
            # Aksiyon butonları
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="💾 Download Report",
                    data=report_data["content"],
                    file_name=f"Elite_{report_data['metadata']['report_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("✏️ Review & Edit", use_container_width=True):
                    st.session_state.show_elite_revision = True
                    st.rerun()
            
            with col3:
                if st.button("🆕 New Report", use_container_width=True):
                    reset_elite_conversation()
                    st.rerun()
            
            # Revizyon formu
            if st.session_state.get('show_elite_revision', False):
                show_elite_revision_form(report_data)

def show_elite_revision_form(report_data):
    """Elite revizyon formu"""
    st.markdown("---")
    st.markdown("""
    <div class="form-elite">
        <h4>✏️ Professional Report Review</h4>
        <p>Review and refine your report. Your feedback helps improve AI performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("elite_revision_form"):
        revised_report = st.text_area(
            "Edit your report:",
            value=report_data["content"],
            height=400
        )
        
        col1, col2 = st.columns(2)
        with col1:
            feedback_type = st.selectbox(
                "Quality Rating:",
                ["positive", "neutral", "negative"],
                format_func=lambda x: {"positive": "👍 Excellent", "neutral": "😐 Good", "negative": "👎 Needs Improvement"}[x]
            )
        
        with col2:
            user_comments = st.text_area(
                "Improvement Suggestions:",
                placeholder="How can AI improve future reports..."
            )
        
        if st.form_submit_button("💾 Save Review", use_container_width=True):
            result = st.session_state.learning_system.save_report_feedback(
                original_report=report_data["content"],
                revised_report=revised_report,
                feedback_type=feedback_type,
                user_comments=user_comments,
                report_type=st.session_state.current_report_type
            )
            
            if result["success"]:
                st.success("✅ Review saved! AI will learn from your feedback.")
                st.download_button(
                    label="💾 Download Revised Report",
                    data=revised_report,
                    file_name=f"Revised_Elite_{report_data['metadata']['report_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                st.session_state.show_elite_revision = False

def reset_elite_conversation():
    """Elite sohbeti sıfırla"""
    st.session_state.chatbot.reset_session(st.session_state.session_id)
    st.session_state.conversation_started = False
    st.session_state.current_report_type = None
    st.session_state.chat_history = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.show_elite_revision = False

def show_archive_ai_page():
    """Elite arşiv AI sayfası"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📚 AI Archive Manager")
    
    st.markdown("""
    <div class="elite-card">
        <h4>🧠 Intelligent Document Processing</h4>
        <p>Upload documents by report type. AI will automatically process, index, and learn from your professional reports.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Implementasyon devam edecek...
    st.info("🚧 Elite Archive AI features are being finalized...")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_analytics_page():
    """Elite analitik sayfası"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📊 Advanced Analytics")
    
    st.markdown("""
    <div class="elite-card">
        <h4>📈 Performance Insights</h4>
        <p>Comprehensive analytics on your report generation patterns, AI learning progress, and system performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Implementasyon devam edecek...
    st.info("🚧 Advanced analytics dashboard coming soon...")
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Ana uygulama fonksiyonu"""
    st.set_page_config(
        page_title="Elite Report Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Elite CSS stillerini yükle
    load_elite_css()
    
    # Session state başlat
    init_session_state()
    
    # Elite header
    show_elite_header()
    
    # Elite navigation
    show_elite_navigation()
    
    # Sayfa yönlendirme
    current_page = st.session_state.current_page
    
    if current_page == "home":
        show_elite_dashboard()
    elif current_page == "smart_types":
        show_smart_types_page()
    elif current_page == "create_report":
        show_create_report_page()
    elif current_page == "archive":
        show_archive_ai_page()
    elif current_page == "analytics":
        show_analytics_page()

if __name__ == "__main__":
    main()