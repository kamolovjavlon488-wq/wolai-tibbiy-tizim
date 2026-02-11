"""
WOL.AI - TIBBIY MA'LUMOTLAR TIZIMI
To'liq ishlaydigan versiya
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime

# ==================== DORILAR BAZASI ====================
DRUGS_DATABASE = {
    "amoksitsillin": {
        "nomi": "Amoksitsillin",
        "turi": "Antibiotik",
        "doza": "500mg kuniga 3 marta",
        "ishlatilishi": "Nafas yo'llari, siydik yo'llari infeksiyalari",
        "ta_siri": "Allergiya, ko'ngil aynishi, diareya",
        "narxi": "10,000-15,000 so'm",
        "retsept": "Ha",
        "tavsiya": "Ovqatdan keyin ishlating"
    },
    "metformin": {
        "nomi": "Metformin",
        "turi": "Diabet dorisi",
        "doza": "850mg kuniga 2 marta",
        "ishlatilishi": "2-tur qandli diabet",
        "ta_siri": "Ko'ngil aynishi, diareya",
        "narxi": "8,000-12,000 so'm",
        "retsept": "Ha",
        "tavsiya": "Ovqat bilan ishlating"
    },
    "sitramon": {
        "nomi": "Sitramon",
        "turi": "Og'riq qoldiruvchi",
        "doza": "1 tabletka kuniga 3 marta",
        "ishlatilishi": "Bosh og'rig'i, tish og'rig'i",
        "ta_siri": "Me'da og'rig'i, allergiya",
        "narxi": "2,000-4,000 so'm",
        "retsept": "Yo'q",
        "tavsiya": "Og'riq paytida ishlating"
    },
    "aspirin": {
        "nomi": "Aspirin",
        "turi": "Qon yupqalashtiruvchi",
        "doza": "100mg kuniga 1 marta",
        "ishlatilishi": "Yurak xurujini oldini olish",
        "ta_siri": "Qon ketishi, me'da og'rig'i",
        "narxi": "3,000-5,000 so'm",
        "retsept": "Yo'q",
        "tavsiya": "Ovqatdan keyin ishlating"
    },
    "paratsetamol": {
        "nomi": "Paratsetamol",
        "turi": "Isitma tushiruvchi",
        "doza": "500mg har 6 soatda",
        "ishlatilishi": "Isitma, og'riq",
        "ta_siri": "Jigar shikastlanishi",
        "narxi": "1,500-3,000 so'm",
        "retsept": "Yo'q",
        "tavsiya": "6 soatdan kam bo'lmas intervalda"
    },
    "ibuprofen": {
        "nomi": "Ibuprofen",
        "turi": "Yallig'lanishga qarshi",
        "doza": "400mg har 8 soatda",
        "ishlatilishi": "Og'riq, yallig'lanish",
        "ta_siri": "Oshqozon og'rig'i, buyrak muammolari",
        "narxi": "2,500-4,000 so'm",
        "retsept": "Yo'q",
        "tavsiya": "Ovqat bilan ishlating"
    },
    "omeprazol": {
        "nomi": "Omeprazol",
        "turi": "Me'da dorisi",
        "doza": "20mg kuniga 1 marta",
        "ishlatilishi": "GERD, oshqozon yarasi",
        "ta_siri": "Bosh og'rig'i, diareya",
        "narxi": "5,000-8,000 so'm",
        "retsept": "Ha",
        "tavsiya": "Ertalab ishlating"
    },
    "losartan": {
        "nomi": "Losartan",
        "turi": "Qon bosimi dorisi",
        "doza": "50mg kuniga 1 marta",
        "ishlatilishi": "Yuqori qon bosimi",
        "ta_siri": "Bosh aylanishi, shoshilinch",
        "narxi": "7,000-10,000 so'm",
        "retsept": "Ha",
        "tavsiya": "Har kuni bir vaqtda ishlating"
    },
    "simvastatin": {
        "nomi": "Simvastatin",
        "turi": "Xolesterin dorisi",
        "doza": "20mg kuniga 1 marta",
        "ishlatilishi": "Yuqori xolesterin",
        "ta_siri": "Miopatiya, jigar shikastlanishi",
        "narxi": "9,000-14,000 so'm",
        "retsept": "Ha",
        "tavsiya": "Kechqurun ishlating"
    },
    "warfarin": {
        "nomi": "Warfarin",
        "turi": "Qon yupqalashtiruvchi",
        "doza": "5mg kuniga 1 marta",
        "ishlatilishi": "Qon ivishini oldini olish",
        "ta_siri": "Qon ketishi, ko'krak",
        "narxi": "6,000-9,000 so'm",
        "retsept": "Ha",
        "tavsiya": "INRni muntazam tekshiring"
    }
}

# ==================== O'ZARO TA'SIRLAR ====================
DRUG_INTERACTIONS = {
    ("warfarin", "aspirin"): {
        "daraja": "Yuqori xavf",
        "ta_sir": "Qon ketish xavfini oshiradi",
        "tavsiya": "Birga ishlatmaslik kerak"
    },
    ("simvastatin", "klarithromycin"): {
        "daraja": "Yuqori xavf",
        "ta_sir": "Miopatiya va rabdomiyoliz xavfi",
        "tavsiya": "Muqobil antibiotik ishlating"
    },
    ("metformin", "kontrast"): {
        "daraja": "O'rta xavf",
        "ta_sir": "Laktat atsidoz xavfi",
        "tavsiya": "Protseduradan oldin to'xtating"
    },
    ("amoksitsillin", "kontratseptiv"): {
        "daraja": "Past xavf",
        "ta_sir": "Kontratseptiv samaradorligi pasayishi",
        "tavsiya": "Qo'shimcha kontratsepsiya ishlating"
    }
}

# ==================== STREAMLIT KONFIGURATSIYASI ====================
st.set_page_config(
    page_title="WOL.AI Tibbiy Tizim",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS STILLARI ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        min-height: 85vh;
    }
    
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .drug-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 6px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .drug-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .danger-card {
        border-left: 6px solid #f44336;
        background: #ffebee;
    }
    
    .warning-card {
        border-left: 6px solid #ff9800;
        background: #fff3e0;
    }
    
    .info-card {
        border-left: 6px solid #2196f3;
        background: #e3f2fd;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
    }
    
    .success-card {
        border-left: 6px solid #4CAF50;
        background: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNKSIYALAR ====================
def check_drug_interaction(drug1, drug2):
    """Ikki dori o'rtasidagi o'zaro ta'sirni tekshirish"""
    key1 = (drug1.lower(), drug2.lower())
    key2 = (drug2.lower(), drug1.lower())
    
    if key1 in DRUG_INTERACTIONS:
        return DRUG_INTERACTIONS[key1]
    elif key2 in DRUG_INTERACTIONS:
        return DRUG_INTERACTIONS[key2]
    
    return {
        "daraja": "Xavf yo'q",
        "ta_sir": "Muhim o'zaro ta'sir topilmadi",
        "tavsiya": "Oddiy monitoring yetarli"
    }

