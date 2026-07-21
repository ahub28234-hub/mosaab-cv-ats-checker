import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_engine import ATSEngine
from file_reader import CVFileReader
from report_generator import ReportGenerator

st.set_page_config(
    page_title="Mosaab CV - ATS Checker",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    .stApp { font-family: 'Tajawal', sans-serif; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Mosaab CV - ATS Checker")
st.caption("فحص مجاني لتوافق سيرتك الذاتية مع أنظمة ATS")

uploaded_file = st.file_uploader("📁 ارفع CVك (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
job_desc = st.text_area("📝 وصف الوظيفة (اختياري)", height=100)

if uploaded_file and st.button("🔍 افحص الآن", use_container_width=True):
    with st.spinner("جاري التحليل..."):
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        reader = CVFileReader()
        file_info = reader.get_file_info(temp_path)
        cv_text, metadata = reader.read(temp_path)

        engine = ATSEngine()
        result = engine.analyze(cv_text, job_desc)

        score = result['overall_score']

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("النتيجة", f"{score}/100")
        with col2:
            st.progress(score / 100)
            st.write(f"**{result['grade']}** - {result['status']}")

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
            st.subheader("⚠️ المشاكل")
            for issue in result['all_issues'][:10]:
                icon = {"high": "🔴", "medium": "🟡", "low": "🔵", "info": "ℹ️"}.get(issue['severity'], "⚪")
                st.warning(f"{icon} {issue['issue']}\n\n💡 {issue['fix']}")

        if score < 75:
            st.info("🚀 عايز CV احترافي يتجاوز 85%؟ تواصل معنا @mosaab_cv")

        os.remove(temp_path)
