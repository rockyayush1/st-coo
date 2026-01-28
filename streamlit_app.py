import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import json
import base64
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import tempfile

# Page config
st.set_page_config(
    page_title="YKTI RAWAT - Message Sender",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with clean background
custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .main-header {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 25px;
        padding: 3rem 2rem;
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
        background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff0080);
        border-radius: 27px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
    }
    @keyframes borderRotate {
        0% { transform: rotate(0deg) scale(1); }
        100% { transform: rotate(360deg) scale(1); }
    }
    .main-header h1 {
        background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
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
    .metric-container {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid transparent;
        animation: containerPulse 3s ease-in-out infinite;
    }
    @keyframes containerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    .console-output {
        background: #000 !important;
        border: 1px solid #00ffff;
        color: #00ff88 !important;
        border-radius: 15px;
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        font-family: 'Courier New', monospace;
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
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Session state initialization
if 'automation_state' not in st.session_state:
    st.session_state.automation_state = {
        'running': False,
        'task_key': None,
        'message_count': 0,
        'logs': [],
        'cookies': '',
        'chat_id': '',
        'delay': 5,
        'name_prefix': '',
        'messages': [],
        'message_rotation_index': 0
    }
if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = {}

def log_message(msg):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    st.session_state.automation_state['logs'].append(formatted_msg)
    if len(st.session_state.automation_state['logs']) > 100:
        st.session_state.automation_state['logs'] = st.session_state.automation_state['logs'][-100:]

def generate_task_key():
    return str(uuid.uuid4())[:8].upper()

def find_message_input(driver, process_id):
    log_message(f"{process_id}: Finding message input...")
    time.sleep(10)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    is_editable = driver.execute_script(
                        "return arguments[0].contentEditable === 'true' || "
                        "arguments[0].tagName === 'TEXTAREA' || "
                        "arguments[0].tagName === 'INPUT';", element
                    )
                    if is_editable:
                        log_message(f"{process_id}: ✅ Found message input #{idx+1}")
                        return element
                except:
                    continue
        except:
            continue
    log_message(f"{process_id}: ❌ Message input not found!")
    return None

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver

def get_next_message(messages):
    if not messages:
        return "Hello!"
    idx = st.session_state.automation_state['message_rotation_index'] % len(messages)
    st.session_state.automation_state['message_rotation_index'] += 1
    return messages[idx]

def send_messages_loop(task_key):
    driver = None
    try:
        log_message(f"TASK-{task_key}: 🚀 Starting automation...")
        driver = setup_browser()
        
        # Add cookies
        if st.session_state.automation_state['cookies']:
            log_message(f"TASK-{task_key}: Adding cookies...")
            cookie_array = st.session_state.automation_state['cookies'].split(';')
            driver.get('https://www.facebook.com/')
            time.sleep(5)
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if '=' in cookie_trimmed:
                    name, value = cookie_trimmed.split('=', 1)
                    try:
                        driver.add_cookie({'name': name.strip(), 'value': value.strip(), 'domain': '.facebook.com'})
                    except:
                        pass
        
        # Open chat
        chat_id = st.session_state.automation_state['chat_id'].strip()
        if chat_id:
            log_message(f"TASK-{task_key}: Opening chat {chat_id}")
            driver.get(f"https://www.facebook.com/messages/t/{chat_id}")
        else:
            driver.get("https://www.facebook.com/messages")
        
        time.sleep(15)
        
        messages_list = st.session_state.automation_state['messages']
        delay = st.session_state.automation_state['delay']
        name_prefix = st.session_state.automation_state['name_prefix']
        
        message_count = 0
        while st.session_state.active_tasks.get(task_key, False):
            base_message = get_next_message(messages_list)
            message_to_send = f"{name_prefix} {base_message}" if name_prefix else base_message
            
            message_input = find_message_input(driver, f"TASK-{task_key}")
            if not message_input:
                time.sleep(10)
                continue
            
            try:
                # Type message
                driver.execute_script("""
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
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                # Send message
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        const events = [
                            new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}),
                            new KeyboardEvent('keypress', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}),
                            new KeyboardEvent('keyup', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true})
                        ];
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                
                message_count += 1
                st.session_state.automation_state['message_count'] = message_count
                log_message(f"TASK-{task_key}: ✅ Message #{message_count} sent: \"{message_to_send[:30]}...\"")
                time.sleep(delay)
                
            except Exception as e:
                log_message(f"TASK-{task_key}: ❌ Error: {str(e)[:100]}")
                time.sleep(5)
        
        log_message(f"TASK-{task_key}: 🛑 Stopped. Total messages: {message_count}")
        
    except Exception as e:
        log_message(f"TASK-{task_key}: 💥 Fatal error: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def start_automation():
    if st.session_state.automation_state['running']:
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
    
    st.success(f"🚀 Automation started! **Task Key: `{task_key}`**")
    st.info("📋 Copy this task key to stop the automation")

def stop_automation():
    task_key = st.session_state.automation_state.get('task_key')
    if task_key and st.session_state.active_tasks.get(task_key):
        st.session_state.active_tasks[task_key] = False
        st.session_state.automation_state['running'] = False
        st.session_state.automation_state['task_key'] = None
        st.rerun()
        st.warning("🛑 Automation stopping...")

# Main UI
st.markdown("""
    <div class="main-header">
        <h1>📱 YKTI RAWAT</h1>
        <p>PREMIUM MESSAGE SENDER - UNLIMITED RUNNING</p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 1, 1])

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
    task_key = st.session_state.automation_state.get('task_key', 'Not Running')
    st.metric("🔑 Task Key", task_key)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Configuration
tab1, tab2 = st.tabs(["⚙️ Configuration", "📊 Live Logs"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Message TXT upload
        uploaded_files = st.file_uploader("📄 Upload Message TXT Files", type=['txt'], accept_multiple_files=True)
        if uploaded_files:
            messages_content = []
            for file in uploaded_files:
                content = file.read().decode('utf-8')
                messages_content.extend([line.strip() for line in content.split('\n') if line.strip()])
            st.session_state.automation_state['messages'] = messages_content
            st.success(f"✅ Loaded {len(messages_content)} messages from {len(uploaded_files)} files")
        
        st.text_input("👤 Name Prefix (optional)", value="", key="name_prefix")
        chat_id = st.text_input("💬 Chat/Conversation ID", placeholder="e.g., 1234567890123456")
        
        cookie_type = st.radio("🍪 Cookie Type:", ["Single Cookie", "Multiple Cookies"])
        if cookie_type == "Single Cookie":
            cookies = st.text_area("Single Cookie", height=100, placeholder="Paste single cookie here")
        else:
            cookies = st.text_area("Multiple Cookies (one per line)", height=150, placeholder="cookie1=value1\ncookie2=value2")
        
        delay = st.number_input("⏱️ Delay (seconds)", min_value=1, max_value=300, value=5)
    
    # Save config
    if st.button("💾 Save Configuration", use_container_width=True):
        st.session_state.automation_state.update({
            'chat_id': chat_id,
            'cookies': cookies,
            'delay': delay,
            'name_prefix': st.session_state.get('name_prefix', '')
        })
        st.success("✅ Configuration saved!")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 START AUTOMATION", use_container_width=True, disabled=st.session_state.automation_state['running']):
            if st.session_state.automation_state['messages'] and st.session_state.automation_state['chat_id']:
                start_automation()
            else:
                st.error("⚠️ Please upload messages and set chat ID first!")
    
    with col_btn2:
        st.text_input("🛑 Stop Task Key", placeholder="Paste task key here to stop")
        if st.button("🛑 STOP BY TASK KEY", use_container_width=True, disabled=not st.session_state.automation_state['running']):
            stop_automation()

with tab2:
    if st.session_state.automation_state['logs']:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        for log in st.session_state.automation_state['logs'][-50:]:
            st.markdown(f'<div class="console-line">{log}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📝 No logs yet. Start automation to see live output!")

# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: white;'>
        <h3>🚀 YKTI RAWAT - PREMIUM MESSAGE SENDER 2026</h3>
        <p>Unlimited running until you stop! Task key for instant control.</p>
    </div>
""", unsafe_allow_html=True)
