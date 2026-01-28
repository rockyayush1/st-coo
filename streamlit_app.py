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
import database as db
import requests

st.set_page_config(
    page_title="YKTI RAWAT",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = "<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
    }
    
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
        background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff0080, #00ff80, #ff00ff);
        border-radius: 27px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
        filter: blur(0.5px);
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
    
    @keyframes pulseGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        animation: containerPulse 3s ease-in-out infinite;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        inset: -2px;
        background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
        border-radius: 22px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
    }
    
    @keyframes containerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
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
    
    .console-output {
        background: #000 !important;
        border: 2px solid #00ffff;
        color: #00ff88 !important;
        border-radius: 15px;
        height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .console-line {
        margin-bottom: 0.5rem;
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    .stTextInput div div input, 
    .stTextArea div div textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #00ffff !important;
        border-radius: 12px;
        color: #333 !important;
        padding: 1rem;
        font-weight: 500;
    }
    
    .stTextInput div div input:focus,
    .stTextArea div div textarea:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
        transform: scale(1.02);
    }
    
    .stFileUploader label {
        color: #ff00ff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
</style>
"

st.markdown(custom_css, unsafe_allow_html=True)

# Session state initialization - NO LOGIN REQUIRED
if 'automation_state' not in st.session_state:
    st.session_state.automation_state = {
        'running': False,
        'task_key': None,
        'message_count': 0,
        'logs': [],
        'message_rotation_index': 0,
        'cookies': '',
        'chat_id': '',
        'delay': 5,
        'name_prefix': '',
        'messages': [],
        'cookie_type': 'single'
    }

if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = {}

def log_message(msg):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    st.session_state.automation_state['logs'].append(formatted_msg)
    if len(st.session_state.automation_state['logs']) > 200:
        st.session_state.automation_state['logs'] = st.session_state.automation_state['logs'][-200:]
    st.rerun()

def generate_task_key():
    return str(uuid.uuid4())[:8].upper()

def find_message_input(driver, process_id):
    log_message(f"{process_id}: 🔍 Finding message input...")
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
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
    
    log_message(f"{process_id}: Testing {len(message_input_selectors)} selectors...")
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f"{process_id}: Selector #{idx+1}: Found {len(elements)} elements")
            
            for element in elements:
                try:
                    is_editable = driver.execute_script(
                        "return arguments[0].contentEditable === 'true' || "
                        "arguments[0].tagName === 'TEXTAREA' || "
                        "arguments[0].tagName === 'INPUT';", 
                        element
                    )
                    
                    if is_editable:
                        element_text = driver.execute_script(
                            "return arguments[0].placeholder || "
                            "arguments[0].getAttribute('aria-label') || "
                            "arguments[0].getAttribute('aria-placeholder') || '';", 
                            element
                        ).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f"{process_id}: ✅ PERFECT message input found!")
                            return element
                        elif idx < 5:
                            log_message(f"{process_id}: ✅ Good editable input found")
                            return element
                            
                except:
                    continue
        except:
            continue
    
    log_message(f"{process_id}: ❌ No message input found!")
    return None

