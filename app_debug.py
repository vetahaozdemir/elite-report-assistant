#!/usr/bin/env python3
"""
Debug versiyonu - API key kontrolü
"""

import streamlit as st
import os

st.set_page_config(page_title="Debug", page_icon="🔍")

st.header("🔍 API Key Debug")

# Debug bilgileri
st.subheader("🧪 Debug Info:")

# Secrets kontrolü
st.write("**Streamlit Secrets Check:**")
if hasattr(st, 'secrets'):
    st.write("✅ st.secrets mevcut")
    if "general" in st.secrets:
        st.write("✅ general section mevcut")
        if "GEMINI_API_KEY" in st.secrets["general"]:
            key = st.secrets["general"]["GEMINI_API_KEY"]
            st.write(f"✅ GEMINI_API_KEY bulundu: {key[:10]}...{key[-4:]}")
        else:
            st.write("❌ GEMINI_API_KEY general'da yok")
            st.write("Available keys:", list(st.secrets["general"].keys()) if "general" in st.secrets else "None")
    else:
        st.write("❌ general section yok")
        st.write("Available sections:", list(st.secrets.keys()) if st.secrets else "None")
else:
    st.write("❌ st.secrets mevcut değil")

# Environment variables
st.write("**Environment Variables Check:**")
env_key = os.getenv("GEMINI_API_KEY")
if env_key:
    st.write(f"✅ Environment GEMINI_API_KEY: {env_key[:10]}...{env_key[-4:]}")
else:
    st.write("❌ Environment GEMINI_API_KEY yok")

# Direkt secrets kontrolü
st.write("**Direct Secrets Access:**")
try:
    if "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        st.write(f"✅ Direct access: {key[:10]}...{key[-4:]}")
    else:
        st.write("❌ Direct access başarısız")
        st.write("Available direct keys:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "None")
except Exception as e:
    st.write(f"❌ Direct access error: {e}")

# Manual key input
st.subheader("🔧 Manual API Key Test")
manual_key = st.text_input("Enter API Key for test:", type="password")
if manual_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=manual_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Test: Say 'API working'")
        st.success(f"✅ API Test Success: {response.text}")
    except Exception as e:
        st.error(f"❌ API Test Failed: {e}")

st.subheader("💡 Secrets Format Example")
st.code("""
# Correct format in Streamlit Cloud Secrets:
[general]
GEMINI_API_KEY = "AIzaSyCYunsSkQS8MuRS6LSRf7EsRpYbosUDcuo"

# OR direct format:
GEMINI_API_KEY = "AIzaSyCYunsSkQS8MuRS6LSRf7EsRpYbosUDcuo"
""", language="toml")