import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# --- 1. CONFIG & STYLING ---
st.set_page_config(
    page_title="Career Analytics Hub",
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

def main():
    st.title("🎓 Student Career Hub (Decoupled)")
    
    # Sidebar Inputs
    with st.sidebar:
        st.header("Profile")
        gender = st.selectbox("Gender", ["Male", "Female"])
        cgpa = st.slider("CGPA", 0.0, 10.0, 8.5)
        ssc_p = st.number_input("SSC %", 0.0, 100.0, 80.0)
        hsc_p = st.number_input("HSC %", 0.0, 100.0, 80.0)
        degree_p = st.number_input("Degree %", 0.0, 100.0, 80.0)
        extra = st.radio("Extracurricular?", ["Yes", "No"])

    # Main Inputs
    col1, col2 = st.columns(2)
    with col1:
        tech_score = st.slider("Technical Skill", 0, 100, 85)
        interns = st.number_input("Internships", 0, 5, 1)
    with col2:
        soft_score = st.slider("Soft Skill", 0, 100, 80)
        certs = st.number_input("Certifications", 0, 10, 1)

    if st.button("🚀 Analyze Career"):
        payload = {
            "gender": str(gender),
            "ssc_percentage": float(ssc_p),
            "hsc_percentage": float(hsc_p),
            "degree_percentage": float(degree_p),
            "cgpa": float(cgpa),
            "entrance_exam_score": 75.0, # Sesuaikan jika ada inputnya
            "technical_skill_score": float(tech_score),
            "soft_skill_score": float(soft_score),
            "internship_count": int(interns),
            "live_projects": 2, # Sesuaikan jika ada inputnya
            "work_experience_months": 0,
            "certifications": int(certs),
            "attendance_percentage": 90.0,
            "backlogs": 0,
            "extracurricular_activities": str(extra)
        }
        
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=payload).json()
            
            if "error" in res:
                st.error(res["error"])
            else:
                st.divider()
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Placement Status", res["placement_status"])
                with c2:
                    st.metric("Est. Salary", f"{res['estimated_salary']} LPA")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}") # Ini akan memunculkan kode error aslinya di layar Streamlit

if __name__ == "__main__":
    main()