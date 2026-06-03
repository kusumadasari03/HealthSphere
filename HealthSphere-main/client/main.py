import streamlit as st
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import os
import time
from datetime import datetime


load_dotenv()


API_URL=os.getenv("API_URL")

st.set_page_config(
    page_title="HealthSphere - AI Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for healthcare theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-color: #2E8B57;
        --secondary-color: #20B2AA;
        --accent-color: #4682B4;
        --background-color: #F0F8FF;
        --text-color: #2F4F4F;
        --success-color: #28A745;
        --warning-color: #FFC107;
        --error-color: #DC3545;
    }
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #F0F8FF 0%, #E6F3FF 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Role badge styling */
    .role-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 1rem 0;
    }
    
    .role-admin { background: #FF6B6B; color: white; }
    .role-doctor { background: #4ECDC4; color: white; }
    .role-nurse { background: #45B7D1; color: white; }
    .role-patient { background: #96CEB4; color: white; }
    .role-other { background: #FFEAA7; color: #2D3436; }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .user-message {
        background: #F8F9FA;
        border-left: 4px solid #4682B4;
        color: #2F4F4F;
        margin-left: 2rem;
    }
    
    .user-message strong {
        color: #4682B4;
        font-weight: 600;
    }
    
    .bot-message {
        background: #F0F8FF;
        border-left: 4px solid #2E8B57;
        color: #2F4F4F;
        margin-right: 2rem;
    }
    
    .bot-message strong {
        color: #2E8B57;
        font-weight: 600;
    }
    
    /* Chat message hover effects for better UX */
    .chat-message:hover {
        transform: translateX(2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
    }
    
    /* Timestamp styling */
    .chat-message small {
        opacity: 0.7;
        font-size: 0.8rem;
    }
    
    /* Better spacing for conversation history */
    .conversation-history {
        max-height: 400px;
        overflow-y: auto;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Scrollbar styling */
    .conversation-history::-webkit-scrollbar {
        width: 8px;
    }
    
    .conversation-history::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .conversation-history::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    .conversation-history::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
    }
    
    /* Form styling */
    .auth-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Upload area */
    .upload-area {
        background: white;
        border: 2px dashed var(--primary-color);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: #F0F8FF;
        border-color: var(--secondary-color);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error message styling */
    .success-message {
        background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--success-color);
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #F8D7DA, #F5C6CB);
        color: #721C24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--error-color);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
if "username" not in st.session_state:
    st.session_state.username=""
    st.session_state.password=""
    st.session_state.role=""
    st.session_state.logged_in=False
    st.session_state.mode="auth"
    st.session_state.chat_history=[]
    st.session_state.loading=False

# Load custom CSS
load_custom_css()

# Helper functions
def get_role_icon(role):
    icons = {
        "admin": "👨‍💼",
        "doctor": "👨‍⚕️", 
        "nurse": "👩‍⚕️",
        "patient": "🧑‍🦽",
        "other": "👤"
    }
    return icons.get(role, "👤")

def get_role_color(role):
    colors = {
        "admin": "role-admin",
        "doctor": "role-doctor",
        "nurse": "role-nurse", 
        "patient": "role-patient",
        "other": "role-other"
    }
    return colors.get(role, "role-other")

def show_loading():
    st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)

def format_timestamp():
    return datetime.now().strftime("%H:%M")

# Auth header
def get_auth():
    return HTTPBasicAuth(st.session_state.username,st.session_state.password)

# Auth UI
def auth_ui():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 HealthSphere</h1>
        <p>AI-Powered Healthcare Assistant with Role-Based Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        st.markdown("### 🔐 Authentication")

        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

        # Login Tab
        with tab1:
            st.markdown("#### Welcome Back!")
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_login1, col_login2 = st.columns([1, 1])
                with col_login1:
                    login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if login_btn:
                    if not username or not password:
                        st.error("❌ Please fill in all fields")
                    else:
                        with st.spinner("🔄 Authenticating..."):
                            try:
                                res = requests.get(f"{API_URL}/login", auth=HTTPBasicAuth(username, password))
                                if res.status_code == 200:
                                    user_data = res.json()
                                    st.session_state.username = username
                                    st.session_state.password = password
                                    st.session_state.role = user_data["role"]
                                    st.session_state.logged_in = True
                                    st.session_state.mode = "chat"
                                    st.success(f"✅ Welcome back, {username}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {res.json().get('detail', 'Login failed')}")
                            except Exception as e:
                                st.error("❌ Connection error. Please try again.")

        # Signup Tab
        with tab2:
            st.markdown("#### Create New Account")
            
            with st.form("signup_form"):
                new_user = st.text_input("👤 Username", placeholder="Choose a username")
                new_pass = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                confirm_pass = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
                new_role = st.selectbox("👔 Role", ["admin", "doctor", "nurse", "patient", "other"],
                                      help="Select your role in the healthcare system")
                
                signup_btn = st.form_submit_button("📝 Create Account", use_container_width=True)
                
                if signup_btn:
                    if not all([new_user, new_pass, confirm_pass]):
                        st.error("❌ Please fill in all fields")
                    elif new_pass != confirm_pass:
                        st.error("❌ Passwords don't match")
                    elif len(new_pass) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        with st.spinner("🔄 Creating account..."):
                            try:
                                payload = {"username": new_user, "password": new_pass, "role": new_role}
                                res = requests.post(f"{API_URL}/signup", json=payload)
                                if res.status_code == 200:
                                    st.success("✅ Account created successfully! Please login.")
                                else:
                                    st.error(f"❌ {res.json().get('detail', 'Signup failed')}")
                            except Exception as e:
                                st.error("❌ Connection error. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)



# Upload PDF (Admin only)
def upload_docs():
    st.markdown("### 📄 Document Management")
    
    with st.container():
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "📁 Choose a PDF file", 
                type=["pdf"],
                help="Upload medical documents, guidelines, or resources"
            )
        
        with col2:
            role_for_doc = st.selectbox(
                "🎯 Target Role", 
                ["doctor", "nurse", "patient", "other"],
                help="Select which role can access this document"
            )
        
        if uploaded_file:
            st.info(f"📋 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            col_upload1, col_upload2 = st.columns([1, 3])
            with col_upload1:
                if st.button("📤 Upload Document", use_container_width=True):
                    with st.spinner("⏳ Uploading document..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                            data = {"role": role_for_doc}
                            res = requests.post(f"{API_URL}/upload_docs", files=files, data=data, auth=get_auth())
                            
                            if res.status_code == 200:
                                doc_info = res.json()
                                st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
                                st.info(f"📊 Document ID: {doc_info['doc_id']} | Access: {doc_info['accessible_to']}")
                            else:
                                st.error(f"❌ {res.json().get('detail', 'Upload failed')}")
                        except Exception as e:
                            st.error("❌ Connection error during upload")
        
        st.markdown('</div>', unsafe_allow_html=True)



# Enhanced chat interface
def chat_interface():
    st.markdown("### 💬 AI Healthcare Assistant")
    
    # Chat history display
    if st.session_state.chat_history:
        st.markdown("#### 📋 Conversation History")
        
        # Create a scrollable chat container
        st.markdown('<div class="conversation-history">', unsafe_allow_html=True)
        chat_container = st.container()
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                timestamp = chat.get('timestamp', '')
                
                # User message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>� You</strong> <small>({timestamp})</small><br>
                    {chat['question']}
                </div>
                """, unsafe_allow_html=True)
                
                # Bot response
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🔬 HealthSphere AI</strong><br>
                    {chat['answer']}
                </div>
                """, unsafe_allow_html=True)
                
                # Sources if available
                if chat.get('sources'):
                    with st.expander("📚 Sources"):
                        for src in chat['sources']:
                            st.write(f"• {src}")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close conversation-history div
        
        # Clear history button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.divider()
    
    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        st.markdown("#### 💭 Ask a Healthcare Question")
        
        msg = st.text_area(
            "Your question:",
            placeholder="Ask about symptoms, treatments, medications, or any healthcare-related topic...",
            help="Be specific about your question for better results"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            send_btn = st.form_submit_button("🚀 Send Query", use_container_width=True)
        
        if send_btn and msg.strip():
            timestamp = format_timestamp()
            
            with st.spinner("🔄 AI is thinking..."):
                try:
                    res = requests.post(f"{API_URL}/chat", data={"message": msg}, auth=get_auth())
                    
                    if res.status_code == 200:
                        reply = res.json()
                        
                        # Add to chat history
                        chat_entry = {
                            'question': msg,
                            'answer': reply["answer"],
                            'sources': reply.get("sources", []),
                            'timestamp': timestamp
                        }
                        st.session_state.chat_history.append(chat_entry)
                        
                        # Display immediate response
                        st.markdown("### 🎯 Response:")
                        st.success(reply["answer"])
                        
                        if reply.get("sources"):
                            with st.expander("📚 View Sources"):
                                for src in reply["sources"]:
                                    st.write(f"• {src}")
                        
                        # Copy to clipboard button
                        st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText('{reply["answer"]}')" 
                                style="background: var(--primary-color); color: white; border: none; 
                                       padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                            📋 Copy Response
                        </button>
                        """, unsafe_allow_html=True)
                        
                        st.rerun()
                    else:
                        st.error(f"❌ {res.json().get('detail', 'Something went wrong')}")
                        
                except Exception as e:
                    st.error("❌ Connection error. Please try again.")
        
        elif send_btn and not msg.strip():
            st.warning("⚠️ Please enter a question before sending")


# Enhanced main application flow
def main_dashboard():
    # Header with user info
    st.markdown(f"""
    <div class="main-header">
        <h1>🏥 HealthSphere Dashboard</h1>
        <p>Welcome back, <strong>{st.session_state.username}</strong></p>
        <div class="role-badge {get_role_color(st.session_state.role)}">
            {get_role_icon(st.session_state.role)} {st.session_state.role.upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with navigation and user controls
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # User info in sidebar
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <strong>👤 {st.session_state.username}</strong><br>
            <span class="role-badge {get_role_color(st.session_state.role)}" style="font-size: 0.8rem; padding: 0.2rem 0.5rem;">
                {st.session_state.role.upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        if st.session_state.role == "admin":
            page = st.selectbox("📋 Select Page", ["💬 Chat Assistant", "📄 Document Management", "📊 Analytics"])
        else:
            page = st.selectbox("📋 Select Page", ["💬 Chat Assistant", "ℹ️ Help & Info"])
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        st.metric("💬 Chat Messages", len(st.session_state.chat_history))
    
    # Main content area
    if page == "💬 Chat Assistant":
        chat_interface()
    elif page == "📄 Document Management" and st.session_state.role == "admin":
        upload_docs()
    elif page == "ℹ️ Help & Info":
        show_help_page()
    elif page == "📊 Analytics" and st.session_state.role == "admin":
        show_analytics()

def show_help_page():
    st.markdown("### ℹ️ Help & Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🤖 How to Use HealthSphere AI
        
        **Ask Questions Like:**
        - What are the symptoms of diabetes?
        - How to treat high blood pressure?
        - Side effects of aspirin
        - Emergency procedures for heart attack
        
        **Tips for Better Results:**
        - Be specific in your questions
        - Include relevant symptoms or conditions
        - Ask one question at a time
        """)
    
    with col2:
        st.markdown("""
        #### 🔒 Your Role Permissions
        
        **As a {role}:**
        - Access role-specific medical information
        - Get personalized healthcare responses  
        - View relevant treatment guidelines
        - Safe and secure data handling
        
        **Need Help?**
        Contact your system administrator for additional access or support.
        """.format(role=st.session_state.role.title()))

def show_analytics():
    st.markdown("### 📊 System Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Users", "47", "+3")
    with col2:
        st.metric("📄 Documents", "23", "+2")
    with col3:
        st.metric("💬 Messages Today", "156", "+12")
    
    st.markdown("#### 📈 Usage Statistics")
    st.info("📊 Advanced analytics coming soon...")

# Main application flow
if not st.session_state.logged_in:
    auth_ui()
else:
    # Set login time if not set
    if 'login_time' not in st.session_state:
        st.session_state.login_time = time.time()
    
    main_dashboard()
