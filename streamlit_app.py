# instagram_streamlit_app.py - COMPLETE WORKING CODE (COPY PASTE)

import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, RateLimitError, ClientError
import database as db

st.set_page_config(pagetitle="YKTI RAWAT", page_icon="📱", layout="wide", initial_sidebar_state="expanded")

# YKTI RAWAT PREMIUM CSS (SAME AS YOUR FB APP)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
font-family: 'Poppins', sans-serif;
    
.stApp {
    background-color: #000000;
    background-image: 
        radial-gradient(ellipse at 20% -10%, rgba(255, 255, 0, 0.85) 0%, rgba(255, 255, 0, 0) 55%),
        radial-gradient(ellipse at 80% -10%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 55%),
        radial-gradient(ellipse at 20% -10%, rgba(0, 0, 255, 0.85) 0%, rgba(0, 0, 255, 0) 55%),
        radial-gradient(ellipse at 80% -10%, rgba(255, 0, 255, 0.85) 0%, rgba(255, 0, 255, 0) 55%);
    background-repeat: no-repeat;
    background-size: 60% 90%, 60% 90%, 60% 90%, 60% 90%;
    background-position: 18% -40%, 82% -40%, 18% -40%, 82% -40%;
    animation: discoColors 6s linear infinite;
}
@keyframes discoColors {
    0% { filter: hue-rotate(0deg); }
    20% { filter: hue-rotate(60deg); }
    40% { filter: hue-rotate(0deg); }
    60% { filter: hue-rotate(200deg); }
    80% { filter: hue-rotate(300deg); }
    100% { filter: hue-rotate(0deg); }
}
.main .block-container {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px;
    padding: 30px;
    border: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
    animation: containerPulse 3s ease-in-out infinite;
}
.main .block-container::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff0080, #00ff80, #ff00ff);
    border-radius: 22px;
    z-index: -1;
    animation: borderRotate 3s linear infinite;
    filter: blur(0.5px);
}
@keyframes borderRotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes containerPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
.main-header {
    background: rgba(255, 255, 255, 0.98) !important;
    padding: 3rem 2rem;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 3rem;
    border: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(45deg, #ffff00, #ff00ff, #00ffff, #ffff00);
    border-radius: 27px;
    z-index: -1;
    animation: headerBorder 2.5s linear infinite;
}
@keyframes headerBorder {
    0% { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(180deg) scale(1.02); }
    100% { transform: rotate(360deg) scale(1); }
}
.main-header h1 {
    background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ff00);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: 2px;
    animation: textRainbow 2s linear infinite;
}
@keyframes textRainbow {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
.main-header p {
    color: #00ffff;
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 1rem;
    animation: pulseGlow 2s ease-in-out infinite alternate;
}
@keyframes pulseGlow { from { filter: brightness(1); } to { filter: brightness(1.2); } }
.stButton > button {
    background: linear-gradient(135deg, #ff00ff 0%, #00ffff 50%, #ffff00 100%);
    background-size: 200% 200%;
    color: #000 !important;
    border: none;
    border-radius: 15px;
    padding: 1rem 2.5rem;
    font-weight: 700;
    font-size: 1.1rem;
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    animation: buttonShift 3s ease infinite;
    transition: all 0.3s ease;
}
@keyframes buttonShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton > button:hover {
    animation: none;
    background: linear-gradient(135deg, #ffff00 0%, #ff00ff 100%);
    transform: translateY(-3px) scale(1.05);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

ADMINUID = "your_instagram_admin_username_here"

# Session State
if 'loggedin' not in st.session_state: st.session_state.loggedin = False
if 'userid' not in st.session_state: st.session_state.userid = None
if 'username' not in st.session_state: st.session_state.username = None
if 'automationrunning' not in st.session_state: st.session_state.automationrunning = False
if 'logs' not in st.session_state: st.session_state.logs = []

class AutomationState:
    def __init__(self):
        self.running = False
        self.messagecount = 0
        self.logs = []
        self.messagerotationindex = 0

if 'automationstate' not in st.session_state:
    st.session_state.automationstate = AutomationState()

def log_message(msg, automationstate=None):
    timestamp = time.strftime('%H:%M:%S')
    formatted_msg = f"[{timestamp}] {msg}"
    if automationstate:
        automationstate.logs.append(formatted_msg)
    else:
        st.session_state.logs.append(formatted_msg)

def create_instagram_client():
    cl = Client()
    cl.delay_range = [8, 15]
    cl.request_timeout = 90
    cl.max_retries = 1
    ua = "Instagram 380.0.0.28.104 Android (35/14; 600dpi; 1440x3360; samsung; SM-S936B; dm5q; exynos2500; en_IN; 380000028)"
    cl.set_user_agent(ua)
    return cl

def safe_instagram_login(session_token, automationstate):
    for attempt in range(3):
        try:
            log_message(f"🔐 IG Login attempt {attempt+1}/3", automationstate)
            cl = create_instagram_client()
            cl.login_by_sessionid(session_token)
            account = cl.account_info()
            log_message(f"✅ IG Login SUCCESS: @{account.username}", automationstate)
            time.sleep(3)
            return True, cl, account.username
        except Exception as e:
            error_msg = str(e).lower()
            if "session" in error_msg or "login required" in error_msg:
                log_message("❌ IG Session expired!", automationstate)
                return False, None, None
            elif "rate limit" in error_msg:
                log_message("⏳ IG Rate limited - waiting...", automationstate)
                time.sleep(60)
            else:
                log_message(f"⚠️ IG Login error: {str(e)[:50]}", automationstate)
                time.sleep(15 * (attempt + 1))
    return False, None, None

def send_instagram_messages(config, automationstate, userid):
    session_token = config.get('session_token', '')
    group_ids = [gid.strip() for gid in config.get('chatid', '').split(',') if gid.strip()]
    messages_list = [msg.strip() for msg in config.get('messages', '').split('\n') if msg.strip()]
    delay = int(config.get('delay', 30))
    
    if not messages_list:
        messages_list = ["Hello! 🔥"]
    
    success, client, username = safe_instagram_login(session_token, automationstate)
    if not success:
        log_message("💥 IG Login failed - Bot STOPPED", automationstate)
        automationstate.running = False
        db.set_automationrunning(userid, False)
        return 0
    
    messagessent = 0
    while automationstate.running:
        for gid in group_ids:
            if not automationstate.running:
                break
            try:
                log_message(f"📱 Checking group {gid[:12]}...", automationstate)
                thread = client.direct_thread(gid)
                
                message = messages_list[automationstate.messagerotationindex % len(messages_list)]
                if config.get('nameprefix'):
                    message = f"{config.get('nameprefix')} {message}"
                
                client.direct_send(message, thread_ids=[gid])
                log_message(f"📨 IG Sent to {gid[:12]}: {message[:30]}", automationstate)
                
                automationstate.messagecount += 1
                messagessent += 1
                automationstate.messagerotationindex += 1
                
                time.sleep(delay)
            except RateLimitError:
                log_message("⏳ IG Rate limit - 2min cooldown", automationstate)
                time.sleep(120)
            except Exception as e:
                log_message(f"⚠️ IG Error {gid[:12]}: {str(e)[:40]}", automationstate)
                time.sleep(15)
        time.sleep(5)
    
    log_message(f"🛑 IG Bot stopped. Total messages: {messagessent}", automationstate)
    automationstate.running = False
    db.set_automationrunning(userid, False)
    return messagessent

def send_admin_notification(config, username, automationstate, userid):
    log_message(f"👑 ADMIN NOTIFY: {username} started IG bot", automationstate)

def run_instagram_automation(config, username, automationstate, userid):
    send_admin_notification(config, username, automationstate, userid)
    send_instagram_messages(config, automationstate, userid)

def start_automation(userconfig, userid):
    automationstate = st.session_state.automationstate
    if automationstate.running:
        return
    automationstate.running = True
    automationstate.messagecount = 0
    automationstate.logs = []
    username = db.get_username(userid)
    thread = threading.Thread(
        target=run_instagram_automation,
        args=(userconfig, username, automationstate, userid),
        daemon=True
    )
    thread.start()
    db.set_automationrunning(userid, True)

def stop_automation(userid):
    st.session_state.automationstate.running = False
    db.set_automationrunning(userid, False)

# LOGIN PAGE (SAME AS YOUR FB APP)
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>📱 YKTI RAWAT</h1>
        <p>PREMIUM INSTAGRAM DIRECT BOT</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["LOGIN", "SIGN UP"])
    
    with tab1:
        st.markdown("**WELCOME BACK!**")
        username = st.text_input("USERNAME", key="login_username", placeholder="Enter your username")
        password = st.text_input("PASSWORD", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("LOGIN", key="login_btn", use_container_width=True):
            if username and password:
                userid = db.verify_user(username, password)
                if userid:
                    st.session_state.loggedin = True
                    st.session_state.userid = userid
                    st.session_state.username = username
                    should_autostart = db.get_automationrunning(userid)
                    if should_autostart:
                        userconfig = db.get_userconfig(userid)
                        if userconfig and userconfig[0]:  # chatid
                            start_automation(userconfig, userid)
                    st.success(f"WELCOME BACK, {username.upper()}! 🚀")
                    st.rerun()
                else:
                    st.error("❌ INVALID USERNAME OR PASSWORD!")
            else:
                st.warning("⚠️ PLEASE ENTER BOTH USERNAME AND PASSWORD")
    
    with tab2:
        st.markdown("**CREATE NEW ACCOUNT**")
        new_username = st.text_input("CHOOSE USERNAME", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("CHOOSE PASSWORD", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("CONFIRM PASSWORD", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("CREATE ACCOUNT", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"{message} 👉 PLEASE LOGIN NOW!")
                    else:
                        st.error(f"{message}")
                else:
                    st.error("❌ PASSWORDS DO NOT MATCH!")
            else:
                st.warning("⚠️ PLEASE FILL ALL FIELDS")

# MAIN APP (SAME LAYOUT AS YOUR FB APP)
def main_app():
    st.markdown("""
    <div class="main-header">
        <h1>📱 YKTI RAWAT</h1>
        <p>PREMIUM INSTAGRAM DIRECT BOT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SIDEBAR
    st.sidebar.markdown("""
    <div class="sidebar-header">👤 USER DASHBOARD</div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown(f"**USERNAME**  \n{st.session_state.username}")
    st.sidebar.markdown(f"**USER ID**  \n{st.session_state.userid}")
    st.sidebar.markdown("""
    <div class="success-box">⭐ PREMIUM ACCESS</div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🔓 LOGOUT", use_container_width=True):
        if st.session_state.automationstate.running:
            stop_automation(st.session_state.userid)
        st.session_state.loggedin = False
        st.session_state.userid = None
        st.session_state.username = None
        st.session_state.automationrunning = False
        st.rerun()
    
    userconfig = db.get_userconfig(st.session_state.userid)
    if userconfig:
        tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "🤖 AUTOMATION"])
        
        with tab1:
            st.markdown('<div class="section-title">📱 INSTAGRAM CONFIGURATION</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                chatid = st.text_input(
                    "📱 Instagram Group IDs (comma separated)", 
                    value=userconfig[0] or "",
                    placeholder="e.g., 1234567890,0987654321",
                    help="Get from Instagram DM URL after /t/"
                )
                nameprefix = st.text_input(
                    "🏷️ Name Prefix", 
                    value=userconfig[1] or "",
                    placeholder="e.g., YKTI RAWAT"
                )
                delay = st.number_input(
                    "⏱️ Delay (seconds)", 
                    min_value=5, max_value=300, 
                    value=int(userconfig[2] or 30)
                )
            
            with col2:
                session_token = st.text_area(
                    "🔑 Instagram Session Token", 
                    value=db.decrypt_cookies(userconfig[3]) if userconfig[3] else "",
                    placeholder="Paste your Instagram sessionid cookie here",
                    height=150,
                    help="F12 → Application → Cookies → sessionid"
                )
                messages = st.text_area(
                    "💬 Messages (one per line)", 
                    value=userconfig[4] or "Welcome bro! 🔥\nHave fun! 🎉\nEnjoy group! 😊",
                    height=200
                )
            
            if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
                db.update_userconfig(
                    st.session_state.userid, 
                    chatid, nameprefix, delay, 
                    session_token, messages
                )
                st.success("✅ CONFIGURATION SAVED SUCCESSFULLY!")
                st.rerun()
        
        with tab2:
            st.markdown('<div class="section-title">🤖 AUTOMATION CONTROL</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📨 MESSAGES SENT", st.session_state.automationstate.messagecount)
            with col2:
                status = "🟢 RUNNING" if st.session_state.automationstate.running else "🔴 STOPPED"
                st.metric("STATUS", status)
            with col3:
                display_chatid = userconfig[0][:8] + "..." if userconfig and userconfig[0] and len(userconfig[0]) > 8 else userconfig[0] or "NOT SET"
                st.metric("CHAT ID", display_chatid)
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 START INSTAGRAM BOT", 
                           disabled=st.session_state.automationstate.running, 
                           use_container_width=True):
                    if userconfig and userconfig[0]:
                        start_automation(userconfig, st.session_state.userid)
                        st.success("🚀 INSTAGRAM BOT STARTED!")
                        st.rerun()
                    else:
                        st.error("❌ PLEASE SET GROUP IDs IN CONFIGURATION FIRST!")
            
            with col2:
                if st.button("⏹️ STOP BOT", 
                           disabled=not st.session_state.automationstate.running, 
                           use_container_width=True):
                    stop_automation(st.session_state.userid)
                    st.warning("⏹️ INSTAGRAM BOT STOPPED!")
                    st.rerun()
            
            # LIVE LOGS
            if st.session_state.automationstate.logs:
                st.markdown("**📊 LIVE CONSOLE OUTPUT**")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automationstate.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
                if st.button("🔄 REFRESH LOGS", use_container_width=True):
                    st.rerun()
            else:
                st.warning("ℹ️ NO LOGS YET. START BOT TO SEE ACTIVITY!")

# MAIN EXECUTION
if not st.session_state.loggedin:
    login_page()
else:
    main_app()

st.markdown("""
<div class="footer">
    📱 MADE WITH ❤️ BY YKTI RAWAT 2026 | PREMIUM INSTAGRAM BOT
</div>
""", unsafe_allow_html=True)
