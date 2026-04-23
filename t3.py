import streamlit as st
import pandas as pd
import requests

# --- 1. CONFIG ---
st.set_page_config(page_title="Career Analytics Hub", layout="wide")

# Styling CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #007bff; color: white; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎓 Student Career Hub (Decoupled)")
    
    # URL dari Dev Tunnel kamu (Sudah Diupdate)
    url_api = "https://n54r6jl7-8000.asse.devtunnels.ms/predict"

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
        # Payload JSON
        payload = {
            "gender": str(gender),
            "ssc_percentage": float(ssc_p),
            "hsc_percentage": float(hsc_p),
            "degree_percentage": float(degree_p),
            "cgpa": float(cgpa),
            "entrance_exam_score": 75.0,
            "technical_skill_score": float(tech_score),
            "soft_skill_score": float(soft_score),
            "internship_count": int(interns),
            "live_projects": 2,
            "work_experience_months": 0,
            "certifications": int(certs),
            "attendance_percentage": 90.0,
            "backlogs": 0,
            "extracurricular_activities": str(extra)
        }
        
        try:
            # Mengirim request ke Backend
            with st.spinner('Menghubungi API...'):
                response = requests.post(url_api, json=payload, timeout=15)
                res = response.json()
            
            if "error" in res:
                st.error(res["error"])
            else:
                st.divider()
                c1, c2 = st.columns(2)
                with c1:
                    status = res["placement_status"]
                    if status == "Placed":
                        st.success(f"### {status} ✅")
                    else:
                        st.error(f"### {status} ❌")
                with c2:
                    st.metric("Estimated Salary", f"{res['estimated_salary']} LPA")
                    
        except Exception as e:
            st.error(f"Koneksi Gagal: {e}")
            st.info("Pastikan terminal FastAPI sedang 'Running' dan Port 8000 sudah 'Public'.")

if __name__ == "__main__":
    main()