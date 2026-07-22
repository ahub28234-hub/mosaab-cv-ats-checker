import streamlit as st
import sys
import os
import requests
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_engine import ATSEngine
from file_reader import CVFileReader

st.set_page_config(
    page_title="Mosaab CV - ATS Checker",
    page_icon="🔍",
    layout="centered"
)

# ─── CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    .stApp { font-family: 'Tajawal', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ─── Telegram Config ───
TELEGRAM_BOT_TOKEN = "8629379332:AAHZdhDh-uwM_fgae68-Aop4rIP2XDArxkg"
TELEGRAM_CHAT_ID = "71080505"

# ─── Header ───
st.title("🔍 Mosaab CV - ATS Checker")
st.caption("فحص مجاني لتوافق سيرتك الذاتية مع أنظمة ATS")
st.markdown("---")

# ─── Lead Form ───
st.subheader("👤 معلوماتك")

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("الاسم الكامل *", placeholder="مثال: أحمد خالد", key="user_name")
with col2:
    user_contact = st.text_input("البريد أو رقم الهاتف *", placeholder="example@email.com أو 079xxxxxxx", key="user_contact")

st.markdown("""
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:10px 0;font-size:13px;color:#475569;">
    <strong>📋 الشروط والأحكام:</strong><br>
    بالضغط على "أوافق" أدناه، أقر بأنني أوافق على جمع واستخدام معلومات الاتصال الخاصة بي
    (الاسم، البريد الإلكتروني، رقم الهاتف) لأغراض تسويقية وتواصلية من قبل Mosaab CV،
    بما في ذلك إرسال عروض الخدمات والنصائح المهنية.
</div>
""", unsafe_allow_html=True)

terms_accepted = st.checkbox("أوافق على شروط الاستخدام واستخدام معلوماتي لأغراض تسويقية *", key="terms")

st.markdown("---")

# ─── CV Upload ───
st.subheader("📁 رفع السيرة الذاتية")
uploaded_file = st.file_uploader("اختر ملف (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="cv_file")

job_desc = st.text_area("📝 وصف الوظيفة (اختياري — لتحليل أدق)", height=100, key="job_desc")

# ─── Validation ───
def validate_form():
    errors = []
    if not user_name or len(user_name.strip()) < 2:
        errors.append("❌ الاسم الكامل مطلوب")
    if not user_contact or len(user_contact.strip()) < 5:
        errors.append("❌ البريد الإلكتروني أو رقم الهاتف مطلوب")
    if not terms_accepted:
        errors.append("❌ يجب الموافقة على شروط الاستخدام")
    if not uploaded_file:
        errors.append("❌ يجب رفع السيرة الذاتية")
    return errors

# ─── Send to Telegram ───
def _send_telegram_raw(chat_id, name, contact, filename, score, grade):
    """Low-level send to a specific chat_id."""
    message = f"""🎯 عميل جديد فحص CV!

👤 الاسم: {name}
📞 التواصل: {contact}
📄 الملف: {filename}
📊 النتيجة: {score}/100 ({grade})
🕐 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
        data = resp.json()
        return data.get("ok", False), data.get("description", resp.text[:200])
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except Exception as e:
        return False, str(e)


def send_telegram(name, contact, filename, score, grade):
    """
    Send notification with multiple fallbacks:
    1. Try configured CHAT_ID
    2. If chat not found, try sending to the bot itself (getMe -> id)
    3. If all fail, return False with last error
    """
    if not TELEGRAM_BOT_TOKEN:
        return False, "Telegram bot token not configured"

    # Attempt 1: configured chat_id
    ok, err = _send_telegram_raw(TELEGRAM_CHAT_ID, name, contact, filename, score, grade)
    if ok:
        return True, "Sent"

    # If chat not found, try to get bot's own chat id via getMe + getUpdates
    if "chat not found" in err.lower() or "chat_not_found" in err.lower():
        try:
            # Get bot info to find bot id
            me_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
            me_resp = requests.get(me_url, timeout=10).json()
            if me_resp.get("ok"):
                bot_id = me_resp["result"]["id"]
                # Try sending to bot itself (works if user started chat with bot)
                ok2, err2 = _send_telegram_raw(bot_id, name, contact, filename, score, grade)
                if ok2:
                    return True, "Sent (via bot self-chat)"

            # Attempt 3: try getUpdates to find any valid chat_id
            upd_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?limit=10"
            upd_resp = requests.get(upd_url, timeout=10).json()
            if upd_resp.get("ok") and upd_resp.get("result"):
                for update in upd_resp["result"]:
                    chat = update.get("message", {}).get("chat", {})
                    fallback_id = chat.get("id")
                    if fallback_id:
                        ok3, err3 = _send_telegram_raw(fallback_id, name, contact, filename, score, grade)
                        if ok3:
                            return True, "Sent (via getUpdates fallback)"
        except Exception:
            pass

    return False, err

# ─── Analyze Button ───
if st.button("🔍 افحص الآن", use_container_width=True):

    errors = validate_form()
    if errors:
        for err in errors:
            st.error(err)
        st.stop()

    with st.spinner("جاري التحليل..."):
        # Save temp file
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Read & analyze
        reader = CVFileReader()
        cv_text, metadata = reader.read(temp_path)

        engine = ATSEngine()
        result = engine.analyze(cv_text, job_desc)

        score = result['overall_score']
        grade = result['grade']

        # Send to Telegram
        success, msg = send_telegram(user_name, user_contact, uploaded_file.name, score, grade)

        if not success:
            st.warning(f"⚠️ تعذر إرسال الإشعار: {msg}")

        # Display result
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
        <div style="text-align:center;margin:20px 0;">
            <div style="font-size:56px;font-weight:800;color:{color};">{score}</div>
            <div style="font-size:18px;color:#666;">من 100</div>
            <div style="background:{color};color:white;display:inline-block;padding:8px 24px;border-radius:20px;font-weight:bold;margin-top:10px;">
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

        # CTA for low scores
        if score < 75:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#1e3a5f,#2d5a87);border-radius:16px;padding:24px;text-align:center;margin:24px 0;color:white;">
                <h3 style="margin-bottom:8px;">🚀 عايز CV احترافي يتجاوز 85%؟</h3>
                <p style="opacity:0.9;margin-bottom:16px;">نكتب لك سيرة ذاتية متوافقة 100% مع ATS — توصيل بنفس اليوم</p>
                <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
                    <a href="https://www.instagram.com/mosaab.cv/" target="_blank"
                       style="background:#E4405F;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:700;">
                        📱 Instagram
                    </a>
                    <a href="https://wa.me/962797414013" target="_blank"
                       style="background:#25D366;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:700;">
                        💬 واتساب
                    </a>
                </div>
                <p style="opacity:0.7;font-size:12px;margin-top:12px;">الأسعار تبدأ من 5 دنانير | ضمان score أعلى من 85%</p>
            </div>
            """, unsafe_allow_html=True)

        os.remove(temp_path)

st.markdown("---")
st.caption("🔍 Mosaab CV — نكتب مستقبلك المهني 🇯🇴")
