#!/usr/bin/env python3
"""
Akıllı Sosyal Hizmet Rapor Sistemi
Minimal bilgiyle maksimal rapor üretimi
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
    page_title="Akıllı Rapor Sistemi",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kullanıcı bilgileri
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("Taha_2123652".encode()).hexdigest()

DEMO_USERS = {
    "demo": hashlib.sha256("demo123".encode()).hexdigest(),
    "user1": hashlib.sha256("user123".encode()).hexdigest()
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_smart_theme():
    """Akıllı sistem teması"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', sans-serif;
        color: #f1f5f9;
    }
    
    .smart-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2.5rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
    }
    
    .smart-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .smart-subtitle {
        color: #c7d2fe;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .smart-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border-left: 4px solid #6366f1;
    }
    
    .smart-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #1e293b;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #475569;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 600;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1e293b;
        border: 2px solid #475569;
        border-radius: 8px;
        color: #f1f5f9;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #6366f1;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #6366f1;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .login-card {
        max-width: 420px;
        margin: 2rem auto;
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        border-top: 4px solid #6366f1;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid #10b981;
        color: #a7f3d0;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid #f59e0b;
        color: #fde68a;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid #ef4444;
        color: #fca5a5;
    }
    
    .smart-progress {
        background: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #475569;
        border-left: 4px solid #6366f1;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        height: 8px;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .question-card {
        background: rgba(99, 102, 241, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #6366f1;
        margin: 1rem 0;
        border: 1px solid #475569;
    }
    
    .minimal-input {
        background: rgba(99, 102, 241, 0.05) !important;
        border: 2px dashed #6366f1 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

def authenticate_user():
    """Kullanıcı kimlik doğrulama"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="smart-header">
            <h1 class="smart-title">🧠 Akıllı Rapor Sistemi</h1>
            <p class="smart-subtitle">Minimal Bilgi → Maksimal Rapor</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Akıllı Giriş Sistemi")
        
        username = st.text_input("👤 Kullanıcı Adı")
        password = st.text_input("🔑 Şifre", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Giriş", type="primary"):
                user_hash = hash_password(password)
                
                if username == ADMIN_USERNAME and user_hash == ADMIN_PASSWORD_HASH:
                    st.session_state.authenticated = True
                    st.session_state.user_id = username
                    st.session_state.user_type = "admin"
                    st.success("✅ Admin giriş!")
                    st.rerun()
                elif username in DEMO_USERS and user_hash == DEMO_USERS[username]:
                    st.session_state.authenticated = True
                    st.session_state.user_id = username
                    st.session_state.user_type = "user"
                    st.success("✅ Kullanıcı giriş!")
                    st.rerun()
                else:
                    st.error("❌ Hatalı bilgiler")
        
        with col2:
            if st.button("👥 Demo"):
                st.session_state.authenticated = True
                st.session_state.user_id = "demo"
                st.session_state.user_type = "user"
                st.success("✅ Demo giriş!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    
    return True

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
        
        return {"text": text, "pages": len(pdf_reader.pages), "title": uploaded_file.name}
    except Exception as e:
        st.error(f"PDF işleme hatası: {str(e)}")
        return None

def create_smart_questions(model, texts, report_type_name):
    """Akıllı minimal sorular oluştur"""
    try:
        combined_text = "\n\n---\n\n".join(texts)
        
        prompt = f"""
Sen bir SÜPER ZEKİ sosyal hizmet AI'ısın. Görevin: Minimal bilgiyle maksimal rapor üretecek AKILLI sorular oluşturmak.

RAPOR ÖRNEKLERİ:
{combined_text[:5000]}...

"{report_type_name}" için SÜPER AKILLI sorular oluştur:

PRİNCİPLER:
1. HER SORU ÇOKLU BİLGİ TOPLASUN: Tek soruda 3-4 farklı bilgi alanını kapsasın
2. ÇIKARIM YAPICI: Verilen bilgiden daha fazlasını çıkarabilsin
3. MİNİMAL CEVAP: Kısa cevaplardan uzun raporlar üretebilsin
4. STRATEJİK: En kritik bilgileri en az soruyla toplasın

ÖRNEK AKILLI SORU:
❌ Kötü: "Yaşınız kaç?" + "Cinsiyetiniz?" + "Eğitim durumunuz?"
✅ İyi: "Danışanın demografik profili (yaş, cinsiyet, eğitim, meslek) ve bu faktörlerin mevcut duruma etkisi nedir?"

SORU TÜRÜ STRATEJİSİ:
- Demografik + Sosyal + Ekonomik → Tek soruda birleştir
- Problem + Neden + Etki → Tek soruda topla  
- Güçlü yanlar + Kaynaklar + Fırsatlar → Birleştir
- Geçmiş + Şimdi + Gelecek → Tek perspektif

SADECE 5-8 SÜPER AKILLI SORU OLUŞTUR. Her soru minimum 3 bilgi alanını kapsasın.

JSON yanıt:
{{
  "smart_questions": [
    "akıllı_soru_1",
    "akıllı_soru_2",
    ...
  ],
  "intelligence_strategy": "Bu soruların neden akıllı olduğu"
}}
"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("smart_questions", [])
        
        return [
            "Danışanın demografik profili (yaş, cinsiyet, eğitim, meslek) ve bu faktörlerin mevcut duruma etkisi nedir?",
            "Aile yapısı, ilişki dinamikleri ve sosyal destek ağının mevcut problemlere etkisi nasıldır?",
            "Sosyoekonomik durum, barınma koşulları ve temel ihtiyaçların karşılanma durumu nedir?",
            "Yaşanan temel problemler, kök nedenleri ve bunların birey/aileye etkisi nasıldır?",
            "Daha önce alınan hizmetler, sonuçları ve bu deneyimlerin mevcut duruma katkısı nedir?",
            "Güçlü yanlar, mevcut kaynaklar ve bu potansiyellerin nasıl kullanılabileceği nedir?",
            "Kısa ve uzun vadeli hedefler ile bunlara ulaşmak için gerekli adımlar nelerdir?"
        ]
        
    except Exception as e:
        st.error(f"Akıllı soru oluşturma hatası: {str(e)}")
        return []

def generate_smart_report(model, questions, answers, knowledge_base):
    """Minimal bilgiden maksimal rapor üret"""
    try:
        qa_pairs = "\n".join([f"S: {q}\nC: {a}\n" for q, a in zip(questions, answers) if a.strip()])
        
        prompt = f"""
Sen bir SÜPER ZEKİ sosyal hizmet AI'ısın. Minimal bilgiden maksimal, kapsamlı rapor üreteceksin.

KNOWLEDGE BASE (Referans bilgiler):
{knowledge_base[:3000]}...

MİNİMAL BİLGİLER:
{qa_pairs}

GÖREV: Bu minimal bilgilerden KAPSAMLI, UZUN, DETAYLI rapor üret.

SÜPER ZEKA STRATEJİLERİ:
1. ÇIKARIM YAP: Verilen bilgilerden mantıklı çıkarımlar yap
2. KNOWLEDGE BASE KULLAN: Referans raporlardaki patterns'ları kullan
3. SOSYAL HİZMET TEORI: Profesyonel teorik çerçeveleri uygula
4. DETAY GENIŞLET: Her bilgiyi derinlemesine analiz et
5. PROFESSIONAL YAZIM: Akademik ve uzman dil kullan

RAPOR YAPISI (HER BÖLÜM DETAYLI OLACAK):

1. YÖNETİCİ ÖZETİ
   - Ana bulgular ve kritik noktalar
   - Risk değerlendirmesi özeti
   - Öncelikli müdahale alanları

2. SOSYAL VE DEMOGRAFİK ANALİZ
   - Detaylı demografik profil
   - Sosyal çevre analizi
   - Kültürel ve toplumsal faktörler
   - Sistemik etki değerlendirmesi

3. PSİKOSOSYAL DEĞERLENDİRME
   - Psikolojik durum analizi
   - Sosyal işlevsellik değerlendirmesi
   - İlişki dinamikleri incelemesi
   - Mental sağlık faktörleri

4. PROBLEM ANALİZİ VE NEDSEL ÇERÇEVE
   - Problem tanımlaması ve kategorilendirmesi
   - Kök neden analizi
   - Etkileyen faktörler matrisi
   - Sistemik etki değerlendirmesi

5. GÜÇLÜ YANLAR VE KAYNAK DEĞERLENDİRMESİ
   - Bireysel güçlü yanlar
   - Aile ve sosyal kaynaklar
   - Toplumsal kaynaklar
   - Potansiyel fırsatlar

6. RİSK VE KORUYUCU FAKTÖRLER
   - Risk değerlendirme matrisi
   - Koruyucu faktörler analizi
   - Önleme stratejileri
   - Güvenlik planlaması

7. KAPSAMLI MÜDAHAlE PLANI
   - Kısa vadeli hedefler ve stratejiler
   - Orta vadeli müdahale planı
   - Uzun vadeli rehabilitasyon
   - Multidisipliner yaklaşım

8. İZLEME VE DEĞERLENDİRME
   - Başarı göstergeleri
   - İzleme protokolü
   - Değerlendirme kriterleri
   - Revizyon planı

9. ÖNERİLER VE SONUÇ
   - Spesifik öneriler
   - Kurumsal öneriler
   - Politika önerileri
   - Genel değerlendirme

HER BÖLÜM EN AZ 2-3 PARAGRAF OLACAK. TOPLAM 2000+ KELİME HEDEFLE.

Minimal bilgiden maksimal çıkarım yap. Professional ve akademik dil kullan.
"""
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Rapor oluşturulamadı."
    except Exception as e:
        return f"Rapor oluşturma hatası: {str(e)}"

def get_user_data_key():
    return f"user_data_{st.session_state.user_id}"

def admin_smart_types_tab(model, user_data):
    """Admin - Akıllı rapor türü oluşturma"""
    st.markdown('<div class="smart-card">', unsafe_allow_html=True)
    st.header("🧠 Süper Akıllı Rapor Türü Oluşturucu")
    st.markdown("*Minimal soru, maksimal bilgi toplama stratejisi*")
    
    st.subheader("📤 Referans Rapor Yükleme")
    uploaded_files = st.file_uploader(
        "Knowledge base için 2-5 adet örnek rapor",
        type=['pdf'],
        accept_multiple_files=True,
        help="AI bu raporları analiz ederek akıllı sorular oluşturacak"
    )
    
    report_name = st.text_input("📋 Rapor Türü Adı", placeholder="Örn: Akıllı Aile Değerlendirme")
    
    if st.button("🧠 Süper Akıllı Sorular Oluştur", type="primary"):
        if uploaded_files and report_name and len(uploaded_files) >= 2:
            with st.spinner("🤖 AI süper akıllı minimal sorular oluşturuyor..."):
                all_texts = []
                
                for uploaded_file in uploaded_files:
                    pdf_data = simple_pdf_processor(uploaded_file)
                    if pdf_data:
                        all_texts.append(pdf_data["text"])
                
                if all_texts:
                    questions = create_smart_questions(model, all_texts, report_name)
                    
                    if questions:
                        user_data['report_types'][report_name] = {
                            'questions': questions,
                            'created_at': datetime.now().isoformat(),
                            'pdf_count': len(uploaded_files),
                            'user_id': st.session_state.user_id,
                            'knowledge_base': "\n\n".join(all_texts)[:10000]  # Referans için
                        }
                        
                        st.success(f"✅ '{report_name}' oluşturuldu! {len(questions)} süper akıllı soru hazırlandı.")
                        
                        with st.expander("🧠 Oluşturulan Akıllı Sorular"):
                            for i, q in enumerate(questions, 1):
                                st.write(f"**{i}.** {q}")
                                
                        st.info("💡 Bu sorular minimal cevaplarla maksimal rapor üretecek şekilde tasarlandı!")
                    else:
                        st.error("❌ Akıllı sorular oluşturulamadı")
                else:
                    st.error("❌ PDF'lerden metin çıkarılamadı")
        else:
            st.warning("⚠️ En az 2 PDF ve rapor adı gerekli")
    
    # Mevcut rapor türleri
    if user_data['report_types']:
        st.subheader("📂 Oluşturulan Akıllı Rapor Türleri")
        for name, data in user_data['report_types'].items():
            with st.expander(f"🧠 {name} ({len(data['questions'])} akıllı soru)"):
                for i, q in enumerate(data['questions'], 1):
                    st.write(f"**{i}.** {q}")
                
                if st.button(f"🗑️ Sil", key=f"delete_{name}"):
                    del user_data['report_types'][name]
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def smart_report_creation_tab(model, user_data):
    """Akıllı rapor oluşturma"""
    st.markdown('<div class="smart-card">', unsafe_allow_html=True)
    st.header("🧠 Akıllı Rapor Oluşturma")
    st.markdown("*Minimal bilgi girişi → AI maksimal rapor üretimi*")
    
    if not user_data['report_types']:
        if st.session_state.user_type == "admin":
            st.warning("⚠️ Önce akıllı rapor türü oluşturun")
        else:
            st.warning("⚠️ Admin henüz akıllı rapor türü oluşturmamış")
    else:
        selected_type = st.selectbox(
            "🧠 Akıllı Rapor Türü Seçin",
            options=list(user_data['report_types'].keys()),
            help="Minimal sorularla maksimal rapor üretecek türü seçin"
        )
        
        if selected_type:
            questions = user_data['report_types'][selected_type]['questions']
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"🧠 Seçilen: **{selected_type}** ({len(questions)} akıllı soru)")
                st.markdown("💡 **Kısa ve öz cevaplar verin, AI detayları genişletecek!**")
            
            with col2:
                if st.button("🚀 Başlat", type="primary"):
                    user_data['current_questions'] = questions
                    user_data['current_answers'] = [""] * len(questions)
                    st.rerun()
            
            if user_data['current_questions']:
                current_q_index = len([a for a in user_data['current_answers'] if a.strip()])
                total_questions = len(user_data['current_questions'])
                
                # İlerleme
                progress = current_q_index / total_questions
                st.markdown(f"""
                <div class="smart-progress">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                        <span><strong>🧠 Akıllı İlerleme:</strong> {current_q_index}/{total_questions} soru</span>
                        <span><strong>%{progress*100:.0f}</strong></span>
                    </div>
                    <div style="background: #334155; border-radius: 4px; height: 8px;">
                        <div class="progress-bar" style="width: {progress*100}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if current_q_index < total_questions:
                    current_question = user_data['current_questions'][current_q_index]
                    
                    st.subheader(f"Akıllı Soru {current_q_index + 1}/{total_questions}")
                    
                    st.markdown(f"""
                    <div class="question-card">
                        <strong>🧠 Süper AI:</strong> {current_question}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Minimal cevap alanı
                    answer = st.text_area(
                        "💬 Kısa Cevabınız (AI detayları genişletecek):", 
                        key=f"answer_{current_q_index}", 
                        height=80,
                        placeholder="Kısa ve öz yazın. Örn: '25 yaş, erkek, lise mezunu, işsiz. Aile 4 kişi, gelir düşük.' - AI bunu genişletecek!",
                        help="Sadece temel bilgileri verin, AI profesyonel detayları ekleyecek"
                    )
                    
                    col1, col2, col3 = st.columns([1, 2, 2])
                    
                    with col1:
                        if st.button("▶️ Devam", disabled=not answer.strip()):
                            user_data['current_answers'][current_q_index] = answer
                            st.rerun()
                    
                    with col2:
                        if answer.strip():
                            word_count = len(answer.split())
                            if word_count > 20:
                                st.warning(f"⚠️ Çok uzun ({word_count} kelime). Daha kısa yazın!")
                            else:
                                st.success(f"✅ Perfect! ({word_count} kelime)")
                    
                    with col3:
                        st.markdown("**💡 İpucu:** Sadece anahtar bilgileri verin")
                
                else:
                    st.success("🎉 Tüm minimal bilgiler toplandı!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🧠 AI Süper Rapor Üret", type="primary"):
                            with st.spinner("🤖 AI minimal bilgilerinizi kapsamlı rapora dönüştürüyor..."):
                                knowledge_base = user_data['report_types'][selected_type].get('knowledge_base', '')
                                
                                report = generate_smart_report(
                                    model,
                                    user_data['current_questions'],
                                    user_data['current_answers'],
                                    knowledge_base
                                )
                                
                                st.subheader("📄 AI Süper Raporu")
                                st.markdown("*Minimal bilgilerden AI'nin ürettiği kapsamlı rapor*")
                                st.markdown("---")
                                st.markdown(report)
                                st.markdown("---")
                                
                                # İstatistikler
                                word_count = len(report.split())
                                input_words = sum(len(a.split()) for a in user_data['current_answers'] if a.strip())
                                
                                st.success(f"🎯 **AI Başarısı:** {input_words} kelime girdi → {word_count} kelime çıktı (%{(word_count/max(input_words,1)*100):.0f} genişleme)")
                                
                                # İndirme
                                report_filename = f"ai_super_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                st.download_button(
                                    "📥 Süper Raporu İndir",
                                    data=report,
                                    file_name=report_filename,
                                    mime="text/plain"
                                )
                    
                    with col2:
                        if st.button("🔄 Yeni Rapor"):
                            user_data['current_questions'] = []
                            user_data['current_answers'] = []
                            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def smart_statistics_tab(user_data):
    """Akıllı istatistikler"""
    st.markdown('<div class="smart-card">', unsafe_allow_html=True)
    
    title = "📊 Akıllı Sistem İstatistikleri" if st.session_state.user_type == "admin" else "📊 Kişisel İstatistikler"
    st.header(title)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🧠 Akıllı Rapor Türleri", len(user_data['report_types']))
    
    with col2:
        total_questions = sum(len(data['questions']) for data in user_data['report_types'].values())
        st.metric("❓ Minimal Sorular", total_questions)
    
    with col3:
        st.metric("🚀 AI Modu", "Süper Akıllı")
    
    if user_data['report_types']:
        st.subheader("📈 Akıllı Rapor Türleri")
        for name, data in user_data['report_types'].items():
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid #475569; border-left: 4px solid #6366f1;">
                <strong>🧠 {name}</strong><br>
                <small>📊 {len(data['questions'])} minimal soru • 📅 {data['created_at'][:10]} • 🤖 AI Knowledge Base aktif</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Ana uygulama"""
    load_smart_theme()
    
    if not authenticate_user():
        return
    
    user_type_text = "🧠 Süper AI Admin" if st.session_state.user_type == "admin" else "👤 Akıllı Kullanıcı"
    
    st.markdown(f"""
    <div class="smart-header">
        <h1 class="smart-title">🧠 Akıllı Rapor Sistemi</h1>
        <p class="smart-subtitle">{user_type_text} - Hoş geldin, {st.session_state.user_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Çıkış"):
            st.session_state.authenticated = False
            st.rerun()
    
    model = configure_api()
    
    user_key = get_user_data_key()
    if user_key not in st.session_state:
        st.session_state[user_key] = {
            'report_types': {},
            'current_questions': [],
            'current_answers': []
        }
    
    user_data = st.session_state[user_key]
    
    if st.session_state.user_type == "admin":
        tab1, tab2, tab3 = st.tabs(["🧠 Akıllı Rapor Türleri", "📝 Minimal → Maksimal", "📊 İstatistikler"])
        
        with tab1:
            admin_smart_types_tab(model, user_data)
    else:
        tab1, tab2 = st.tabs(["📝 Minimal → Maksimal", "📊 İstatistikler"])
    
    with tab2 if st.session_state.user_type == "admin" else tab1:
        smart_report_creation_tab(model, user_data)
    
    with tab3 if st.session_state.user_type == "admin" else tab2:
        smart_statistics_tab(user_data)

if __name__ == "__main__":
    main()