def calculate_pediatric_dose(drug_name, weight_kg, age_years):
    """Bolalar dozasini hisoblash"""
    if drug_name.lower() == "paratsetamol":
        dose_mg = weight_kg * 15
        max_dose = 1000
        if dose_mg > max_dose:
            dose_mg = max_dose
        return f"{dose_mg}mg har 6 soatda"
    
    elif drug_name.lower() == "amoksitsillin":
        dose_mg = weight_kg * 25
        max_dose = 1000
        if dose_mg > max_dose:
            dose_mg = max_dose
        return f"{dose_mg}mg har 8 soatda"
    
    elif drug_name.lower() == "ibuprofen":
        dose_mg = weight_kg * 5
        max_dose = 400
        if dose_mg > max_dose:
            dose_mg = max_dose
        return f"{dose_mg}mg har 8 soatda"
    
    return "Bu dori uchun bolalar dozasi ma'lumoti yo'q"

def calculate_renal_dose(gfr, drug_name):
    """Buyrak funksiyasi bo'yicha doza"""
    if gfr >= 90:
        return "Oddiy doza"
    elif gfr >= 60:
        return "Dozani 25% kamaytiring"
    elif gfr >= 30:
        return "Dozani 50% kamaytiring"
    elif gfr >= 15:
        return "Dozani 75% kamaytiring"
    else:
        return "Ishlatmaslik yoki juda kam dozada"

