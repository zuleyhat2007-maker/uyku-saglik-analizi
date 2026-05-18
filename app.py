import os
os.system("pip install -r requirements.txt")
import streamlit as st
import joblib
import numpy as np
import base64

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Huzurlu Uyku ve Stres Analizi",
    page_icon="🌙",
    layout="centered"
)

# --- 🚀 OTURUM HAFIZASI (SAYFA GEÇİŞİ İÇİN) ---
# Kullanıcının hangi sayfada olduğunu takip eder
if 'sayfa_durumu' not in st.session_state:
    st.session_state.sayfa_durumu = "giris"

# --- YARDIMCI FONKSİYONLAR ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_resource
def model_yukle():
    return joblib.load('uyku_modeli.pkl')

# ==============================================================================
#                      1. AŞAMA: GİRİŞ (KAPAK) SAYFASI
# ==============================================================================
if st.session_state.sayfa_durumu == "giris":
    
    try:
        bin_str = get_base64_of_bin_file('arka_plan.jpg') # İlk gün batımı resmi
        st.markdown(f"""
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp, [data-testid="stMainBlockContainer"] {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.3)), url("data:image/jpg;base64,{bin_str}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            #MainMenu, footer, header {{visibility: hidden;}}
            
            /* Başlık ve Alt Başlık Stilleri */
            .main-title {{
                color: #ffffff !important;
                font-weight: 900 !important;
                text-align: center;
                margin-top: 15vh !important;
                text-shadow: 4px 4px 20px rgba(0, 0, 0, 1) !important;
                font-size: 3.5rem !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .sub-title {{
                color: #ffffff !important;
                font-weight: 600 !important;
                text-align: center;
                font-size: 1.5rem !important;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 1) !important;
                margin-top: 20px !important;
            }}
            
            /* BAŞLAT BUTONU */
            .stButton>button {{
                display: block; margin: 0 auto;
                background: linear-gradient(45deg, #ffaa00, #ff4b4b) !important;
                color: #ffffff !important;
                font-weight: bold !important;
                font-size: 1.6rem !important;
                border: none !important;
                border-radius: 50px !important;
                padding: 18px 65px !important;
                margin-top: 10vh !important;
                box-shadow: 0px 10px 40px rgba(255, 75, 75, 0.6) !important;
                cursor: pointer;
            }}
            </style>
            
            <h1 class="main-title">🌙 Giyilebilir Cihaz Sağlık Analizi</h1>
            <p class="sub-title">Doğanın Huzurunda Uyku, Stres ve Ekran Süresi Analiziniz</p>
        """, unsafe_allow_html=True)
    except:
        st.error("Kapak resmi ('arka_plan.jpg') bulunamadı.")

    # Sayfa geçiş butonu
    if st.button("Analizi Başlat ✨"):
        st.session_state.sayfa_durumu = "anket"
        st.rerun()

# ==============================================================================
#                      2. AŞAMA: ANKET (SORULAR) SAYFASI
# ==============================================================================
elif st.session_state.sayfa_durumu == "anket":
    
    try:
        model = model_yukle()
        bin_str_soru = get_base64_of_bin_file('soru_plani.jpg') # İkinci yıldızlı gece resmi
        
        st.markdown(f"""
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp, [data-testid="stMainBlockContainer"] {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("data:image/jpg;base64,{bin_str_soru}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            #MainMenu, footer, header {{visibility: hidden;}}
            
            /* Okunabilirlik Ayarları */
            label, p, span, div, .stSlider p {{
                color: #ffffff !important;
                font-weight: 700 !important;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 1) !important;
            }}
            h1 {{
                color: #ffffff !important;
                font-weight: 900 !important;
                text-align: center;
                text-shadow: 3px 3px 15px rgba(0, 0, 0, 1) !important;
            }}
            
            /* Girdi Alanları */
            .stNumberInput input, .stSelectbox div div div {{
                background-color: rgba(0, 0, 0, 0.7) !important;
                color: white !important;
                border: 2px solid #5d5dbd !important;
            }}
            
            /* Analiz Et Butonu */
            .stButton>button {{
                background: linear-gradient(45deg, #00ff87, #ffaa00) !important;
                color: #000 !important;
                font-weight: 900 !important;
                border-radius: 15px !important;
                width: 100% !important;
                padding: 15px !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Hata oluştu: {e}")

    st.markdown("<h1>📊 Sağlık Verilerinizi Giriniz</h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Cinsiyetiniz:", ["Erkek", "Kadın"])
        age = st.number_input("Yaşınız:", min_value=1, max_value=100, value=25)
        sleep_duration = st.number_input("Günlük Uyku Süresi (Saat):", min_value=1.0, max_value=24.0, value=7.0)
        quality_of_sleep = st.slider("Uyku Kaliteniz (1-10):", 1, 10, 7)
        physical_activity = st.number_input("Günlük Aktivite (Dakika):", min_value=0, max_value=480, value=45)

    with col2:
        stress_level = st.slider("Stres Seviyeniz (1-10):", 1, 10, 5)
        screen_time_label = st.selectbox(
            "Yatmadan Önce Ekran Süreniz:",
            ["Az (0 - 30 dk)", "Normal (30 - 60 dk)", "Çok Fazla (60 dk üzeri)"]
        )
        weight = st.number_input("Kilonuz (kg):", min_value=30.0, max_value=250.0, value=70.0)
        height_cm = st.number_input("Boyunuz (cm):", min_value=100, max_value=250, value=175)
        heart_rate = st.number_input("Dinlenme Nabzınız (BPM):", min_value=40, max_value=200, value=72)
        daily_steps = st.number_input("Günlük Adım Sayınız:", min_value=0, max_value=50000, value=7000)

    st.markdown("---")

    if st.button("✨ Sağlık Durumumu Analiz Et"):
        # Veri Hazırlama
        gender_val = 0 if gender == "Erkek" else 1
        height_m = height_cm / 100.0
        bmi = weight / (height_m ** 2)
        bmi_val = 0 if bmi < 25.0 else (1 if bmi < 30.0 else 2)
        
        # Ekran Süresi Mantığı (AI Katsayısı)
        mod_stres = stress_level
        mod_kalite = quality_of_sleep
        if screen_time_label == "Çok Fazla (60 dk üzeri)":
            mod_stres = min(10, stress_level + 2)
            mod_kalite = max(1, quality_of_sleep - 1)
        elif screen_time_label == "Normal (30 - 60 dk)":
            mod_stres = min(10, stress_level + 1)

        # Tahmin
        girdi = np.array([[gender_val, age, sleep_duration, mod_kalite, physical_activity, mod_stres, bmi_val, heart_rate, daily_steps]])
        tahmin = model.predict(girdi)
        
        st.subheader("📊 Analiz Sonucu:")
        st.write(f"Hesaplanan Vücut Kitle İndeksiniz (BMI): **{bmi:.1f}**")
        
        if tahmin[0] == 0:
            st.balloons()
            st.success("🎉 Risk Tespit Edilmedi. Uykunuz gayet sağlıklı!")
        elif tahmin[0] == 1:
            st.error("⚠️ İnsomni (Uykusuzluk) Riski Tespit Edildi!")
        elif tahmin[0] == 2:
            st.warning("⚠️ Uyku Apnesi Riski Tespit Edildi!")
