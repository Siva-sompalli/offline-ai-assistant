import streamlit as st

# ---------- IMPORTS ----------
from auth import register_user, login_user
from database import create_tables
from ai import get_ai_response
from voice_input import listen_voice
from voice_output import speak
from system_control import open_application
from history import save_history
from history_view import show_history

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Offline Neural Voice Assistant",
    layout="wide"
)

create_tables()

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.auth-card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    width: 360px;
    margin: 100px auto;
}
.stTextInput>div>div>input {
    border-radius: 8px;
    height: 38px;
    font-size: 14px;
}
.stButton>button {
    border-radius: 8px;
    height: 38px;
    font-weight: 600;
    width: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
}
.logo-title {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

# ✅ FIX FLAG
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# ---------- LOGIN ----------
if st.session_state.user_id is None:

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="logo-title">🤖 Offline Neural Voice Assistant</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(login_username, login_password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.is_admin = (login_username == "admin")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        reg_username = st.text_input("Username", key="reg_user")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password")

        uploaded_photo = st.file_uploader("Profile Photo", type=["jpg","jpeg","png"])

        if uploaded_photo:
            st.image(uploaded_photo, width=70)

        if st.button("Create Account"):
            if reg_password != confirm_password:
                st.error("Passwords do not match")
            else:
                if register_user(reg_username, reg_password):
                    st.success("Account created successfully")
                else:
                    st.error("Username already exists")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.subheader("👤 Profile")
st.sidebar.write("User ID:", st.session_state.user_id)

language = st.sidebar.selectbox(
    "Language",
    ["English", "Telugu", "Hindi"]
)

if st.sidebar.button("View History"):
    show_history(st.session_state.user_id)
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.user_id = None
    st.session_state.is_admin = False
    st.rerun()

# ---------- MAIN CHAT ----------
st.title("🤖 Offline Neural Voice Assistant")

col1, col2, col3 = st.columns([9,1,1])

# ✅ SAFE CLEAR BEFORE INPUT
if st.session_state.clear_input:
    st.session_state.input_box = ""
    st.session_state.clear_input = False

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Ask anything...",
        key="input_box",
        label_visibility="collapsed"
    )

with col2:
    mic_clicked = st.button("🎤")

with col3:
    send_clicked = st.button("➤")

# ---------- MIC ----------
if mic_clicked:
    spoken_text = listen_voice()
    st.session_state.input_box = spoken_text
    st.rerun()

# ---------- SEND ----------
if send_clicked and st.session_state.input_box.strip():

    user_input = st.session_state.input_box.strip()

    system_reply = open_application(user_input)

    if system_reply:
        reply_text = system_reply
    else:
        prompt = f"Give a short and clear answer in {language}: {user_input}"
        reply = get_ai_response(prompt)
        reply_text = reply.replace("**", "")
        save_history(st.session_state.user_id, user_input, reply_text)

    st.markdown("### 🤖 Assistant")
    st.write(reply_text)

    speak(reply_text)

    # ✅ FINAL FIX
    st.session_state.clear_input = True
    