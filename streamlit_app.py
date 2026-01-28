import streamlit as st
import time
import threading
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

st.set_page_config(page_title="YK TRICKS INDIA", layout="wide")

# Custom CSS - No Icons, Screenshot exact design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #2d1b69 50%, #1a0f3d 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        background: linear-gradient(135deg, #ff0080 0%, #ff6b9d 50%, #ffb3d1 100%);
        padding: 2.5rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(255,0,128,0.4);
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        inset: -3px;
        background: linear-gradient(45deg, #ff0080, #00f5ff, #ff0080);
        border-radius: 28px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 900;
        background: linear-gradient(45deg, #fff, #f0f8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 1px;
    }
    
    .input-section {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .input-section::before {
        content: '';
        position: absolute;
        inset: -3px;
        background: linear-gradient(45deg, #ff0080, #00f5ff, #ff0080);
        border-radius: 23px;
        z-index: -1;
        animation: inputBorder 4s linear infinite;
    }
    
    @keyframes inputBorder {
        0% { border-image: linear-gradient(45deg, #ff0080, #00f5ff) 1; }
        50% { border-image: linear-gradient(45deg, #00f5ff, #ff6b9d) 1; }
        100% { border-image: linear-gradient(45deg, #ff6b9d, #ff0080) 1; }
    }
    
    .cookie-tabs .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 10px;
        gap: 10px;
        border: 2px solid transparent;
    }
    
    .cookie-tabs .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .cookie-tabs .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 100%);
        color: white !important;
        border-image: linear-gradient(45deg, #ff0080, #00f5ff) 1;
        transform: scale(1.02);
    }
    
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #e1e5e9 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 50%, #ff6b9d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        height: 50px !important;
        text-transform: uppercase !important;
        box-shadow: 0 8px 25px rgba(255,0,128,0.4) !important;
    }
    
    .control-button {
        height: 45px !important;
        font-size: 1rem !important;
        margin-top: 1rem !important;
    }
    
    .logs-container {
        background: #0a0a0a !important;
        color: #00ff88 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 15px !important;
        height: 380px !important;
        font-family: 'Courier New', monospace !important;
        padding: 1.5rem !important;
        overflow-y: auto !important;
        font-size: 0.9rem !important;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(255,0,128,0.3);
        position: relative;
    }
    
    .section-title {
        color: #ff0080;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'running' not in st.session_state:
    st.session_state.running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'cookies' not in st.session_state:
    st.session_state.cookies = ""
if 'chat_ids' not in st.session_state:
    st.session_state.chat_ids = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'prefix' not in st.session_state:
    st.session_state.prefix = ""
if 'delay' not in st.session_state:
    st.session_state.delay = 5
if 'cookie_mode' not in st.session_state:
    st.session_state.cookie_mode = "single"

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]

def find_input(driver):
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    for sel in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in elements:
                if driver.execute_script("return arguments[0].contentEditable === 'true' || arguments[0].tagName === 'TEXTAREA'", el):
                    return el
        except:
            continue
    return None

def load_cookies_from_file(uploaded_file):
    """Load cookies from uploaded txt file"""
    try:
        content = uploaded_file.read().decode('utf-8')
        cookies = content.strip()
        return cookies
    except Exception as e:
        log(f"❌ Cookie file error: {str(e)}")
        return ""

def worker():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        # Add cookies
        cookies_text = st.session_state.cookies.strip()
        if cookies_text:
            log("🔑 Loading cookies...")
            for cookie_line in cookies_text.split('\n'):
                cookie_line = cookie_line.strip()
                if '=' in cookie_line and cookie_line:
                    name, value = cookie_line.split('=', 1)
                    try:
                        driver.add_cookie({
                            'name': name.strip(), 
                            'value': value.strip(), 
                            'domain': '.facebook.com'
                        })
                    except:
                        pass
        
        total = 0
        while st.session_state.running:
            for chat_id in st.session_state.chat_ids:
                if not st.session_state.running:
                    break
                
                log(f"📱 Chat: {chat_id[:15]}...")
                driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
                time.sleep(8)
                
                inp = find_input(driver)
                if not inp:
                    log("❌ Message input not found")
                    continue
                
                for msg in st.session_state.messages:
                    if not st.session_state.running:
                        break
                    
                    full_msg = f"{st.session_state.prefix} {msg}".strip() if st.session_state.prefix else msg
                    
                    # Type message
                    driver.execute_script("""
                        arguments[0].focus();
                        arguments[0].textContent = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                    """, inp, full_msg)
                    
                    time.sleep(1)
                    
                    # Send with Enter
                    driver.execute_script("""
                        arguments[0].dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true}));
                        arguments[0].dispatchEvent(new KeyboardEvent('keyup', {key: 'Enter', bubbles: true}));
                    """, inp)
                    
                    total += 1
                    st.session_state.count = total
                    log(f"✅ Sent: {full_msg[:30]}... (Total: {total})")
                    time.sleep(st.session_state.delay)
                
    except Exception as e:
        log(f"❌ Error: {str(e)[:50]}")
    finally:
        driver.quit()
        log("🔒 Browser closed")

def start():
    if st.session_state.chat_ids and st.session_state.messages:
        st.session_state.running = True
        st.session_state.count = 0
        st.session_state.logs = []
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        log("🚀 STARTED!")
    else:
        st.error("⚠️ Add Chat IDs & Messages first!")

def stop():
    st.session_state.running = False
    log("⏹️ STOPPED!")

# Header - NO ICON/LOGO
st.markdown("""
<div class="main-header">
    <h1>YK TRICKS INDIA</h1>
    <p>Messenger Auto Tool</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">🔑 Cookies</h3>', unsafe_allow_html=True)
    
    # COOKIE TABS - Single vs Multiple File
    cookie_tabs = st.tabs(["Single Cookie", "Multiple Cookies (TXT)"], key="cookie_tabs")
    
    with cookie_tabs[0]:  # Single Cookie
        st.session_state.cookies = st.text_area(
            "Paste Single Cookie String",
            height=100,
            placeholder="c_user=1000...; xs=...; fr=... (Full cookie string)",
            key="single_cookie"
        )
    
    with cookie_tabs[1]:  # Multiple Cookies File
        uploaded_file = st.file_uploader(
            "📤 Upload cookie.txt (one cookie per line)", 
            type=['txt'],
            key="cookie_file"
        )
        if uploaded_file is not None:
            cookies_content = load_cookies_from_file(uploaded_file)
            st.text_area(
                "Loaded Cookies",
                value=cookies_content,
                height=100,
                key="multiple_cookie_display"
            )
            st.session_state.cookies = cookies_content
    
    st.markdown('<h3 class="section-title">📱 Chat ID / E2EE / Inbox</h3>', unsafe_allow_html=True)
    chat_input = st.text_area(
        "Enter Chat IDs (one per line)",
        height=100,
        placeholder="1362400298935018\n100036283209197",
        key="chat_input"
    )
    st.session_state.chat_ids = [x.strip() for x in chat_input.split('\n') if x.strip()]
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">💬 Messages</h3>', unsafe_allow_html=True)
    
    # Message file upload
    msg_file = st.file_uploader("📤 Upload Message TXT", type=['txt'], key="msg_file")
    if msg_file:
        msg_content = msg_file.read().decode('utf-8')
        st.session_state.messages = [x.strip() for x in msg_content.split('\n') if x.strip()]
        st.success(f"✅ Loaded {len(st.session_state.messages)} messages")
    else:
        msg_input = st.text_area(
            "Enter Messages (one per line)",
            height=120,
            placeholder="Hello!\nHow are you?\nGood morning!",
            key="msg_input"
        )
        st.session_state.messages = [x.strip() for x in msg_input.split('\n') if x.strip()]
    
    st.markdown('<h3 class="section-title">👤 Prefix</h3>', unsafe_allow_html=True)
    st.session_state.prefix = st.text_input("Name Prefix", placeholder="YKTI RAWAT", key="prefix")
    
    st.markdown('<h3 class="section-title">⏱️ Delay</h3>', unsafe_allow_html=True)
    st.session_state.delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, value=5, key="delay")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📨 Messages</h3>
        <h1 style="font-size: 2.5rem;">{st.session_state.count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    status = "🟢 LIVE" if st.session_state.running else "🔴 STOPPED"
    st.markdown(f"""
    <div class="metric-container">
        <h3>⚙️ Status</h3>
        <h1 style="font-size: 2rem;">{status}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📱 Chats</h3>
        <h1 style="font-size: 2rem;">{len(st.session_state.chat_ids)}</h1>
    </div>
    """, unsafe_allow_html=True)

# Control Buttons - Small & Lower
st.markdown('<div style="margin-top: 2rem; padding: 2rem; text-align: center;">', unsafe_allow_html=True)
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🚀 START MESSAGING", key="start", disabled=st.session_state.running, use_container_width=True):
        start()

with col_btn2:
    if st.button("⏹️ STOP MESSAGING", key="stop", disabled=not st.session_state.running, use_container_width=True):
        stop()

st.markdown('</div>', unsafe_allow_html=True)

# Live Logs
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">📊 LIVE LOGS</h3>', unsafe_allow_html=True)

logs_html = '<div class="logs-container">'
for log in st.session_state.logs[-25:]:
    logs_html += f'<div>{log}</div>'
logs_html += '</div>'
st.markdown(logs_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Auto refresh
if st.session_state.running:
    time.sleep(2)
    st.rerun()