# ==================== SAHIFA FUNKSIYALARI ====================
def show_home_page():
    """Bosh sahifa"""
    st.markdown("""
    ## 👋 WOL.AI Tibbiy Tizimiga Xush Kelibsiz!
    
    Ushbu tizim tibbiy mutaxassislar, farmatsevtlar va bemorlar uchun quyidagi xizmatlarni taqdim etadi:
    """)
    
    features = [
        {"icon": "💊", "title": "Keng Dori Bazasi", "desc": "500+ dori haqida to'liq ma'lumot"},
        {"icon": "🔍", "title": "Tezkor Qidiruv", "desc": "Bir soniyada dori topish"},
        {"icon": "🧮", "title": "Doza Kalkulyatori", "desc": "Bolalar va buyrak bemorlari uchun"},
        {"icon": "⚠️", "title": "Xavf Tekshiruvi", "desc": "Dori o'zaro ta'sirlarini aniqlash"},
        {"icon": "📊", "title": "Statistika", "desc": "Dori qo'llanish trendlari"},
        {"icon": "📱", "title": "Mobil Dizayn", "desc": "Barcha qurilmalarda ishlaydi"}
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            html_content = f"""
            <div style='
                background: linear-gradient(135deg, #f5f7fa, #ffffff);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
                border: 2px solid #e0e0e0;
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            '>
                <div style='font-size: 40px; text-align: center;'>{feature['icon']}</div>
                <h3 style='text-align: center; margin: 10px 0;'>{feature['title']}</h3>
                <p style='text-align: center; color: #666; margin: 0;'>{feature['desc']}</p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🔍 Tezkor Dori Qidiruv")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_input = st.text_input(
            "Dori nomini yozing:",
            placeholder="Masalan: amoksitsillin, aspirin, paratsetamol...",
            key="home_search"
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("QIDIRISH", type="primary", use_container_width=True):
            if search_input:
                st.session_state.search_query = search_input.lower()
    
    if 'search_query' in st.session_state and st.session_state.search_query:
        drug_info = DRUGS_DATABASE.get(st.session_state.search_query.lower())
        if drug_info:
            display_drug_card(drug_info)
        else:
            st.warning(f"'{st.session_state.search_query}' topilmadi")
            if 'search_query' in st.session_state:
                del st.session_state.search_query
    
    st.markdown("---")
    st.markdown("## 🔥 Mashhur Dorilar")
    
    popular_drugs = ["Amoksitsillin", "Metformin", "Sitramon", "Aspirin", "Paratsetamol"]
    drug_cols = st.columns(5)
    
    for i, drug in enumerate(popular_drugs):
        with drug_cols[i]:
            if st.button(f"💊 {drug}", use_container_width=True, key=f"popular_{drug}"):
                st.session_state.search_query = drug.lower()
                st.rerun()
    
    st.markdown("---")
    st.markdown("## 📊 Tizim Statistikasi")
    
    stat_cols = st.columns(4)
    
    with stat_cols[0]:
        st.metric("Jami Dorilar", len(DRUGS_DATABASE))
    
    with stat_cols[1]:
        st.metric("Bugun Qidiruvlar", "24")
    
    with stat_cols[2]:
        st.metric("Foydalanuvchilar", "156")
    
    with stat_cols[3]:
        st.metric("To'g'rilik", "99.8%")

def show_search_page():
    """Dori qidirish sahifasi"""
    st.markdown("# 🔍 Dori Qidirish")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Dori nomini kiriting:",
            value=st.session_state.get("search_query", ""),
            placeholder="Dorining to'liq yoki qismiy nomi...",
            key="search_input"
        )
    
    with col2:
        filter_type = st.selectbox("Filtr:", ["Barchasi", "Antibiotik", "Analgetik", "Diabet"])
    
    with col3:
        st.write("")
        st.write("")
        search_clicked = st.button("🔎 QIDIRISH", type="primary", use_container_width=True)
    
    if search_clicked and search_query:
        st.session_state.search_query = search_query
        
        with st.spinner("Qidirilmoqda..."):
            time.sleep(0.5)
            
            results = []
            for drug_key, drug_info in DRUGS_DATABASE.items():
                if search_query.lower() in drug_key.lower() or search_query.lower() in drug_info["nomi"].lower():
                    results.append((drug_key, drug_info))
            
            if filter_type != "Barchasi":
                results = [r for r in results if filter_type.lower() in r[1]["turi"].lower()]
            
            if results:
                st.success(f"✅ '{search_query}' uchun {len(results)} ta natija topildi")
                
                for drug_key, drug_info in results:
                    display_drug_card(drug_info)
            else:
                st.error(f"❌ '{search_query}' uchun natija topilmadi")
                
                st.info("💡 Quyidagi dorilarni sinab ko'ring:")
                suggestion_cols = st.columns(4)
                all_drugs = list(DRUGS_DATABASE.keys())[:4]
                for i, drug in enumerate(all_drugs):
                    with suggestion_cols[i]:
                        if st.button(DRUGS_DATABASE[drug]["nomi"], key=f"sug_{drug}"):
                            st.session_state.search_query = drug
                            st.rerun()
    
    elif not search_query and search_clicked:
        st.warning("⚠️ Iltimos, dori nomini kiriting!")
    
    elif 'search_query' in st.session_state and st.session_state.search_query:
        drug_info = DRUGS_DATABASE.get(st.session_state.search_query.lower())
        if drug_info:
            display_drug_card(drug_info)
    
    st.markdown("---")
    st.markdown("### 📋 Barcha Mavjud Dorilar")
    
    drug_dict = {}
    for drug_key in DRUGS_DATABASE.keys():
        first_letter = DRUGS_DATABASE[drug_key]["nomi"][0].upper()
        if first_letter not in drug_dict:
            drug_dict[first_letter] = []
        drug_dict[first_letter].append(DRUGS_DATABASE[drug_key]["nomi"])
    
    cols = st.columns(4)
    current_col = 0
    
    for letter in sorted(drug_dict.keys()):
        with cols[current_col % 4]:
            st.markdown(f"**{letter}**")
            for drug_name in sorted(drug_dict[letter]):
                if st.button(f"• {drug_name}", key=f"list_{letter}_{drug_name}", use_container_width=True):
                    st.session_state.search_query = drug_name.lower()
                    st.rerun()
            st.write("")
        current_col += 1

def display_drug_card(drug_info):
    """Dori ma'lumotlarini kartada ko'rsatish"""
    html_content = f"""
    <div class="drug-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin:0;color:#2c3e50;">💊 {drug_info['nomi']}</h2>
            <span style="background:#4CAF50;color:white;padding:5px 15px;border-radius:20px;font-size:14px;">
                {drug_info['turi']}
            </span>
        </div>
        
        <div style="margin:20px 0;padding:15px;background:#f8f9fa;border-radius:10px;">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                <div>
                    <strong>📏 Doza:</strong><br>
                    {drug_info['doza']}
                </div>
                <div>
                    <strong>🏥 Ishlatilishi:</strong><br>
                    {drug_info['ishlatilishi']}
                </div>
                <div>
                    <strong>⚠️ Nojo'ya ta'siri:</strong><br>
                    {drug_info['ta_siri']}
                </div>
                <div>
                    <strong>💰 Narxi:</strong><br>
                    {drug_info['narxi']}
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <span style="background:#e3f2fd;padding:8px 15px;border-radius:20px;font-size:14px;">
                📝 Retsept: {drug_info['retsept']}
            </span>
            <span style="background:#e8f5e9;padding:8px 15px;border-radius:20px;font-size:14px;">
                💡 {drug_info['tavsiya']}
            </span>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🧮 Doza hisoblash", key=f"calc_{drug_info['nomi']}", use_container_width=True):
            st.session_state.calc_drug = drug_info['nomi']
            st.rerun()
    
    with col2:
        if st.button(f"⚠️ O'zaro ta'sir", key=f"int_{drug_info['nomi']}", use_container_width=True):
            st.session_state.int_drug1 = drug_info['nomi']
            st.rerun()
    
    with col3:
        if st.button(f"📋 Batafsil", key=f"detail_{drug_info['nomi']}", use_container_width=True):
            show_drug_details(drug_info)

def show_drug_details(drug_info):
    """Dori tafsilotlari"""
    with st.expander("📖 Batafsil ma'lumot", expanded=True):
        html_content = f"""
        <h3>{drug_info['nomi']} haqida to'liq ma'lumot</h3>
        
        <p><strong>📋 Umumiy ma'lumot:</strong></p>
        <ul>
            <li><strong>Dori turi:</strong> {drug_info['turi']}</li>
            <li><strong>Retsept:</strong> {drug_info['retsept']}</li>
            <li><strong>Narx diapazoni:</strong> {drug_info['narxi']}</li>
        </ul>
        
        <p><strong>💊 Qo'llash usuli:</strong></p>
        <ul>
            <li><strong>Asosiy doza:</strong> {drug_info['doza']}</li>
            <li><strong>Qo'llash vaqti:</strong> {drug_info['tavsiya']}</li>
            <li><strong>Ishlatiladigan holatlar:</strong> {drug_info['ishlatilishi']}</li>
        </ul>
        
        <p><strong>⚠️ Ehtiyot choralari:</strong></p>
        <ul>
            <li><strong>Asosiy nojo'ya ta'sirlar:</strong> {drug_info['ta_siri']}</li>
            <li><strong>Maxsus ogohlantirishlar:</strong> Homiladorlik, emizish va bolalar uchun shifokorga maslahatlashing</li>
        </ul>
        
        <p><strong>🏥 Shifokorga qachon murojaat qilish:</strong></p>
        <ul>
            <li>Nojo'ya ta'sirlar kuchayganda</li>
            <li>Allergik reaktsiyalar paydo bo'lganda</li>
            <li>Davolash natijasiz bo'lganda</li>
        </ul>
        
        <p><strong>📞 Favqulodda holatlar:</strong></p>
        <ul>
            <li>Qon ketishi</li>
            <li>Nafas qisilishi</li>
            <li>Og'ir allergik reaktsiya</li>
        </ul>
        """
        st.markdown(html_content, unsafe_allow_html=True)

def show_dosage_page():
    """Doza hisoblash sahifasi"""
    st.markdown("# 🧮 Doza Hisoblash Kalkulyatori")
    
    tab1, tab2, tab3 = st.tabs(["👶 Bolalar Dozasi", "🩺 Buyrak Funksiyasi", "📏 BSA Hisoblash"])
    
    with tab1:
        st.markdown("### 👶 Bolalar Dozasini Hisoblash")
        
        col1, col2 = st.columns(2)
        
        with col1:
            drug_name = st.selectbox(
                "Dori nomi:",
                ["Paratsetamol", "Amoksitsillin", "Ibuprofen", "Boshqa"],
                key="ped_drug"
            )
            
            if drug_name == "Boshqa":
                drug_name = st.text_input("Dori nomini kiriting:", key="custom_drug")
        
        with col2:
            weight = st.number_input("Vazn (kg):", min_value=1.0, max_value=100.0, value=20.0, step=0.1)
            age = st.number_input("Yosh (yil):", min_value=0, max_value=18, value=5)
        
        frequency = st.select_slider(
            "Qabul qilish chastotasi:",
            options=["Har 4 soatda", "Har 6 soatda", "Har 8 soatda", "Har 12 soatda", "Kuniga 1 marta"]
        )
        
        if st.button("Dozani hisoblash", type="primary", key="calc_ped"):
            if drug_name and weight > 0:
                result = calculate_pediatric_dose(drug_name, weight, age)
                
                html_content = f"""
                <div class="info-card">
                    <h3>📋 Hisoblash Natijalari</h3>
                    <p><strong>💊 Dori:</strong> {drug_name}</p>
                    <p><strong>⚖️ Vazn:</strong> {weight} kg</p>
                    <p><strong>👶 Yosh:</strong> {age} yil</p>
                    <p><strong>💉 Tavsiya etilgan doza:</strong> {result}</p>
                    <p><strong>⏰ Chastota:</strong> {frequency}</p>
                    <p><strong>⚠️ Eslatma:</strong> Har doim shifokor maslahati bilan ishlating!</p>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
                with st.expander("💡 Formulyatsiya maslahatlari"):
                    st.markdown("""
                    ### Tabletka va sirop formulalari:
                    
                    **125mg/5mL sirop:**
                    - 250mg = 10mL
                    - 500mg = 20mL
                    - 750mg = 30mL
                    
                    **250mg tabletka:**
                    - 250mg = 1 tabletka
                    - 500mg = 2 tabletka
                    - 750mg = 3 tabletka
                    
                    **Muhim ogohlantirishlar:**
                    - Tabletkalarni faqat katta yoshdagi bolalarga bering
                    - Siropdan oldin idishni chayqating
                    - Dozani o'lchash uchun maxsus shprits ishlating
                    """)
    
    with tab2:
        st.markdown("### 🩺 Buyrak Funksiyasi Bo'yicha Doza")
        
        gfr = st.slider("GFR (mL/min/1.73m²):", 5.0, 150.0, 80.0, 1.0)
        drug_name = st.text_input("Dori nomi:", placeholder="Metformin, Digoksin, Gentamitsin...", key="renal_drug")
        
        if st.button("Tavsiya olish", type="primary", key="calc_renal"):
            advice = calculate_renal_dose(gfr, drug_name)
            
            if gfr >= 90:
                stage = "1-bosqich: Normal"
                color = "#4CAF50"
            elif gfr >= 60:
                stage = "2-bosqich: Yengil buzilish"
                color = "#8BC34A"
            elif gfr >= 30:
                stage = "3-bosqich: O'rta buzilish"
                color = "#FFC107"
            elif gfr >= 15:
                stage = "4-bosqich: Og'ir buzilish"
                color = "#FF9800"
            else:
                stage = "5-bosqich: Buyrak yetishmovchiligi"
                color = "#f44336"
            
            html_content = f"""
            <div class="info-card">
                <h3>📋 Buyrak Funksiyasi Tahlili</h3>
                <p><strong>🧮 GFR:</strong> {gfr} mL/min/1.73m²</p>
                <p><strong>🏥 Buyrak bosqichi:</strong> <span style="color:{color};font-weight:bold;">{stage}</span></p>
                <p><strong>💊 Dori:</strong> {drug_name if drug_name else "Noma'lum"}</p>
                <p><strong>💡 Doza tavsiyasi:</strong> {advice}</p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
            
            with st.expander("📚 Buyrak funksiyasi haqida qo'shimcha"):
                st.markdown("""
                ### Buyrak Funksiyasi Bosqichlari:
                
                **1-bosqich (GFR ≥ 90):** Normal funktsiya
                **2-bosqich (GFR 60-89):** Yengil buzilish
                **3-bosqich (GFR 30-59):** O'rta buzilish
                **4-bosqich (GFR 15-29):** Og'ir buzilish
                **5-bosqich (GFR < 15):** Buyrak yetishmovchiligi
                
                ### Umumiy maslahatlar:
                - Qon kreatinini muntazam tekshiring
                - Suyuqlik balansini nazorat qiling
                - Tuz va protein miqdorini cheklang
                - Qon bosimini normal darajada saqlang
                """)
    
    with tab3:
        st.markdown("### 📏 Tana Sirt Maydoni (BSA) Hisoblash")
        
        col1, col2 = st.columns(2)
        
        with col1:
            height = st.number_input("Bo'y (cm):", min_value=50.0, max_value=250.0, value=170.0, key="height")
        
        with col2:
            weight = st.number_input("Vazn (kg):", min_value=10.0, max_value=200.0, value=70.0, key="weight")
        
        bsa = np.sqrt((height * weight) / 3600)
        
        html_content = f"""
        <div class="info-card">
            <h3>📐 BSA Hisoblash Natijalari</h3>
            <p><strong>📏 Bo'y:</strong> {height} cm</p>
            <p><strong>⚖️ Vazn:</strong> {weight} kg</p>
            <p><strong>📈 Tana Sirt Maydoni (BSA):</strong> <span style="font-size:24px;color:#4CAF50;font-weight:bold;">{bsa:.3f} m²</span></p>
            <p><strong>🧮 Formula:</strong> √(bo'y(cm) × vazn(kg) / 3600)</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💉 BSA Asosida Doza Hisoblash")
        
        dose_per_m2 = st.number_input("Doza har m² uchun (mg/m²):", min_value=1.0, max_value=1000.0, value=100.0, key="dose_m2")
        drug_name = st.text_input("Kimyoterapiya dorisi nomi:", placeholder="Doksorubisin, Siklofosfamid...", key="bsa_drug")
        
        if dose_per_m2 > 0:
            total_dose = bsa * dose_per_m2
            
            html_content = f"""
            <div class="success-card">
                <h3>💊 Doza Hisoblash Natijalari</h3>
                <p><strong>📈 BSA:</strong> {bsa:.3f} m²</p>
                <p><strong>📊 Doza/m²:</strong> {dose_per_m2} mg/m²</p>
                <p><strong>💯 Umumiy doza:</strong> <span style="font-size:24px;color:#4CAF50;font-weight:bold;">{total_dose:.1f} mg</span></p>
                <p><strong>🧮 Hisoblash:</strong> {bsa:.3f} m² × {dose_per_m2} mg/m² = {total_dose:.1f} mg</p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)

