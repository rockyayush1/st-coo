import streamlit as st
import requests
import threading
import time
import random
import string
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="✨𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Theme CSS with Live Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
        position: relative;
        overflow: hidden;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120,119,198,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,119,198,0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120,219,255,0.2) 0%, transparent 50%);
        z-index: 0;
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .stApp {
        background: transparent;
        backdrop-filter: blur(10px);
        font-family: 'Orbitron', monospace;
    }
    
    .premium-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(45deg, #00d4ff, #ff00ff, #00ff88, #ffaa00);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 20px 0;
        padding: 20px;
        text-shadow: 0 0 30px rgba(0,212,255,0.5);
        position: relative;
        z-index: 10;
    }
    
    .metric-container {
        background: rgba(15, 15, 25, 0.9) !important;
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    
    .glass-panel {
        background: rgba(20, 20, 40, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 25px 50px rgba(0,0,0,0.6);
        position: relative;
        z-index: 10;
    }
    
    .live-log {
        background: rgba(10, 10, 25, 0.95) !important;
        backdrop-filter: blur(25px);
        border: 2px solid rgba(0,255,136,0.4);
        border-radius: 20px;
        padding: 25px;
        height: 500px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: inset 0 0 30px rgba(0,255,136,0.1);
    }
    
    .log-success { color: #00ff88 !important; font-weight: 600; }
    .log-error { color: #ff4757 !important; font-weight: 600; }
    .log-info { color: #00d4ff !important; font-weight: 500; }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div,
    .stNumberInput > div > div > input {
        background: rgba(10, 10, 25, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0,212,255,0.5) !important;
        border-radius: 15px !important;
        padding: 12px 15px !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0,212,255,0.4) !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099ff) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 15px 30px !important;
        font-family: 'Orbitron', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 10px 30px rgba(0,212,255,0.4) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #0099ff, #00d4ff) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(0,212,255,0.6) !important;
    }
    
    .task-table {
        background: rgba(15, 15, 25, 0.9);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(0,212,255,0.3);
    }
    
    .status-running { color: #00ff88 !important; font-weight: bold; }
    .status-stopped { color: #ff4757 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Headers
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'https://www.facebook.com/'
}

PRELOADED_FILES = {
    "Rishi Premium": ["🔥 RISHI PRO", "⚡ LIVE MODE", "✨ PREMIUM", "💎 ELITE", "🚀 ULTRA"],
    "Pro Messages": ["PRO ACTIVE", "ELITE MODE", "PREMIUM LIVE", "ULTRA FAST", "VIP ACCESS"]
}

# Session State
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}
if 'stop_events' not in st.session_state:
    st.session_state.stop_events = {}
if 'active_threads' not in st.session_state:
    st.session_state.active_threads = {}
if 'message_log' not in st.session_state:
    st.session_state.message_log = []
if 'total_messages_sent' not in st.session_state:
    st.session_state.total_messages_sent = 0
if 'log_placeholder' not in st.session_state:
    st.session_state.log_placeholder = None

def send_messages(cookies_list, thread_id, mn, time_interval, messages, task_id):
    stop_event = st.session_state.stop_events[task_id]
    st.session_state.tasks[task_id] = {
        "status": "Running", 
        "start_time": datetime.now(),
        "messages_sent": 0,
        "cookies_used": len(cookies_list)
    }
    
    message_count = 0
    cookie_index = 0
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
                
            if cookie_index >= len(cookies_list):
                cookie_index = 0
                
            cookie = cookies_list[cookie_index]
            cookie_index += 1
            
            try:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                
                session = requests.Session()
                cookie_dict = {}
                for c in cookie.strip().split(';'):
                    if '=' in c:
                        key, value = c.strip().split('=', 1)
                        cookie_dict[key] = value
                
                session.cookies.update(cookie_dict)
                session.headers.update(headers)
                
                parameters = {'message': message}
                response = session.post(api_url, data=parameters)
                
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if response.status_code == 200:
                    log_message = f"✅ [{current_time}] {message[:50]}... | SENT SUCCESSFULLY"
                    st.session_state.message_log.append(("success", log_message))
                    message_count += 1
                    st.session_state.tasks[task_id]["messages_sent"] = message_count
                    st.session_state.total_messages_sent += 1
                else:
                    log_message = f"❌ [{current_time}] FAILED | Status: {response.status_code}"
                    st.session_state.message_log.append(("error", log_message))
                
                # Keep last 100 logs
                if len(st.session_state.message_log) > 100:
                    st.session_state.message_log.pop(0)
                    
                time.sleep(time_interval)
                
            except Exception as e:
                current_time = datetime.now().strftime("%H:%M:%S")
                log_message = f"⚠️ [{current_time}] ERROR: {str(e)[:50]}..."
                st.session_state.message_log.append(("error", log_message))
                time.sleep(2)
    
    st.session_state.tasks[task_id]["status"] = "Stopped"

def start_task(cookies_list, thread_id, mn, time_interval, messages):
    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    st.session_state.stop_events[task_id] = threading.Event()
    
    thread = threading.Thread(
        target=send_messages, 
        args=(cookies_list, thread_id, mn, time_interval, messages, task_id),
        name=f"Task_{task_id}"
    )
    thread.daemon = True
    thread.start()
    
    st.session_state.active_threads[task_id] = thread
    return task_id

def stop_task(task_id):
    if task_id in st.session_state.stop_events:
        st.session_state.stop_events[task_id].set()
        return True
    return False

def stop_all_tasks():
    for task_id in list(st.session_state.stop_events.keys()):
        stop_task(task_id)

# LIVE LOG UPDATER
def update_live_logs():
    if st.session_state.log_placeholder:
        with st.session_state.log_placeholder.container():
            st.markdown('<div class="live-log">', unsafe_allow_html=True)
            
            if st.session_state.message_log:
                for log_type, log_msg in reversed(st.session_state.message_log[-30:]):
                    if log_type == "success":
                        st.markdown(f'<div class="log-success">{log_msg}</div>', unsafe_allow_html=True)
                    elif log_type == "error":
                        st.markdown(f'<div class="log-error">{log_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="log-info">{log_msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="log-info">🚀 Waiting for messages... LIVE MODE ACTIVE</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# MAIN APP
st.markdown('<div class="premium-title">✨ 𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎 𝐗-𝐒𝐄𝐑𝐕𝐄𝐑 ✨</div>', unsafe_allow_html=True)

# DASHBOARD METRICS
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("🔥 LIVE TASKS", len([t for t in st.session_state.tasks.values() if t.get("status") == "Running"]))
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("📨 TOTAL SENT", st.session_state.total_messages_sent)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    active_threads = len([t for t in threading.enumerate() if t.name.startswith("Task_")])
    st.metric("⚡ LIVE THREADS", active_threads)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    total_cookies = sum(task.get("cookies_used", 0) for task in st.session_state.tasks.values())
    st.metric("🍪 COOKIES LOADED", total_cookies)
    st.markdown('</div>', unsafe_allow_html=True)

# CREATE TASK FORM
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 🚀 𝐋𝐈𝐕𝐄 𝐏𝐑𝐎 𝐓𝐀𝐒𝐊 𝐂𝐑𝐄𝐀𝐓𝐎𝐑")
with st.form("pro_form"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🍪 𝐏𝐑𝐎 𝐂𝐎𝐎𝐊𝐈𝐄𝐒")
        cookie_text = st.text_area("Paste FB Cookies", height=100, placeholder="datr=...; sb=...; c_user=...")
        cookies_list = [cookie_text.strip()] if cookie_text.strip() else []
    
    with col2:
        st.markdown("#### 💬 𝐓𝐀𝐑𝐆𝐄𝐓")
        thread_id = st.text_input("Conversation UID", placeholder="t_xxxxxxxxxx")
        sender_name = st.text_input("Sender Name", placeholder="RISHI PRO")
    
    time_interval = st.slider("⚡ Speed (seconds)", 1, 30, 3)
    
    st.markdown("#### 📝 𝐏𝐑𝐎 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
    selected_messages = st.selectbox("Message Pack", list(PRELOADED_FILES.keys()))
    messages = PRELOADED_FILES[selected_messages]
    
    col1, col2 = st.columns([1,3])
    with col2:
        start_btn = st.form_submit_button("🚀 𝐒𝐓𝐀𝐑𝐓 𝐏𝐑𝐎 𝐒𝐄𝐑𝐕𝐄𝐑 🚀", use_container_width=True)
    
    if start_btn:
        if cookies_list and thread_id and sender_name and messages:
            task_id = start_task(cookies_list, thread_id, sender_name, time_interval, messages)
            st.success(f"✅ PRO TASK **{task_id}** LIVE! 🚀")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Complete all fields!")

st.markdown('</div>', unsafe_allow_html=True)

# CONTROL PANEL
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 🎮 𝐏𝐑𝐎 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋")
col1, col2 = st.columns(2)
with col1:
    with st.form("control_form"):
        task_id = st.text_input("Task ID", placeholder="Enter Task ID")
        stop_btn = st.form_submit_button("🛑 STOP TASK")
        if stop_btn and task_id:
            if stop_task(task_id):
                st.success(f"✅ Task {task_id} STOPPED!")
                st.rerun()

with col2:
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("⚠️ STOP ALL", use_container_width=True):
            stop_all_tasks()
            st.warning("🔴 ALL TASKS STOPPED!")
            st.rerun()
    with col_btn2:
        if st.button("🗑️ CLEAR LOGS", use_container_width=True):
            st.session_state.message_log = []
            st.success("✅ LOGS CLEARED!")
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ACTIVE TASKS
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 📊 𝐋𝐈𝐕𝐄 𝐓𝐀𝐒𝐊 𝐃𝐀𝐒𝐇𝐁𝐎𝐀𝐑𝐃")
if st.session_state.tasks:
    tasks_data = []
    for task_id, info in st.session_state.tasks.items():
        status_class = "status-running" if info["status"] == "Running" else "status-stopped"
        tasks_data.append({
            "🆔 ID": task_id,
            "📊 Status": f'<span class="{status_class}">{info["status"]}</span>',
            "📨 Sent": info.get("messages_sent", 0),
            "🍪 Cookies": info.get("cookies_used", 0),
            "⏱️ Duration": str(datetime.now() - info["start_time"]).split('.')[0]
        })
    st.markdown('<div class="task-table">', unsafe_allow_html=True)
    st.dataframe(tasks_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📭 No active PRO tasks. Create one above!")
st.markdown('</div>', unsafe_allow_html=True)

# LIVE LOGS - FIXED VERSION
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 📡 𝐋𝐈𝐕𝐄 𝐏𝐑𝐎 𝐋𝐎𝐆𝐒 ✨")
st.session_state.log_placeholder = st.empty()
update_live_logs()
st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style='
    text-align: center; 
    padding: 30px; 
    color: rgba(0,212,255,0.8); 
    font-family: Orbitron; 
    font-size: 14px;
    border-top: 1px solid rgba(0,212,255,0.3);
    margin-top: 40px;
'>
    ✨ 𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎 𝐗-𝐒𝐄𝐑𝐕𝐄𝐑 | 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐄𝐝𝐢𝐭𝐢𝐨𝐧 ✨
</div>
""", unsafe_allow_html=True)
