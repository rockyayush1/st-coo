import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import os
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

st.set_page_config(
    page_title="YKTI RAWAT",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# COMPLETE PREMIUM CSS - FULL WORKING DESIGN
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { 
    font-family: 'Inter', sans-serif !important; 
}

html, body, [class*="css"]  {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 30%, #2d1b69 60%, #00b4d8 100%) !important;
    background-attachment: fixed !important;
}

.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 30%, #2d1b69 60%, #00b4d8 100%) !important;
    background-attachment: fixed !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* Header */
.header-section {
    background: rgba(255,255,255,0.12) !important;
    backdrop-filter: blur(30px) !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 4rem 3rem !important;
    margin-bottom: 3rem !important;
    box-shadow: 0 40px 80px rgba(0,0,0,0.4) !important;
    text-align: center !important;
}

.header-title {
    background: linear-gradient(135deg, #00f5ff, #ff00ff, #00ff88, #00f5ff) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 4.5rem !important;
    font-weight: 900 !important;
    margin: 0 0 1rem 0 !important;
    letter-spacing: -0.03em !important;
    animation: gradientShift 3s ease infinite !important;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.header-subtitle {
    color: rgba(255,255,255,0.95) !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(25px) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    padding: 2.5rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.12) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 20px !important;
    color: white !important;
    padding: 1.5rem !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00f5ff !important;
    box-shadow: 0 0 0 4px rgba(0,245,255,0.25) !important;
    transform: scale(1.02) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 50%, #00ff88 100%) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 1.5rem 3rem !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
    height: auto !important;
    box-shadow: 0 15px 35px rgba(0,245,255,0.4) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 25px 50px rgba(0,245,255,0.6) !important;
}

/* Console */
.live-console {
    background: rgba(0,0,0,0.95) !important;
    border: 2px solid rgba(0,245,255,0.6) !important;
    border-radius: 24px !important;
    color: #00ff88 !important;
    height: 550px !important;
    padding: 2.5rem !important;
    font-family: 'SF Mono', Monaco, 'Courier New', monospace !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    overflow-y: auto !important;
    box-shadow: inset 0 0 40px rgba(0,245,255,0.15) !important;
}

/* Metrics */
.metric-container {
    background: rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    padding: 2.5rem !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}

.metric-container:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 30px 60px rgba(0,0,0,0.4) !important;
}

.metric-value {
    color: #00f5ff !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    margin: 0 !important;
    text-shadow: 0 0 20px rgba(0,245,255,0.5) !important;
}

.metric-label {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-top: 0.5rem !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Session State - NO SAVE CONFIG
if 'automation_state' not in st.session_state:
    st.session_state.automation_state = {
        'running': False,
        'task_key': None,
        'message_count': 0,
        'logs': [],
        'message_rotation_index': 0,
        'messages': [],
        'cookies': '',
        'chat_id': '',
        'delay': 5,
        'name_prefix': ''
    }

if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = {}

def log_message(msg):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    st.session_state.automation_state['logs'].append(formatted_msg)
    if len(st.session_state.automation_state['logs']) > 300:
        st.session_state.automation_state['logs'] = st.session_state.automation_state['logs'][-300:]
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
                    element.dispatchEvent(new InputEvent('input', {bubbles: true, data: message}));
                """, message_input, message_to_send)
                
                time.sleep(1.5)
                
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
        st.error("⚠️ Already running!")
        return
    
    messages = st.session_state.automation_state.get('messages', [])
    chat_id = st.session_state.automation_state.get('chat_id', '').strip()
    cookies = st.session_state.automation_state.get('cookies', '').strip()
    
    if not messages:
        st.error("❌ Upload message TXT files first!")
        return
    if not chat_id:
        st.error("❌ Enter Chat/Conversation ID!")
        return
    if not cookies:
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
    
    st.success(f"🚀 STARTED! **TASK KEY: `{task_key}`** - Copy to stop instantly!")
    st.rerun()

def stop_automation():
    task_key = st.session_state.automation_state.get('task_key')
    if task_key and st.session_state.active_tasks.get(task_key):
        st.session_state.active_tasks[task_key] = False
        st.session_state.automation_state['running'] = False
        st.session_state.automation_state['task_key'] = None
        st.success("🛑 EMERGENCY STOP triggered!")
        st.rerun()

# MAIN UI
st.markdown("""
    <div class="header-section">
        <h1 class="header-title">📱 YKTI RAWAT</h1>
        <p class="header-subtitle">PREMIUM UNLIMITED MESSAGING 2026 • INSTANT START • LIVE LOGS</p>
    </div>
""", unsafe_allow_html=True)

# Live Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="metric-value">{st.session_state.automation_state["message_count"]:,}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">📊 Messages Sent</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    status = "🟢 LIVE" if st.session_state.automation_state['running'] else "🔴 STOPPED"
    st.markdown(f'<h2 class="metric-value">{status}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">⚙️ Status</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    task_key_display = st.session_state.automation_state.get('task_key', 'NO TASK')
    st.markdown(f'<h2 class="metric-value">{task_key_display}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">🔑 Current Task</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Main Tabs
tab1, tab2 = st.tabs(["⚙️ INSTANT SETUP", "📊 LIVE CONSOLE"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
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
                st.success(f"📝 **{len(all_messages)} TOTAL MESSAGES** loaded!")
        
        st.markdown("### 💬 Chat Settings")
        chat_id = st.text_input(
            "🔗 Chat/Conversation ID", 
            placeholder="e.g., 1234567890123456",
            help="Get from Facebook URL: /messages/t/ID/"
        )
        st.session_state.automation_state['chat_id'] = chat_id
        
        name_prefix = st.text_input(
            "✏️ Name Prefix (optional)", 
            placeholder="e.g., YKTI RAWAT"
        )
        st.session_state.automation_state['name_prefix'] = name_prefix
        
        delay = st.number_input(
            "⏱️ Delay (seconds)", 
            min_value=1, 
            max_value=300, 
            value=5
        )
        st.session_state.automation_state['delay'] = delay
    
    with col_config2:
        st.markdown("### 🍪 Facebook Cookies")
        cookies = st.text_area(
            "Paste Cookies Here",
            placeholder="c_user=123...; xs=ABC...; datr=XYZ... (semicolon separated)",
            height=200
        )
        st.session_state.automation_state['cookies'] = cookies
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 START AUTOMATION", use_container_width=True, disabled=st.session_state.automation_state['running']):
            start_automation()
    
    with col_btn2:
        if st.button("🛑 EMERGENCY STOP", use_container_width=True, disabled=not st.session_state.automation_state['running']):
            stop_automation()
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📱 LIVE CONSOLE - Real Time Logs")
    
    st.markdown('<div class="live-console">', unsafe_allow_html=True)
    if st.session_state.automation_state['logs']:
        for log in st.session_state.automation_state['logs'][-100:]:
            st.markdown(f'<div style="margin-bottom: 0.8rem; padding: 0.4rem 0; border-bottom: 1px solid rgba(0,245,255,0.2);">{log}</div>', unsafe_allow_html=True)
    else:
        st.info("👀 **No logs yet** - Click START to begin automation!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 AUTO REFRESH", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🗑️ CLEAR CONSOLE", use_container_width=True):
            st.session_state.automation_state['logs'] = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 3rem 2rem; background: rgba(0,0,0,0.4); border-radius: 24px; margin: 3rem 1rem 1rem 1rem; color: rgba(255,255,255,0.9);'>
    <h3 style='color: #00f5ff; margin-bottom: 1rem;'>🚀 YKTI RAWAT - PREMIUM UNLIMITED MESSAGING 2026</h3>
    <p><strong>✅ No Save Config</strong> • <strong>✅ Premium Gradient Design</strong> • <strong>✅ Live Logs</strong> • <strong>✅ Instant Start/Stop</strong> • <strong>✅ Task Key Control</strong></p>
</div>
""", unsafe_allow_html=True)