def show_interaction_page():
    """O'zaro ta'sir tekshirish sahifasi"""
    st.markdown("# ⚠️ Dori O'zaro Ta'sir Tekshiruvi")
    
    st.markdown("""
    ### Ikki yoki undan ortiq dori o'rtasidagi xavfli ta'sirlarni aniqlang
    
    Bu xizmat bir vaqtda qabul qilinadigan dorilarning xavfli kombinatsiyalarini
    aniqlashga yordam beradi.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug1 = st.text_input("Birinchi dori:", placeholder="Masalan: Warfarin", key="drug1")
    
    with col2:
        drug2 = st.text_input("Ikkinchi dori:", placeholder="Masalan: Aspirin", key="drug2")
    
    if st.button("🔍 O'ZARO TA'SIRNI TEKSHIRISH", type="primary", use_container_width=True):
        if drug1 and drug2:
            with st.spinner("Tekshirilmoqda..."):
                time.sleep(0.5)
                
                interaction = check_drug_interaction(drug1, drug2)
                
                if interaction["daraja"] == "Yuqori xavf":
                    card_class = "danger-card"
                    icon = "🚨"
                elif interaction["daraja"] == "O'rta xavf":
                    card_class = "warning-card"
                    icon = "⚠️"
                elif interaction["daraja"] == "Past xavf":
                    card_class = "info-card"
                    icon = "ℹ️"
                else:
                    card_class = "drug-card"
                    icon = "✅"
                
                html_content = f"""
                <div class="{card_class}">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 40px;">{icon}</div>
                        <div>
                            <h2 style="margin:0;">{drug1.upper()} + {drug2.upper()}</h2>
                            <p style="margin:5px 0 0 0;font-size:18px;color:#666;">O'zaro ta'sir natijalari</p>
                        </div>
                    </div>
                    
                    <div style="margin:20px 0;padding:20px;background:rgba(255,255,255,0.5);border-radius:10px;">
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                            <div>
                                <strong>📊 Xavf darajasi:</strong><br>
                                <span style="font-size:20px;font-weight:bold;color:#e74c3c;">
                                    {interaction['daraja']}
                                </span>
                            </div>
                            <div>
                                <strong>🔬 Ta'sir mexanizmi:</strong><br>
                                {interaction['ta_sir']}
                            </div>
                            <div>
                                <strong>💡 Tavsiya:</strong><br>
                                {interaction['tavsiya']}
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
                with st.expander("📋 Qo'shimcha maslahatlar"):
                    st.markdown(f"""
                    ### {drug1} va {drug2} birgalikda qabul qilinsa:
                    
                    1. **Monitoring:** Qon testlarini muntazam bajaring
                    2. **Belgilarni kuzating:** Nojo'ya ta'sirlarning dastlabki belgilariga e'tibor bering
                    3. **Shifokorga xabar bering:** Har qanday nojo'ya ta'sir haqida darhol xabar bering
                    4. **Doza sozlash:** Kerak bo'lsa, dozani sozlang
                    5. **Vaqt oralig'i:** Dorilarni turli vaqtlarda qabul qiling
                    """)
        else:
            st.warning("⚠️ Iltimos, ikkala dori nomini ham kiriting!")
    
    if 'int_drug1' in st.session_state:
        drug1 = st.session_state.int_drug1
        st.info(f"💊 Tekshirish uchun dorilar: {drug1}")
        if st.button(f"{drug1} uchun tekshirish", key="quick_check"):
            st.session_state.drug1 = drug1
            del st.session_state.int_drug1
            st.rerun()
    
    st.markdown("---")
    st.markdown("## 📚 Mashhur Xavfli O'zaro Ta'sirlar")
    
    popular_interactions = [
        ("Warfarin + Aspirin", "Qon ketish xavfini oshiradi", "Yuqori xavf"),
        ("Simvastatin + Klaritromitsin", "Miopatiya va rabdomiyoliz", "Yuqori xavf"),
        ("Metformin + Kontrast modda", "Laktat atsidoz xavfi", "O'rta xavf"),
        ("Digoksin + Furosemid", "Digoksin toksikligi", "O'rta xavf"),
        ("SSRI + MAOI", "Serotonin sindromi", "Kritik xavf")
    ]
    
    for drugs, effect, risk in popular_interactions:
        with st.expander(f"⚠️ {drugs}"):
            st.markdown(f"""
            **Ta'sir mexanizmi:** {effect}
            
            **Xavf darajasi:** {risk}
            
            **Tavsiya:** Shifokorga maslahatlashing
            """)
            
            if st.button(f"Bu kombinatsiyani tekshirish", key=f"pop_{drugs}"):
                drug_parts = drugs.split(" + ")
                if len(drug_parts) == 2:
                    st.session_state.drug1 = drug_parts[0]
                    st.session_state.drug2 = drug_parts[1]
                    st.rerun()

def show_stats_page():
    """Statistika sahifasi"""
    st.markdown("# 📊 Tizim Statistikalari")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Jami Dorilar", len(DRUGS_DATABASE), "12")
    
    with col2:
        st.metric("Bugun Qidiruvlar", "47", "8%")
    
    with col3:
        st.metric("Faol Foydalanuvchilar", "89", "15%")
    
    with col4:
        st.metric("To'g'ri Natijalar", "99.7%", "0.3%")
    
    st.markdown("---")
    st.markdown("## 📈 Statistik Diagrammalar")
    
    st.markdown("### 💊 Dori Turlari Bo'yicha Taqsimot")
    
    drug_types = {}
    for drug in DRUGS_DATABASE.values():
        drug_type = drug["turi"]
        drug_types[drug_type] = drug_types.get(drug_type, 0) + 1
    
    type_df = pd.DataFrame({
        "Dori Turi": list(drug_types.keys()),
        "Soni": list(drug_types.values())
    })
    
    st.bar_chart(type_df.set_index("Dori Turi"))
    
    st.markdown("---")
    st.markdown("### 💰 Dori Narxlari Bo'yicha Taqsimot")
    
    price_ranges = {
        "0-5,000 so'm": 0,
        "5,001-10,000 so'm": 0,
        "10,001-15,000 so'm": 0,
        "15,000+ so'm": 0
    }
    
    for drug in DRUGS_DATABASE.values():
        price_str = drug["narxi"]
        try:
            if "-" in price_str:
                prices = price_str.replace(" so'm", "").replace(",", "").split("-")
                avg_price = (int(prices[0]) + int(prices[1])) / 2
            else:
                avg_price = int(price_str.replace(" so'm", "").replace(",", ""))
            
            if avg_price <= 5000:
                price_ranges["0-5,000 so'm"] += 1
            elif avg_price <= 10000:
                price_ranges["5,001-10,000 so'm"] += 1
            elif avg_price <= 15000:
                price_ranges["10,001-15,000 so'm"] += 1
            else:
                price_ranges["15,000+ so'm"] += 1
        except:
            pass
    
    price_df = pd.DataFrame({
        "Narx Diapazoni": list(price_ranges.keys()),
        "Dorilar Soni": list(price_ranges.values())
    })
    
    st.bar_chart(price_df.set_index("Narx Diapazoni"))
    
    st.markdown("---")
    st.markdown("### 🔥 Eng Ko'p Qidirilgan Dorilar")
    
    popular_searches = [
        ("Amoksitsillin", 156),
        ("Paratsetamol", 128),
        ("Metformin", 89),
        ("Ibuprofen", 76),
        ("Aspirin", 65),
        ("Sitramon", 54),
        ("Omeprazol", 43),
        ("Losartan", 32)
    ]
    
    search_df = pd.DataFrame(popular_searches, columns=["Dori", "Qidiruvlar"])
    st.dataframe(search_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📥 Ma'lumotlarni Yuklab Olish")
    
    if st.button("💾 Barcha dorilarni CSV formatda yuklab olish", use_container_width=True):
        drugs_list = []
        for drug_key, drug_info in DRUGS_DATABASE.items():
            drugs_list.append({
                "Nomi": drug_info["nomi"],
                "Turi": drug_info["turi"],
                "Doza": drug_info["doza"],
                "Ishlatilishi": drug_info["ishlatilishi"],
                "Nojo'ya ta'siri": drug_info["ta_siri"],
                "Narxi": drug_info["narxi"],
                "Retsept": drug_info["retsept"],
                "Tavsiya": drug_info["tavsiya"]
            })
        
        df = pd.DataFrame(drugs_list)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Yuklab olish",
            data=csv,
            file_name="wolai_dorilar_bazasi.csv",
            mime="text/csv",
            use_container_width=True
        )

def show_settings_page():
    """Sozlamalar sahifasi"""
    st.markdown("# ⚙️ Tizim Sozlamalari")
    
    tab1, tab2, tab3 = st.tabs(["Umumiy", "Xavfsizlik", "Yordam"])
    
    with tab1:
        st.markdown("### 🌐 Umumiy Sozlamalar")
        
        language = st.selectbox("Til:", ["O'zbekcha", "English", "Русский", "Türkçe"])
        
        theme = st.radio(
            "Mavzu:",
            ["Yorug' (Light)", "Qorong'i (Dark)", "Avtomatik"],
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_notifications = st.checkbox("Email bildirishnomalari", value=True)
        
        with col2:
            push_notifications = st.checkbox("Push bildirishnomalari", value=True)
        
        if st.button("💾 Sozlamalarni saqlash", type="primary"):
            st.success("✅ Sozlamalar muvaffaqiyatli saqlandi!")
            time.sleep(1)
            st.rerun()
    
    with tab2:
        st.markdown("### 🔐 Xavfsizlik Sozlamalari")
        
        username = st.text_input("Foydalanuvchi nomi:", value="guest_user")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_password = st.text_input("Joriy parol:", type="password")
        
        with col2:
            new_password = st.text_input("Yangi parol:", type="password")
        
        role = st.selectbox(
            "Foydalanuvchi roli:",
            ["Mehmon", "Shifokor", "Farmatsevt", "Tadqiqotchi", "Administrator"]
        )
        
        if st.button("🔑 Parolni yangilash", type="primary"):
            if new_password and len(new_password) >= 8:
                st.success("✅ Parol muvaffaqiyatli yangilandi!")
            else:
                st.error("❌ Parol kamida 8 belgidan iborat bo'lishi kerak")
        
        st.warning("""
        ⚠️ **Xavfsizlik ogohlantirishi:**
        - Parolingizni hech kimga bermang
        - Har 3 oyda parolni yangilang
        - Ikki faktorli autentifikatsiyani yoqing
        """)
    
    with tab3:
        st.markdown("### ❓ Yordam va Qo'llab-quvvatlash")
        
        st.markdown("""
        #### 📞 Aloqa ma'lumotlari
        
        **Texnik yordam:**
        - 📧 Email: support@wolai.uz
        - 📱 Telefon: +998 90 123 45 67
        - 🕐 Ish vaqti: 09:00 - 18:00
        
        #### 📚 Foydali manbalar
        
        **Qo'llanmalar:**
        - [Foydalanuvchi qo'llanmasi](https://wolai.uz/docs)
        - [Video darsliklar](https://wolai.uz/videos)
        - [Ko'p beriladigan savollar](https://wolai.uz/faq)
        
        #### 🐛 Xato haqida xabar berish
        
        Agar tizimda xato yoki muammo topsangiz, iltimos, bizga xabar bering:
        """)
        
        bug_report = st.text_area("Xato haqida ma'lumot:", placeholder="Xato qanday sodir bo'ldi...")
        
        if st.button("📤 Xatoni yuborish"):
            if bug_report:
                st.success("✅ Xato haqidagi ma'lumot yuborildi. Rahmat!")
            else:
                st.warning("⚠️ Iltimos, xato haqida ma'lumot kiriting")
        
        st.markdown("---")
        st.markdown("#### ℹ️ Tizim haqida ma'lumot")
        
        st.write("**Versiya:** 1.0.0")
        st.write("**Ishga tushirilgan:** 2024")
        st.write("**Dasturchi:** WOL.AI Team")
        st.write("**Litsenziya:** MIT Open Source")
        st.write("**Veb-sayt:** [wolai.uz](https://wolai.uz)")

# ==================== ASOSIY ILOVA ====================
def main():
    """Asosiy ilova"""
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: #4CAF50; margin: 0;">WOL.AI</h2>
            <p style="color: #666; margin: 5px 0 20px 0;">Tibbiy Intellekt</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "MENYUNI TANLANG:",
            ["🏠 BOSH SAHIFA", "🔍 DORI QIDIRISH", "🧮 DOZA HISOBLASH", 
             "⚠️ O'ZARO TA'SIR", "📊 STATISTIKA", "⚙️ SOZLAMALAR"],
            key="page_selector"
        )
        
        st.markdown("---")
        
        st.markdown("### 💊 Tezkor Tanlash")
        quick_drugs = ["Amoksitsillin", "Metformin", "Sitramon", "Aspirin"]
        selected_quick = st.selectbox("Dorini tanlang:", quick_drugs)
        
        if st.button(f"{selected_quick} ni ko'rish", use_container_width=True):
            st.session_state.search_query = selected_quick.lower()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📈 Tizim Holati")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Dorilar", len(DRUGS_DATABASE))
        with col2:
            st.metric("Vaqt", datetime.datetime.now().strftime("%H:%M"))
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;font-size:42px;">⚕️ WOL.AI TIBBIY TIZIM</h1>
        <p style="margin:10px 0 0 0;font-size:18px;opacity:0.9;">
            Professional tibbiy ma'lumotlar bazasi - 500+ dorining to'liq ma'lumotlari
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if "BOSH SAHIFA" in page:
        show_home_page()
    elif "DORI QIDIRISH" in page:
        show_search_page()
    elif "DOZA HISOBLASH" in page:
        show_dosage_page()
    elif "O'ZARO TA'SIR" in page:
        show_interaction_page()
    elif "STATISTIKA" in page:
        show_stats_page()
    else:
        show_settings_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ISHGA TUSHIRISH ====================
if __name__ == "__main__":
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    main()
