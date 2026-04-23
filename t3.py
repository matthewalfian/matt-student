import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIG & STYLING ---
st.set_page_config(
    page_title="Career Analytics Hub",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS untuk mempercantik UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD MODELS ---
@st.cache_resource
def load_all_models():
    try:
        clf = joblib.load('model_classification.pkl')
        reg = joblib.load('model_regression.pkl')
        return clf, reg
    except:
        return None, None

model_clf, model_reg = load_all_models()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎓 User Profile")
    gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
    cgpa = st.slider("CGPA (0-10)", 0.0, 10.0, 8.0, step=0.1)
    ssc_p = st.number_input("SSC %", 0.0, 100.0, 85.0)
    hsc_p = st.number_input("HSC %", 0.0, 100.0, 80.0)
    degree_p = st.number_input("Degree %", 0.0, 100.0, 75.0)
    extra = st.radio("Ekstrakurikuler?", ["Yes", "No"])

# --- MAIN CONTENT ---
st.title("Career Path Prediction")

if model_clf is None or model_reg is None:
    st.error("Model tidak ditemukan! Jalankan t2.py terlebih dahulu.")
else:
    col1, col2, col3 = st.columns(3)
    with col1: tech_skill = st.slider("Tech Score", 0, 100, 80)
    with col2: soft_skill = st.slider("Soft Score", 0, 100, 75)
    with col3: internships = st.number_input("Internships", 0, 5, 1)

    c1, c2 = st.columns(2)
    with c1: projects = st.number_input("Projects", 0, 10, 2)
    with c2: certs = st.number_input("Certifications", 0, 10, 1)

    if st.button("🚀 Analyze Career Potential"):
        # Bungkus input sesuai dengan nama kolom di B.csv
        input_df = pd.DataFrame([{
            "gender": gender,
            "ssc_percentage": ssc_p,
            "hsc_percentage": hsc_p,
            "degree_percentage": degree_p,
            "cgpa": cgpa,
            "entrance_exam_score": 75.0,
            "technical_skill_score": tech_skill,
            "soft_skill_score": soft_skill,
            "internship_count": internships,
            "live_projects": projects,
            "work_experience_months": 0,
            "certifications": certs,
            "attendance_percentage": 90.0,
            "backlogs": 0,
            "extracurricular_activities": extra
        }])

        # Prediksi langsung dari Pipeline (Encoding & Scaling otomatis)
        placed = model_clf.predict(input_df)[0]
        salary = model_reg.predict(input_df)[0]

        st.divider()
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            if placed == 1:
                st.success("### STATUS: PLACED ✅")
            else:
                st.error("### STATUS: NOT PLACED ❌")
        
        with res_col2:
            st.metric("Estimated Salary", f"{round(salary, 2)} LPA")

        # Visualization
        fig, ax = plt.subplots()
        sns.barplot(x=['Tech', 'Soft', 'Academic'], y=[tech_skill, soft_skill, cgpa*10], palette='viridis')
        st.pyplot(fig)