def setup_browser():
    log_message("🔧 Setting up Chrome browser...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        log_message("✅ Chrome browser ready!")
        return driver
    except Exception as e:
        log_message(f"💥 Browser setup failed: {str(e)}")
        raise e

def get_next_message(messages):
    if not messages:
        return "Hello!"
    idx = st.session_state.automation_state['message_rotation_index'] % len(messages)
    st.session_state.automation_state['message_rotation_index'] += 1
    return messages[idx]

def send_messages_loop(task_key):
    driver = None
    messages_sent = 0
    
    try:
        log_message(f"TASK-{task_key}: 🚀 Automation STARTED!")
        driver = setup_browser()
        
        # Facebook login with cookies
        log_message(f"TASK-{task_key}: 🌐 Going to Facebook...")
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        cookies = st.session_state.automation_state['cookies']
        if cookies and cookies.strip():
            log_message(f"TASK-{task_key}: 🍪 Adding {len(cookies.split(';')) if ';' in cookies else 1} cookies...")
            cookie_array = cookies.split(';') if ';' in cookies else [cookies]
            
            for cookie_str in cookie_array:
                cookie_trimmed = cookie_str.strip()
                if '=' in cookie_trimmed:
                    name, value = cookie_trimmed.split('=', 1)
                    name = name.strip()
                    value = value.strip()
                    try:
                        driver.add_cookie({
                            'name': name,
                            'value': value,
                            'domain': '.facebook.com',
                            'path': '/'
                        })
                        log_message(f"TASK-{task_key}: Added cookie: {name}")
                    except Exception as e:
                        log_message(f"TASK-{task_key}: Cookie error: {str(e)[:50]}")
        
        # Open target chat
        chat_id = st.session_state.automation_state['chat_id'].strip()
        if chat_id:
            log_message(f"TASK-{task_key}: 💬 Opening chat {chat_id[:8]}...")
            driver.get(f"https://www.facebook.com/messages/t/{chat_id}")
        else:
            log_message(f"TASK-{task_key}: 💬 Opening messages...")
            driver.get("https://www.facebook.com/messages")
        
        time.sleep(15)
        
        messages_list = st.session_state.automation_state['messages']
        delay = st.session_state.automation_state['delay']
        name_prefix = st.session_state.automation_state['name_prefix']
        
        if not messages_list:
            messages_list = ["Hello!"]
            log_message(f"TASK-{task_key}: Using default message")
        
        log_message(f"TASK-{task_key}: 📝 Loaded {len(messages_list)} messages")
        log_message(f"TASK-{task_key}: ⏱️ Delay: {delay}s | Prefix: {name_prefix or 'None'}")
        
        while st.session_state.active_tasks.get(task_key, False):
            if not st.session_state.automation_state['running']:
                break
                
            base_message = get_next_message(messages_list)
            message_to_send = f"{name_prefix} {base_message}" if name_prefix else base_message
            
            message_input = find_message_input(driver, f"TASK-{task_key}")
            if not message_input:
                log_message(f"TASK-{task_key}: Retrying input search...")
                time.sleep(10)
                continue
            
            try:
                # Type message
                driver.execute_script("
                    const element = arguments[0];
                    const message = arguments[1];
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    element.dispatchEvent(new Event('input', {bubbles: true}));
                    element.dispatchEvent(new Event('change', {bubbles: true}));
                    element.dispatchEvent(new InputEvent('input', {bubbles: true, data: message}));
                ", message_input, message_to_send)
                
                time.sleep(1.5)
                
                # Try send button first
                sent = driver.execute_script("
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';")
                
                if sent == 'button_not_found':
                    # Fallback to Enter key
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        const events = [
                            new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}),
                            new KeyboardEvent('keypress', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}),
                            new KeyboardEvent('keyup', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true})
                        ];
                        events.forEach(event => element.dispatchEvent(event));
                    ", message_input)
                    log_message(f"TASK-{task_key}: ✅ #{messages_sent+1} Sent (Enter): {message_to_send[:40]}...")
                else:
                    log_message(f"TASK-{task_key}: ✅ #{messages_sent+1} Sent (Button): {message_to_send[:40]}...")
                
                messages_sent += 1
                st.session_state.automation_state['message_count'] = messages_sent
                time.sleep(delay)
                
            except Exception as e:
                log_message(f"TASK-{task_key}: ❌ Send error: {str(e)[:100]}")
                time.sleep(5)
        
        total_sent = st.session_state.automation_state['message_count']
        log_message(f"TASK-{task_key}: 🛑 STOPPED! Total sent: {total_sent}")
        
    except Exception as e:
        log_message(f"TASK-{task_key}: 💥 FATAL ERROR: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"TASK-{task_key}: Browser closed")
            except:
                pass

def start_automation():
    if st.session_state.automation_state['running']:
        st.warning("⚠️ Already running!")
        return
    
    # Validation
    if not st.session_state.automation_state['messages']:
        st.error("❌ Upload message TXT files first!")
        return
    if not st.session_state.automation_state['chat_id'].strip():
        st.error("❌ Enter Chat/Conversation ID!")
        return
    if not st.session_state.automation_state['cookies'].strip():
        st.error("❌ Add cookies first!")
        return
    
    task_key = generate_task_key()
    st.session_state.automation_state['task_key'] = task_key
    st.session_state.automation_state['running'] = True
    st.session_state.active_tasks[task_key] = True
    st.session_state.automation_state['message_count'] = 0
    st.session_state.automation_state['logs'] = []
    st.session_state.automation_state['message_rotation_index'] = 0
    
    thread = threading.Thread(target=send_messages_loop, args=(task_key,))
    thread.daemon = True
    thread.start()
    
    st.success(f"🚀 STARTED! **TASK KEY: `{task_key}`**")
    st.info("📋 Copy this task key to stop instantly")

def stop_by_task_key():
    input_key = st.session_state.get('stop_task_key_input', '').strip().upper()
    if input_key and input_key in st.session_state.active_tasks:
        st.session_state.active_tasks[input_key] = False
        st.session_state.automation_state['running'] = False
        st.session_state.automation_state['task_key'] = None
        st.session_state.stop_task_key_input = ""
        st.success(f"🛑 INSTANT STOP: Task {input_key}")
        st.rerun()
    elif input_key:
        st.error("❌ Invalid task key!")

def stop_automation():
    task_key = st.session_state.automation_state.get('task_key')
    if task_key and st.session_state.active_tasks.get(task_key):
        st.session_state.active_tasks[task_key] = False
        st.session_state.automation_state['running'] = False
        st.session_state.automation_state['task_key'] = None
        st.success("🛑 Automation stopping...")
        st.rerun()

# MAIN DASHBOARD (NO LOGIN)
st.markdown("<div class="main-header">
        <h1>📱 YKTI RAWAT</h1>
        <p>PREMIUM UNLIMITED MESSAGE SENDER - TASK KEY CONTROL</p>
    </div>
", unsafe_allow_html=True)

# Status Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("📊 Messages Sent", st.session_state.automation_state['message_count'])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    status = "🟢 RUNNING" if st.session_state.automation_state['running'] else "🔴 STOPPED"
    st.metric("⚙️ Status", status)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    task_key_display = st.session_state.automation_state.get('task_key', 'Not Running')
    st.metric("🔑 Current Task Key", task_key_display)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Main Tabs
tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "📊 LIVE LOGS"])

