import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

st.set_page_config(page_title="YK TRICKS INDIA", layout="wide")

# Custom CSS - Screenshot exact design
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #2d1b69 50%, #1a0f3d 100%);
        background-attachment: fixed;
    }
    .main-header {
        background: linear-gradient(135deg, #ff0080 0%, #ff6b9d 50%, #ffb3d1 100%);
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(255,0,128,0.4);
    }
    .main-header h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .input-box {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .input-box::before {
        content: '';
        position: absolute;
        inset: -3px;
        background: linear-gradient(45deg, #ff0080, #00f5ff, #ff0080);
        border-radius: 23px;
        z-index: -1;
    }
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #e1e5e9 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(255,0,128,0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(255,0,128,0.6) !important;
    }
    .control-btn {
        height: 45px !important;
        font-size: 1rem !important;
        margin-top: 1rem !important;
    }
    .logs-box {
        background: #000 !important;
        color: #00ff88 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 15px !important;
        height: 350px !important;
        font-family: 'Courier New', monospace !important;
        padding: 1.5rem !important;
        overflow-y: auto !important;
        font-size: 0.9rem !important;
    }
    .metric-box {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(255,0,128,0.3);
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

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")
    if len(st.session_state.logs) > 50:
        st.session_state.logs = st.session_state.logs[-50:]

def find_input(driver):
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        '[role="textbox"]',
        'textarea'
    ]
    for sel in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in elements:
                if driver.execute_script("return arguments[0].contentEditable === 'true'", el):
                    return el
        except:
            continue
    return None

def worker():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get('https://www.facebook.com/')
        time.sleep(3)
        
        # Add cookies
        for cookie_line in st.session_state.cookies.split('\n'):
            if '=' in cookie_line:
                name, value = cookie_line.strip().split('=', 1)
                driver.add_cookie({'name': name.strip(), 'value': value.strip(), 'domain': '.facebook.com'})
        
        total = 0
        while st.session_state.running:
            for chat_id in st.session_state.chat_ids:
                if not st.session_state.running:
                    break
                    
                log(f"📱 Opening chat: {chat_id[:15]}...")
                driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
                time.sleep(8)
                
                inp = find_input(driver)
                if not inp:
                    log("❌ Message box not found")
                    continue
                
                for msg in st.session_state.messages:
                    if not st.session_state.running:
                        break
                        
                    full_msg = f"{st.session_state.prefix} {msg}" if st.session_state.prefix else msg
                    
                    driver.execute_script("""
                        arguments[0].focus();
                        arguments[0].textContent = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                    """, inp, full_msg)
                    
                    time.sleep(1)
                    driver.execute_script("""
                        arguments[0].dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true}));
                        arguments[0].dispatchEvent(new KeyboardEvent('keyup', {key: 'Enter', bubbles: true}));
                    """, inp)
                    
                    total += 1
                    st.session_state.count = total
                    log(f"✅ Sent: {full_msg[:30]}... (Total: {total})")
                    time.sleep(st.session_state.delay)
                
                if not st.session_state.running:
                    break
    except Exception as e:
        log(f"❌ Error: {str(e)[:50]}")
    finally:
        driver.quit()
        log("🔄 Browser closed")

def start():
    if st.session_state.chat_ids and st.session_state.messages:
        st.session_state.running = True
        st.session_state.count = 0
        st.session_state.logs = []
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        log("🚀 START MESSAGING")
    else:
        st.error("⚠️ Add Chat IDs & Messages first!")

def stop():
    st.session_state.running = False
    log("⏹️ STOPPED")

# Header
st.markdown("""
<div class="main-header">
    <h1>✨ YK TRICKS INDIA ✨</h1>
    <p>Messenger Auto Tool</p>
</div>
""", unsafe_allow_html=True)

# Inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    st.markdown("### 🔑 **Enter Cookies**")
    st.session_state.cookies = st.text_area("Single/Multiple Cookies (one per line)", 
                                          height=120, key="cookie_input")
    st.markdown("### 📱 **Chat ID / E2EE / Inbox**")
    chat_input = st.text_area("Enter Chat IDs (one per line)", height=100, key="chat_input")
    st.session_state.chat_ids = [x.strip() for x in chat_input.split('\n') if x.strip()]
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    st.markdown("### 💬 **Upload Message TXT File**")
    uploaded = st.file_uploader("📤 Choose file", type="txt")
    if uploaded:
        content = uploaded.read().decode()
        st.session_state.messages = [x.strip() for x in content.split('\n') if x.strip()]
    else:
        msg_input = st.text_area("Or Enter Messages (one per line)", height=120, key="msg_input")
        st.session_state.messages = [x.strip() for x in msg_input.split('\n') if x.strip()]
    
    st.session_state.prefix = st.text_input("👤 **Prefix**", placeholder="YKTI RAWAT")
    st.session_state.delay = st.number_input("⏱️ **Delay (seconds)**", min_value=1, max_value=60, value=5)
    st.markdown('</div>', unsafe_allow_html=True)

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h3>📨 Messages Sent</h3>
        <h1>{st.session_state.count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    status = "🟢 LIVE" if st.session_state.running else "🔴 STOPPED"
    st.markdown(f"""
    <div class="metric-box">
        <h3>⚙️ Status</h3>
        <h1>{status}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <h3>📱 Chats</h3>
        <h1>{len(st.session_state.chat_ids)}</h1>
    </div>
    """, unsafe_allow_html=True)

# Control Buttons - Smaller & Lower
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 START MESSAGING", key="start", help="Start sending messages"):
        start()

with col2:
    if st.button("⏹️ STOP MESSAGING", key="stop", disabled=not st.session_state.running):
        stop()

# Live Logs
st.markdown('<div class="input-box">', unsafe_allow_html=True)
st.markdown("### 📊 **LIVE LOGS**")
logs_html = '<div class="logs-box">'
for log in st.session_state.logs[-20:]:
    logs_html += f'<div>{log}</div>'
logs_html += '</div>'
st.markdown(logs_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Auto refresh
if st.session_state.running:
    time.sleep(2)
    st.rerun()
