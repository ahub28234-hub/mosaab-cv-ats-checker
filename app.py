import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_engine import ATSEngine
from file_reader import CVFileReader

st.set_page_config(
    page_title="Mosaab CV - ATS Checker",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Mosaab CV - ATS Checker")
st.caption("فحص مجاني لتوافق سيرتك الذاتية مع أنظمة ATS")

uploaded_file = st.file_uploader("📁 ارفع CVك (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
job_desc = st.text_area("📝 وصف الوظيفة (اختياري — لتحليل أدق)", height=100)

if uploaded_file and st.button("🔍 افحص الآن", use_container_width=True):
    with st.spinner("جاري التحليل..."):
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        reader = CVFileReader()
        cv_text, metadata = reader.read(temp_path)

        engine = ATSEngine()
        result = engine.analyze(cv_text, job_desc)

        score = result['overall_score']
        grade = result['grade']

        # Color based on score
        if score >= 85:
            color = "#22c55e"
        elif score >= 70:
            color = "#3b82f6"
        elif score >= 55:
            color = "#f59e0b"
        elif score >= 40:
            color = "#ef4444"
        else:
            color = "#991b1b"

        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 56px; font-weight: 800; color: {color};">{score}</div>
            <div style="font-size: 18px; color: #666;">من 100</div>
            <div style="background: {color}; color: white; display: inline-block; padding: 8px 24px; border-radius: 20px; font-weight: bold; margin-top: 10px;">
                {grade} — {result['status']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100)

        st.subheader("📊 التفصيل")
        cols = st.columns(5)
        metrics = [
            ("الكلمات", result['breakdown']['keywords'], 35),
            ("التنسيق", result['breakdown']['format'], 25),
            ("القراءة", result['breakdown']['readability'], 20),
            ("التواصل", result['breakdown']['contact_info'], 10),
            ("الطول", result['breakdown']['length'], 10),
        ]
        for col, (name, data, max_val) in zip(cols, metrics):
            col.metric(name, f"{data['score']}/{max_val}", f"{data['percentage']}%")

        if result['all_issues']:
            st.subheader("⚠️ المشاكل المكتشفة")
            severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}
            for issue in result['all_issues'][:12]:
                icon = severity_icons.get(issue['severity'], '⚪')
                st.warning(f"{icon} **{issue['issue']}**\n\n💡 {issue['fix']}")

        if score < 75:
            st.info("🚀 عايز CV احترافي يتجاوز 85%؟ تواصل معنا @mosaab_cv")

        os.remove(temp_path)
