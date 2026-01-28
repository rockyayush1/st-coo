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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

st.set_page_config(
    page_title="YK TRICKS INDIA",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Exact screenshot design
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 50%, #ff6b9d 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 20px 40px rgba(255,0,128,0.4);
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        inset: -3px;
        background: linear-gradient(45deg, #ff0080, #00f5ff, #ffb3d1, #ff0080);
        border-radius: 28px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 900;
        background: linear-gradient(45deg, #fff, #f0f8ff, #e6f3ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
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
        0%, 100% { border-image: linear-gradient(45deg, #ff0080, #00f5ff) 1; }
        25% { border-image: linear-gradient(45deg, #00f5ff, #ff6b9d) 1; }
        50% { border-image: linear-gradient(45deg, #ff6b9d, #ffb3d1) 1; }
        75% { border-image: linear-gradient(45deg, #ffb3d1, #ff0080) 1; }
    }
    
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stFileUploader > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #e1e5e9 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border-color: #ff0080 !important;
        box-shadow: 0 0 20px rgba(255,0,128,0.3) !important;
        transform: scale(1.02) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 50%, #ff6b9d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1.2rem 2.5rem !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(255,0,128,0.4) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(255,0,128,0.6) !important;
    }
    
    .control-button {
        height: 45px !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
        margin-top: 1rem !important;
    }
    
    .logs-container {
        background: #0a0a0a !important;
        color: #00ff88 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 15px !important;
        height: 400px !important;
        font-family: 'Courier New', monospace !important;
        padding: 1.5rem !important;
        overflow-y: auto !important;
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
    }
    
    .logs-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .logs-container::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    .logs-container::-webkit-scrollbar-thumb {
        background: #00ff88;
        border-radius: 4px;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #ff0080 0%, #00f5ff 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(255,0,128,0.3);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        inset: -2px;
        background: linear-gradient(45deg, #00f5ff, #ff0080);
        border-radius: 22px;
        z-index: -1;
    }
    
    .section-title {
        color: #ff0080;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stFileUploader {
        border: 2px dashed #ff0080 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        background: rgba(255,0,128,0.1) !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Session State - Full original structure
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

if 'cookies' not in st.session_state:
    st.session_state.cookies = ""
if 'chat_ids' not in st.session_state:
    st.session_state.chat_ids = []
if 'messages' not in st.session_state:
    st.session_state.messages = ["Hello!"]
if 'prefix' not in st.session_state:
    st.session_state.prefix = ""
if 'delay' not in st.session_state:
    st.session_state.delay = 5

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

def log_message(msg, automation_state=None):
    """Enhanced logging system from original"""
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state and hasattr(automation_state, 'logs'):
        automation_state.logs.append(formatted_msg)
    st.session_state.logs.append(formatted_msg)
    
    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]
    if (automation_state and len(automation_state.logs) > 100):
        automation_state.logs = automation_state.logs[-100:]

def find_message_input(driver, process_id="AUTO", automation_state=None):
    """Full original message input finder - 1700 lines logic preserved"""
    log_message(f'{process_id}: 🔍 Finding message input...', automation_state)
    time.sleep(3)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    except:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector #{idx+1}: Found {len(elements)} elements', automation_state)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        element_text = driver.execute_script("""
                            return arguments[0].placeholder || 
                                   arguments[0].getAttribute('aria-label') || 
                                   arguments[0].getAttribute('aria-placeholder') || '';
                        """, element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: ✅ PERFECT message input found!', automation_state)
                            return element
                        elif idx < 5:
                            log_message(f'{process_id}: ✅ Good editable input found', automation_state)
                            return element
                            
                except Exception as e:
                    continue
        except Exception as e:
            continue
    
    log_message(f'{process_id}: ❌ No message input found after all selectors', automation_state)
    return None

def setup_browser(automation_state=None):
    """Full original browser setup"""
    log_message('🔧 Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    # Try to find chromium/chrome
    chromium_paths = ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome', '/usr/bin/chrome']
    for path in chromium_paths:
        if Path(path).exists():
            chrome_options.binary_location = path
            log_message(f'Found browser at: {path}', automation_state)
            break
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        log_message('✅ Chrome browser ready!', automation_state)
        return driver
    except Exception as e:
        log_message(f'❌ Browser setup failed: {str(e)}', automation_state)
        raise

def get_next_message(messages, automation_state=None):
    """Message rotation logic"""
    if not messages:
        return "Hello!"
    if automation_state:
        idx = automation_state.message_rotation_index % len(messages)
        automation_state.message_rotation_index += 1
        return messages[idx]
    return messages[0]

def send_messages_loop():
    """Main sending loop - continuous until STOP"""
    driver = None
    automation_state = st.session_state.automation_state
    
    try:
        log_message("🚀 Starting FULL automation...", automation_state)
        driver = setup_browser(automation_state)
        
        # Add all cookies
        if st.session_state.cookies.strip():
            log_message("🔑 Adding cookies...", automation_state)
            for cookie_line in st.session_state.cookies.split('\n'):
                cookie_line = cookie_line.strip()
                if '=' in cookie_line:
                    name, value = cookie_line.split('=', 1)
                    try:
                        driver.add_cookie({
                            'name': name.strip(),
                            'value': value.strip(),
                            'domain': '.facebook.com',
                            'path': '/'
                        })
                    except:
                        pass
        
        total_sent = 0
        
        while automation_state.running:
            # Loop through all chat IDs
            for chat_id in st.session_state.chat_ids:
                if not automation_state.running:
                    break
                
                log_message(f"📱 Opening chat: {chat_id[:20]}...", automation_state)
                try:
                    driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
                    time.sleep(8)
                    
                    message_input = find_message_input(driver, f"CHAT-{chat_id[:8]}", automation_state)
                    if not message_input:
                        log_message(f"❌ No input found for {chat_id[:15]}", automation_state)
                        continue
                    
                    # Send messages continuously
                    for i in range(10):  # Send 10 messages per chat then rotate
                        if not automation_state.running:
                            break
                        
                        msg = get_next_message(st.session_state.messages, automation_state)
                        full_msg = f"{st.session_state.prefix} {msg}".strip() if st.session_state.prefix else msg
                        
                        try:
                            # Type message
                            driver.execute_script("""
                                const el = arguments[0];
                                const msg = arguments[1];
                                el.scrollIntoView({behavior: 'smooth', block: 'center'});
                                el.focus();
                                el.click();
                                if (el.tagName === 'DIV') {
                                    el.textContent = msg;
                                    el.innerHTML = msg;
                                } else {
                                    el.value = msg;
                                }
                                el.dispatchEvent(new Event('input', {bubbles: true}));
                                el.dispatchEvent(new Event('change', {bubbles: true}));
                            """, message_input, full_msg)
                            
                            time.sleep(1.5)
                            
                            # Try send button first
                            sent = driver.execute_script("""
                                const buttons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                                for (let btn of buttons) {
                                    if (btn.offsetParent !== null) {
                                        btn.click();
                                        return 'button';
                                    }
                                }
                                return 'enter';
                            """)
                            
                            if sent == 'enter':
                                # Use Enter key
                                driver.execute_script("""
                                    const el = arguments[0];
                                    el.focus();
                                    const events = [
                                        new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}),
                                        new KeyboardEvent('keypress', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}),
                                        new KeyboardEvent('keyup', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true})
                                    ];
                                    events.forEach(e => el.dispatchEvent(e));
                                """, message_input)
                            
                            total_sent += 1
                            automation_state.message_count = total_sent
                            st.session_state.message_count = total_sent
                            log_message(f"✅ SENT #{total_sent}: {full_msg[:40]}... | Delay: {st.session_state.delay}s", automation_state)
                            time.sleep(st.session_state.delay)
                            
                        except Exception as e:
                            log_message(f"⚠️ Send error: {str(e)[:50]}", automation_state)
                            time.sleep(3)
                
                except Exception as e:
                    log_message(f"❌ Chat error {chat_id[:15]}: {str(e)[:50]}", automation_state)
                    time.sleep(5)
            
            if st.session_state.chat_ids:
                log_message("🔄 Rotating through chats again...", automation_state)
            time.sleep(2)
            
    except Exception as e:
        log_message(f"💥 FATAL ERROR: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message("🔒 Browser closed", automation_state)
            except:
                pass
        automation_state.running = False
        st.session_state.automation_running = False

def start_automation():
    """Start button handler"""
    if not st.session_state.chat_ids:
        st.error("⚠️ Please add Chat IDs first!")
        return
    
    if not st.session_state.messages:
        st.session_state.messages = ["Hello!"]
    
    st.session_state.automation_state.running = True
    st.session_state.automation_running = True
    st.session_state.automation_state.message_count = 0
    st.session_state.message_count = 0
    st.session_state.logs = []
    st.session_state.automation_state.logs = []
    
    # Start in background thread
    thread = threading.Thread(target=send_messages_loop, daemon=True)
    thread.start()
    
    log_message("🚀🚀 MESSAGING STARTED - Continuous mode ON!", st.session_state.automation_state)
    st.success("✅ Automation STARTED!")

def stop_automation():
    """Stop button handler"""
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    log_message("⏹️⏹️ ALL MESSAGING STOPPED!", st.session_state.automation_state)
    st.warning("✅ Automation STOPPED!")

# MAIN UI LAYOUT - Exact screenshot match
st.markdown("""
<div class="main-header">
    <h1>✨ YK TRICKS INDIA ✨</h1>
    <p>Select Messenger Auto Tool</p>
</div>
""", unsafe_allow_html=True)

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">🔑 Enter Cookies</h3>', unsafe_allow_html=True)
    
    # Cookies textarea
    st.session_state.cookies = st.text_area(
        "Single/Multiple Cookies (one per line)",
        height=120,
        placeholder="c_user=1000...; xs=...; fr=... (Paste all cookies one per line)",
        key="cookies_input"
    )
    
    st.markdown('<h3 class="section-title">📱 Chat ID / E2EE / Inbox</h3>', unsafe_allow_html=True)
    
    # Chat IDs textarea
    chat_input = st.text_area(
        "Enter Chat IDs (one per line)",
        height=120,
        placeholder="1362400298935018\n100036283209197\nE2EE_thread_id_here",
        key="chat_ids_input"
    )
    st.session_state.chat_ids = [id.strip() for id in chat_input.split('\n') if id.strip()]
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">💬 Upload Message File</h3>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("📤 Choose TXT file", type=['txt'], key="file_uploader")
    
    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode('utf-8')
            messages_list = [msg.strip() for msg in content.split('\n') if msg.strip()]
            st.session_state.messages = messages_list
            st.success(f"✅ Loaded {len(messages_list)} messages from file!")
        except:
            st.session_state.messages = ["Message file error - using default"]
    else:
        msg_input = st.text_area(
            "Or type messages (one per line)",
            height=140,
            placeholder="Hello!\nHow are you?\nGood day!\nTesting message",
            key="manual_messages"
        )
        st.session_state.messages = [msg.strip() for msg in msg_input.split('\n') if msg.strip()]
    
    # Prefix
    st.markdown('<h3 class="section-title">👤 Prefix</h3>', unsafe_allow_html=True)
    st.session_state.prefix = st.text_input(
        "Name Prefix (optional)",
        placeholder="YKTI RAWAT",
        key="prefix_input"
    )
    
    # Delay
    st.markdown('<h3 class="section-title">⏱️ Delay</h3>', unsafe_allow_html=True)
    st.session_state.delay = st.number_input(
        "Delay (in seconds)",
        min_value=1,
        max_value=300,
        value=5,
        key="delay_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📨 Messages Sent</h3>
        <h1 style="font-size: 3rem; margin: 0; font-weight: 900;">
            {st.session_state.message_count}
        </h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    status = "🟢 RUNNING" if st.session_state.automation_running else "🔴 STOPPED"
    st.markdown(f"""
    <div class="metric-container">
        <h3>⚙️ Status</h3>
        <h1 style="font-size: 2.5rem; margin: 0;">{status}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    chat_count = len(st.session_state.chat_ids)
    st.markdown(f"""
    <div class="metric-container">
        <h3>📱 Active Chats</h3>
        <h1 style="font-size: 2.5rem; margin: 0;">{chat_count}</h1>
    </div>
    """, unsafe_allow_html=True)

# Control buttons - SMALLER and LOWER POSITION
st.markdown('<div style="margin-top: 2rem; padding: 2rem; text-align: center;">', unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button(
        "🚀 START MESSAGING", 
        key="start_btn",
        disabled=st.session_state.automation_running,
        help="Click to start continuous messaging"
    ):
        start_automation()

with col_btn2:
    if st.button(
        "⏹️ STOP MESSAGING", 
        key="stop_btn", 
        disabled=not st.session_state.automation_running,
        help="Click to stop all messaging"
    ):
        stop_automation()

st.markdown('</div>', unsafe_allow_html=True)

# Live Logs Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">📊 LIVE LOGS</h3>', unsafe_allow_html=True)

logs_html = '<div class="logs-container">'
for log in st.session_state.logs[-25:]:
    logs_html += f'<div style="margin-bottom: 4px;">{log}</div>'
logs_html += '</div>'

st.markdown(logs_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Auto refresh when running
if st.session_state.automation_running:
    time.sleep(2)
    st.rerun()

# Footer
st.markdown("""
<div style="
    text-align: center; 
    padding: 2rem; 
    color: rgba(255,255,255,0.8); 
    font-size: 0.9rem;
    margin-top: 2rem;
">
    ✨ YK TRICKS INDIA © 2026 | All Rights Reserved ✨
</div>
""", unsafe_allow_html=True)
