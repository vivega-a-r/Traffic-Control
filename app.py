import streamlit as st
import pickle
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Traffic Command v4.0", layout="wide", initial_sidebar_state="collapsed")

# --- ULTRA-FUTURISTIC CSS ---
def apply_ui_style():
    st.markdown("""
        <style>
            /* Base Theme Overrides */
            .stApp {
                background: radial-gradient(circle at top right, #1e293b, #020617);
                color: #e2e8f0;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: rgba(15, 23, 42, 0.8);
                backdrop-filter: blur(10px);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* Glassmorphism Cards */
            .glass-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(15px);
                border-radius: 24px;
                padding: 30px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
                margin-bottom: 20px;
            }

            /* Neon Glow Titles */
            .neon-text {
                text-shadow: 0 0 10px rgba(37, 99, 235, 0.8), 0 0 20px rgba(37, 99, 235, 0.3);
                font-weight: 800;
                letter-spacing: -1px;
            }

            /* Button Styling: Futuristic Blue */
            .stButton > button {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 12px 30px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(37, 99, 235, 0.6) !important;
            }

            /* Metric Styling */
            [data-testid="stMetricValue"] {
                font-family: 'Courier New', monospace;
                color: #60a5fa;
            }
        </style>
    """, unsafe_allow_html=True)

apply_ui_style()

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- PAGE 1: NEON LANDING ---
if st.session_state.page == 'landing':
    st.markdown("""
        <div style="text-align: center; padding: 100px 0;">
            <h1 class="neon-text" style="font-size: 85px; margin-bottom: 0;">NEURAL TRAFFIC</h1>
            <p style="font-size: 22px; color: #94a3b8; margin-bottom: 40px;">Autonomous Logic for the Smart City Grid</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 0.5, 1])
    with col_btn:
        if st.button("INITIALIZE SYSTEM ➔", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 50px; opacity: 0.6;">
            <img src="https://img.icons8.com/nolan/256/traffic-light.png" width="180">
        </div>
    """, unsafe_allow_html=True)

# --- PAGE 2: THE DASHBOARD ---
else:
    # Sidebar
    st.sidebar.markdown("### 🛰️ SYSTEM STATUS")
    st.sidebar.success("Core: ONLINE")
    st.sidebar.divider()
    if st.sidebar.button("LOGOUT"):
        st.session_state.page = 'landing'
        st.rerun()

    # Layout
    head1, head2 = st.columns([3, 1])
    with head1:
        st.markdown("<h1 class='neon-text'>DASHBOARD CONTROL</h1>", unsafe_allow_html=True)
    with head2:
        st.metric("LATENCY", "12ms", "-2ms")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_in, col_res = st.columns([1, 1.5], gap="large")

    with col_in:
        st.markdown("### 📟 Sensor Data")
        cars = st.slider("Car Density", 0, 200, 45)
        bikes = st.slider("Bike Density", 0, 200, 30)
        buses = st.slider("Heavy Transit (Buses)", 0, 100, 12)
        trucks = st.slider("Logistics (Trucks)", 0, 100, 8)
        total = cars + bikes + buses + trucks
        
    with col_res:
        # Dummy Logic for Prediction (Replace with your actual model/scaler calls)
        if total < 50:
            status, color, shadow = "SMOOTH FLOW", "#10b981", "rgba(16, 185, 129, 0.4)"
            timer = 30
        elif total < 120:
            status, color, shadow = "MODERATE", "#f59e0b", "rgba(245, 158, 11, 0.4)"
            timer = 60
        else:
            status, color, shadow = "CONGESTED", "#ef4444", "rgba(239, 68, 68, 0.4)"
            timer = 115

        st.markdown(f"""
            <div style="
                background: rgba(0,0,0,0.3);
                padding: 40px;
                border-radius: 20px;
                border: 2px solid {color};
                box-shadow: 0 0 30px {shadow};
                text-align: center;
            ">
                <p style="color: {color}; font-weight: 800; letter-spacing: 2px; margin: 0;">AI RECOMMENDATION</p>
                <h1 style="font-size: 100px; color: white; margin: 10px 0; font-family: monospace;">{timer}<span style="font-size: 40px;">s</span></h1>
                <div style="background: {color}; color: black; display: inline-block; padding: 5px 20px; border-radius: 50px; font-weight: 900; font-size: 14px;">
                    {status}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Sub-metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="glass-card">Confidence: <b>99.4%</b></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="glass-card">Total Units: <b>' + str(total) + '</b></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="glass-card">Next Sync: <b>0.4s</b></div>', unsafe_allow_html=True)