with tab1:
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.markdown("### 📄 Message Files")
        uploaded_files = st.file_uploader(
            "Upload TXT files (one message per line)", 
            type=['txt'], 
            accept_multiple_files=True,
            help="Multiple TXT files supported!"
        )
        
        if uploaded_files:
            all_messages = []
            for uploaded_file in uploaded_files:
                try:
                    content = uploaded_file.read().decode('utf-8')
                    file_messages = [line.strip() for line in content.split('\n') if line.strip()]
                    all_messages.extend(file_messages)
                    st.success(f"✅ {uploaded_file.name}: {len(file_messages)} messages")
                except:
                    st.error(f"❌ Error reading {uploaded_file.name}")
            
            if all_messages:
                st.session_state.automation_state['messages'] = all_messages
                st.success(f"📝 Total: {len(all_messages)} messages loaded!")
        
        st.markdown("### 💬 Chat Settings")
        chat_id = st.text_input(
            "Chat/Conversation ID", 
            value=st.session_state.automation_state['chat_id'],
            placeholder="e.g., 1234567890123456",
            help="Get from Facebook URL: /messages/t/ID/"
        )
        
        name_prefix = st.text_input(
            "Name Prefix (optional)", 
            value=st.session_state.automation_state['name_prefix'],
            placeholder="e.g., YKTI RAWAT"
        )
        
        delay = st.number_input(
            "Delay (seconds)", 
            min_value=1, 
            max_value=300, 
            value=st.session_state.automation_state['delay']
        )
    
    with col_config2:
        st.markdown("### 🍪 Cookies")
        cookie_type = st.radio(
            "Cookie Type:",
            ["Single Cookie", "Multiple Cookies"],
            index=0 if st.session_state.automation_state['cookie_type'] == 'single' else 1
        )
        st.session_state.automation_state['cookie_type'] = 'single' if cookie_type == "Single Cookie" else 'multiple'
        
        if cookie_type == "Single Cookie":
            cookies = st.text_area(
                "Paste Single Cookie Here",
                value=st.session_state.automation_state['cookies'],
                height=120,
                placeholder="c_user=123...; xs=ABC...; datr=XYZ... (semicolon separated)"
            )
        else:
            cookies = st.text_area(
                "Multiple Cookies (one per line)",
                value=st.session_state.automation_state['cookies'],
                height=200,
                placeholder="c_user=123...\nxs=ABC...\ndatr=XYZ...\n(each cookie on new line)"
            )
        
        if st.button("💾 SAVE CONFIG", use_container_width=True):
            st.session_state.automation_state.update({
                'chat_id': chat_id,
                'cookies': cookies,
                'delay': delay,
                'name_prefix': name_prefix
            })
            st.success("✅ Configuration saved!")
            st.rerun()
    
    # Control Buttons
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🚀 START AUTOMATION", use_container_width=True, disabled=st.session_state.automation_state['running']):
            start_automation()
    
    with col_btn2:
        if st.button("🛑 EMERGENCY STOP", use_container_width=True, disabled=not st.session_state.automation_state['running']):
            stop_automation()
    
    # Task Key Stop
    st.markdown("### 🔑 Instant Stop by Task Key")
    stop_key_input = st.text_input("Paste Task Key Here", key="stop_task_key_input")
    if st.button("STOP BY TASK KEY", use_container_width=True):
        stop_by_task_key()

with tab2:
    st.markdown("### 📊 LIVE CONSOLE OUTPUT")
    if st.session_state.automation_state['logs']:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        for log in st.session_state.automation_state['logs'][-100:]:
            st.markdown(f'<div class="console-line">{log}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 REFRESH LOGS", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🗑️ CLEAR LOGS", use_container_width=True):
                st.session_state.automation_state['logs'] = []
                st.rerun()
    else:
        st.info("👀 No logs yet. Start automation to see live output!")

# Footer
st.markdown("<div style='text-align: center; padding: 3rem; color: white; background: rgba(0,0,0,0.2); border-radius: 20px; margin-top: 3rem;'>
        <h3>🚀 YKTI RAWAT - PREMIUM UNLIMITED MESSAGING 2026</h3>
        <p>✅ No login • ✅ TXT upload • ✅ Task key control • ✅ Unlimited running • ✅ Live logs</p>
    </div>
    ", unsafe_allow_html=True)
