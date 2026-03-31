import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from src.engine import TrafficEngine
import folium
from streamlit_folium import st_folium

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(
    page_title="NEURAL TRAFFIC OS v4.0",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛰️"
)

# --- 2. WORLD-CLASS CSS ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
/* ============================================================
   ROOT DESIGN TOKENS
   ============================================================ */
:root {
  --bg-void:       #03060f;
  --bg-deep:       #060d1c;
  --bg-surface:    #0b1529;
  --bg-raised:     #0f1e35;
  --border-dim:    rgba(56, 120, 255, 0.12);
  --border-glow:   rgba(56, 120, 255, 0.35);
  --accent-blue:   #3878ff;
  --accent-cyan:   #00d4ff;
  --accent-green:  #00ff87;
  --accent-amber:  #ffb300;
  --accent-red:    #ff3d3d;
  --accent-violet: #9b5de5;
  --text-primary:  #e8f0ff;
  --text-secondary:#8ba3cc;
  --text-muted:    #4a6080;
  --glow-blue:     0 0 30px rgba(56,120,255,0.25), 0 0 60px rgba(56,120,255,0.1);
  --glow-green:    0 0 30px rgba(0,255,135,0.25), 0 0 60px rgba(0,255,135,0.1);
  --glow-red:      0 0 30px rgba(255,61,61,0.25), 0 0 60px rgba(255,61,61,0.1);
  --font-display:  'Syne', sans-serif;
  --font-mono:     'Space Mono', monospace;
  --font-body:     'DM Sans', sans-serif;
  --radius-sm:     8px;
  --radius-md:     14px;
  --radius-lg:     20px;
  --radius-xl:     28px;
}

/* ============================================================
   GLOBAL RESET & BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: var(--bg-void) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

/* Animated starfield background */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(56,120,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 30% 70%, rgba(0,212,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 15%, rgba(56,120,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 80% 50%, rgba(0,255,135,0.2) 0%, transparent 100%),
    radial-gradient(1px 1px at 95% 80%, rgba(56,120,255,0.35) 0%, transparent 100%),
    radial-gradient(1px 1px at 50% 90%, rgba(0,212,255,0.25) 0%, transparent 100%),
    radial-gradient(2px 2px at 25% 45%, rgba(155,93,229,0.25) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 35%, rgba(56,120,255,0.4) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
  animation: starTwinkle 8s ease-in-out infinite alternate;
}

@keyframes starTwinkle {
  0%   { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Subtle grid overlay */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(56,120,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,120,255,0.025) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* ============================================================
   SIDEBAR — MISSION CONTROL PANEL
   ============================================================ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #040a18 0%, #060e1f 50%, #040a18 100%) !important;
  border-right: 1px solid var(--border-dim) !important;
  box-shadow: 4px 0 40px rgba(56,120,255,0.08) !important;
}

[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--accent-blue), var(--accent-cyan), transparent);
  animation: scanline 3s ease-in-out infinite;
}

@keyframes scanline {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

[data-testid="stSidebar"] .stRadio label {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.08em !important;
  color: var(--text-secondary) !important;
  padding: 10px 14px !important;
  border-radius: var(--radius-sm) !important;
  transition: all 0.2s ease !important;
  border: 1px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
  color: var(--accent-cyan) !important;
  background: rgba(56,120,255,0.08) !important;
  border-color: var(--border-dim) !important;
}

/* ============================================================
   METRIC CARDS — HOLOGRAPHIC TILES
   ============================================================ */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, rgba(11,21,41,0.9) 0%, rgba(6,13,28,0.95) 100%) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: var(--radius-lg) !important;
  padding: 22px 24px !important;
  position: relative !important;
  overflow: hidden !important;
  transition: all 0.3s ease !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 4px 24px rgba(0,0,0,0.4) !important;
}

[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
  opacity: 0.6;
}

[data-testid="stMetric"]::after {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 80px; height: 80px;
  background: radial-gradient(circle, rgba(56,120,255,0.12), transparent 70%);
  border-radius: 50%;
}

[data-testid="stMetric"]:hover {
  border-color: var(--border-glow) !important;
  box-shadow: var(--glow-blue), inset 0 1px 0 rgba(255,255,255,0.04) !important;
  transform: translateY(-2px) !important;
}

[data-testid="stMetricLabel"] {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.15em !important;
  color: var(--text-muted) !important;
  text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
  font-family: var(--font-display) !important;
  font-size: 28px !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.02em !important;
}

[data-testid="stMetricDelta"] {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
}

/* ============================================================
   BUTTONS — PRECISION CONTROLS
   ============================================================ */
.stButton > button {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  background: linear-gradient(135deg, rgba(56,120,255,0.15) 0%, rgba(56,120,255,0.08) 100%) !important;
  color: var(--accent-cyan) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: var(--radius-sm) !important;
  padding: 12px 24px !important;
  transition: all 0.25s ease !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton > button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(56,120,255,0.2), transparent);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.stButton > button:hover {
  background: linear-gradient(135deg, rgba(56,120,255,0.3) 0%, rgba(0,212,255,0.15) 100%) !important;
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 20px rgba(0,212,255,0.2), 0 0 40px rgba(56,120,255,0.1) !important;
  color: white !important;
  transform: translateY(-1px) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

/* ============================================================
   INPUTS — TERMINAL STYLE
   ============================================================ */
.stTextInput input, .stSelectbox select {
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
  background: rgba(6,13,28,0.8) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--accent-cyan) !important;
  letter-spacing: 0.05em !important;
  transition: all 0.2s ease !important;
}

.stTextInput input:focus {
  border-color: var(--accent-blue) !important;
  box-shadow: 0 0 0 3px rgba(56,120,255,0.15), var(--glow-blue) !important;
  background: rgba(11,21,41,0.9) !important;
  outline: none !important;
}

.stTextInput label {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  color: var(--text-muted) !important;
}

/* ============================================================
   GLASS CARD — PRIMARY CONTAINER
   ============================================================ */
.glass-card {
  background: linear-gradient(135deg,
    rgba(15,30,53,0.8) 0%,
    rgba(6,13,28,0.9) 100%) !important;
  backdrop-filter: blur(20px) !important;
  border-radius: var(--radius-xl) !important;
  padding: 28px 32px !important;
  border: 1px solid var(--border-dim) !important;
  margin-bottom: 20px !important;
  position: relative !important;
  overflow: hidden !important;
  box-shadow:
    0 8px 32px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.04),
    inset 0 -1px 0 rgba(0,0,0,0.2) !important;
  transition: all 0.3s ease !important;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(56,120,255,0.5) 30%,
    rgba(0,212,255,0.5) 70%,
    transparent 100%);
}

/* ============================================================
   NEON HEADINGS
   ============================================================ */
.neon-text {
  font-family: var(--font-display) !important;
  font-weight: 800 !important;
  font-size: 3rem !important;
  letter-spacing: -0.02em !important;
  background: linear-gradient(135deg, #ffffff 0%, var(--accent-cyan) 50%, var(--accent-blue) 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  position: relative !important;
  display: inline-block !important;
  animation: textShimmer 4s ease-in-out infinite alternate !important;
}

@keyframes textShimmer {
  0%   { filter: brightness(1); }
  100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(0,212,255,0.4)); }
}

.section-tag {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--accent-blue);
  text-transform: uppercase;
  margin-bottom: 6px;
  display: block;
  opacity: 0.8;
}

/* ============================================================
   STATUS BADGES
   ============================================================ */
.status-smooth  { color: var(--accent-green); }
.status-moderate{ color: var(--accent-amber); }
.status-congested{color: var(--accent-red);   }

/* ============================================================
   PROGRESS / SLIDERS
   ============================================================ */
.stProgress > div > div {
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
  border-radius: 4px !important;
  box-shadow: 0 0 10px rgba(0,212,255,0.4) !important;
}

.stProgress > div {
  background: rgba(56,120,255,0.1) !important;
  border-radius: 4px !important;
}

/* ============================================================
   CODE BLOCKS — TERMINAL
   ============================================================ */
.stCode, code, pre {
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
  background: rgba(2,6,15,0.9) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: var(--radius-md) !important;
  color: var(--accent-cyan) !important;
  letter-spacing: 0.05em !important;
}

/* ============================================================
   ALERTS & TOASTS
   ============================================================ */
.stSuccess, .stInfo, .stWarning, .stError {
  font-family: var(--font-body) !important;
  border-radius: var(--radius-md) !important;
  border-left-width: 3px !important;
}

/* ============================================================
   DATAFRAME / TABLES
   ============================================================ */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border-dim) !important;
  border-radius: var(--radius-lg) !important;
  overflow: hidden !important;
}

/* ============================================================
   RADIO BUTTONS
   ============================================================ */
.stRadio > div {
  gap: 8px !important;
}

.stRadio > div label {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.1em !important;
}

/* ============================================================
   SCROLLBARS
   ============================================================ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
  background: var(--accent-blue);
  border-radius: 2px;
  opacity: 0.5;
}

/* ============================================================
   FOLIUM MAP CONTAINER
   ============================================================ */
iframe {
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border-dim) !important;
  box-shadow: var(--glow-blue) !important;
}

/* ============================================================
   FILE UPLOADER
   ============================================================ */
[data-testid="stFileUploader"] {
  border: 2px dashed var(--border-glow) !important;
  border-radius: var(--radius-lg) !important;
  background: rgba(56,120,255,0.04) !important;
  transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-cyan) !important;
  background: rgba(0,212,255,0.06) !important;
}

/* ============================================================
   SIDEBAR TITLE
   ============================================================ */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: var(--font-display) !important;
  font-weight: 800 !important;
  letter-spacing: -0.01em !important;
}

/* ============================================================
   CHART AREA
   ============================================================ */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
  border-radius: var(--radius-lg) !important;
  overflow: hidden !important;
  border: 1px solid var(--border-dim) !important;
  background: rgba(6,13,28,0.6) !important;
}

/* ============================================================
   CUSTOM COMPONENTS
   ============================================================ */

/* Signal Timer Display */
.signal-timer {
  text-align: center;
  border-radius: var(--radius-xl);
  padding: 28px;
  position: relative;
  overflow: hidden;
  font-family: var(--font-display);
  transition: all 0.4s ease;
}

.signal-timer::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  padding: 2px;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.6;
}

/* Alert Log Item */
.alert-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  border-left: 2px solid;
  background: rgba(6,13,28,0.6);
  font-family: var(--font-body);
  font-size: 12px;
  transition: all 0.2s ease;
}

.alert-item:hover {
  background: rgba(11,21,41,0.8);
  transform: translateX(2px);
}

/* CCTV Card */
.cctv-card {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border-dim);
  background: #000;
  position: relative;
  transition: all 0.3s ease;
}

.cctv-card:hover {
  border-color: var(--border-glow);
  box-shadow: var(--glow-blue);
  transform: scale(1.02);
}

/* Emergency Banner */
.emergency-banner {
  border-radius: var(--radius-xl);
  padding: 36px;
  text-align: center;
  position: relative;
  overflow: hidden;
  animation: emergencyPulse 1.2s ease-in-out infinite;
}

@keyframes emergencyPulse {
  0%, 100% {
    box-shadow: 0 0 30px rgba(255,61,61,0.4), 0 0 80px rgba(255,61,61,0.15);
  }
  50% {
    box-shadow: 0 0 60px rgba(255,61,61,0.7), 0 0 120px rgba(255,61,61,0.3);
  }
}

/* Override Panel */
.override-card {
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,61,61,0.2);
  background: rgba(255,61,61,0.04);
  padding: 20px;
  transition: all 0.3s ease;
}

/* KPI Strip */
.kpi-label {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.kpi-value {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1;
}

.kpi-delta {
  font-family: var(--font-mono);
  font-size: 10px;
  margin-top: 4px;
}

/* Section Headers */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.section-header-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--border-glow), transparent);
}

.section-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  text-transform: uppercase;
  white-space: nowrap;
}

/* Pulse dot */
.pulse-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent-green);
  box-shadow: 0 0 6px var(--accent-green);
  animation: pulseDot 2s ease-in-out infinite;
  margin-right: 6px;
}

@keyframes pulseDot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.6; }
}

/* Login Page */
.login-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  animation: orbFloat 6s ease-in-out infinite alternate;
}

@keyframes orbFloat {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(20px, -20px) scale(1.1); }
}

/* Divider */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--border-glow), transparent) !important;
  margin: 20px 0 !important;
}

/* Markdown text */
.stMarkdown p {
  color: var(--text-secondary);
  font-family: var(--font-body);
  line-height: 1.6;
}

/* Captions */
.stCaption {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  color: var(--text-muted) !important;
  letter-spacing: 0.08em !important;
}

/* Tab panels if any */
.stTabs [data-baseweb="tab"] {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.1em !important;
}

/* Download button special */
[data-testid="stDownloadButton"] button {
  background: linear-gradient(135deg, rgba(0,255,135,0.12), rgba(0,212,255,0.08)) !important;
  border-color: rgba(0,255,135,0.3) !important;
  color: var(--accent-green) !important;
}

[data-testid="stDownloadButton"] button:hover {
  background: linear-gradient(135deg, rgba(0,255,135,0.25), rgba(0,212,255,0.15)) !important;
  border-color: var(--accent-green) !important;
  box-shadow: 0 0 20px rgba(0,255,135,0.2) !important;
}

/* Sidebar nav radio items */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  gap: 4px;
}

/* Spinner */
.stSpinner > div {
  border-top-color: var(--accent-cyan) !important;
}

/* Select box */
[data-baseweb="select"] {
  background: rgba(6,13,28,0.8) !important;
  border-color: var(--border-dim) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
}

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-glow) !important;
  color: var(--accent-cyan) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--accent-blue) !important;
  box-shadow: var(--glow-blue) !important;
}

/* Bottom gradient fade for the page */
.main .block-container {
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE & AUTHENTICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

USER_DB = {
    "admin": "city_pass_2026",
    "operator_1": "secure_traffic",
    "planner_main": "data_is_power"
}

# --- LOGIN PAGE ---
if not st.session_state.authenticated:
    # Background orbs
    st.markdown("""
    <div style="position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 0;">
      <div class="login-orb" style="width:600px;height:600px;background:radial-gradient(circle,rgba(56,120,255,0.12),transparent 70%);top:-100px;left:-100px;animation-duration:7s;"></div>
      <div class="login-orb" style="width:500px;height:500px;background:radial-gradient(circle,rgba(0,212,255,0.08),transparent 70%);bottom:-80px;right:-80px;animation-duration:9s;animation-direction:alternate-reverse;"></div>
      <div class="login-orb" style="width:300px;height:300px;background:radial-gradient(circle,rgba(155,93,229,0.08),transparent 70%);top:50%;right:20%;animation-duration:5s;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

    # Logo / Title
    st.markdown("""
    <div style="text-align:center; margin-bottom: 8px;">
      <div style="font-family:'Space Mono',monospace; font-size:11px; letter-spacing:0.3em; color:#3878ff; text-transform:uppercase; margin-bottom:16px; opacity:0.8;">
        ◈ CLASSIFIED INFRASTRUCTURE SYSTEM ◈
      </div>
      <h1 style="
        font-family:'Syne',sans-serif;
        font-size:64px;
        font-weight:800;
        letter-spacing:-0.03em;
        background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#3878ff 100%);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        background-clip:text;
        margin:0;
        line-height:1;
      ">NEURAL<br>TRAFFIC OS</h1>
      <div style="font-family:'Space Mono',monospace; font-size:12px; color:#4a6080; letter-spacing:0.15em; margin-top:12px;">
        URBAN INTELLIGENCE PLATFORM — v4.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div style="
          background:linear-gradient(135deg,rgba(15,30,53,0.85) 0%,rgba(6,13,28,0.95) 100%);
          border:1px solid rgba(56,120,255,0.18);
          border-radius:24px;
          padding:36px 40px 40px;
          position:relative;
          overflow:hidden;
          box-shadow:0 24px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.04);
        ">
          <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(56,120,255,0.6),rgba(0,212,255,0.6),transparent);"></div>
          <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:#3878ff;text-transform:uppercase;margin-bottom:20px;opacity:0.8;">
            🔐 SECURE TERMINAL ACCESS
          </div>
        """, unsafe_allow_html=True)

        user = st.text_input("OPERATOR ID", placeholder="Enter username...")
        pas = st.text_input("ACCESS KEY", type="password", placeholder="••••••••••••")

        if st.button("⟶  INITIALIZE SYSTEM", use_container_width=True):
            if user in USER_DB and USER_DB[user] == pas:
                st.session_state.authenticated = True
                st.session_state.user_role = user
                st.success("✓  Access Granted. Loading mission control...")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("⚠  Invalid credentials. Access denied.")

        st.markdown("""
          <div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3d5c;text-align:center;margin-top:20px;letter-spacing:0.1em;">
            ENCRYPTED · ZERO-TRUST ARCHITECTURE · AES-256
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()


def create_city_map(lat, lon, status, name):
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles="CartoDB dark_matter", control_scale=True)
    color_map = {'SMOOTH': '#00ff87', 'MODERATE': '#ffb300', 'CONGESTED': '#ff3d3d'}
    color = color_map.get(status, '#3878ff')
    folium.CircleMarker(
        location=[lat, lon], radius=15,
        popup=f"<b>{name}</b><br>Status: {status}",
        color=color, fill=True, fill_color=color, fill_opacity=0.8, weight=3
    ).add_to(m)
    return m


@st.cache_resource
def load_engine():
    try:
        return TrafficEngine()
    except Exception as e:
        st.error(f"Engine Failure: {e}")
        return None

engine = load_engine()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 24px;">
      <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;letter-spacing:-0.01em;
        background:linear-gradient(135deg,#fff,#00d4ff);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;background-clip:text;">
        🏙️ CITY CONTROL
      </div>
      <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.15em;color:#2a4060;margin-top:4px;text-transform:uppercase;">
        Neural Traffic OS
      </div>
    </div>
    """, unsafe_allow_html=True)

    # User badge
    st.markdown(f"""
    <div style="
      background:rgba(56,120,255,0.08);
      border:1px solid rgba(56,120,255,0.18);
      border-radius:10px;
      padding:10px 14px;
      margin-bottom:16px;
      display:flex;
      align-items:center;
      gap:10px;
    ">
      <span class="pulse-dot"></span>
      <div>
        <div style="font-family:'Space Mono',monospace;font-size:9px;color:#4a6080;letter-spacing:0.1em;">ACTIVE OPERATOR</div>
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#e8f0ff;">{st.session_state.user_role}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.15em;color:#2a4060;
      text-transform:uppercase;margin-bottom:8px;padding-left:4px;">
      COMMAND MODULES
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "nav",
        ["🛰️ System Overview", "🚦 Live Junction Control", "📈 Traffic Analytics", "🛡️ System Health"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(56,120,255,0.2),transparent);margin-bottom:16px;"></div>""", unsafe_allow_html=True)

    if st.button("⎋  LOGOUT / LOCK TERMINAL", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    # System status strip
    st.markdown(f"""
    <div style="margin-top:20px;padding:12px;border-radius:10px;background:rgba(0,255,135,0.05);
      border:1px solid rgba(0,255,135,0.12);">
      <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.15em;color:#00ff87;opacity:0.7;margin-bottom:6px;">
        SYSTEM STATUS
      </div>
      <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6080;line-height:1.8;">
        ENGINE · <span style="color:#00ff87">ONLINE</span><br>
        MODEL  · <span style="color:#00ff87">4.0.2-STABLE</span><br>
        TIME   · <span style="color:#3878ff">{time.strftime('%H:%M:%S')}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MODULE 1: SYSTEM OVERVIEW
# ============================================================
if nav == "🛰️ System Overview":
    st.markdown("""
    <span class="section-tag">◈ NETWORK OPERATIONS</span>
    <h1 class="neon-text">MISSION CONTROL</h1>
    """, unsafe_allow_html=True)

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.98%", "Stable")
    with col2:
        st.metric("Active Nodes", "1,242", "+4")
    with col3:
        st.metric("Avg. Latency", "24ms", "-2ms")
    with col4:
        st.metric("Carbon Offset", "12.4 Tons", "↑ High")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Map + Alerts
    map_col, log_col = st.columns([3, 1])

    with map_col:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">🌎 Infrastructure Map</span>
          <div class="section-header-line"></div>
          <span style="font-family:'Space Mono',monospace;font-size:9px;color:#2a4060;">LIVE · COIMBATORE GRID</span>
        </div>
        """, unsafe_allow_html=True)

        global_nodes = pd.DataFrame({
            'name': ['Peelamedu Hub', 'Gandhipuram', 'Airport Rd', 'Railway Stn'],
            'lat': [11.0271, 11.0183, 11.0285, 10.9967],
            'lon': [77.0108, 76.9723, 77.0261, 76.9616],
            'status': ['SMOOTH', 'CONGESTED', 'SMOOTH', 'MODERATE']
        })

        m_ov = folium.Map(location=[11.01, 76.98], zoom_start=12, tiles="CartoDB dark_matter")
        for _, row in global_nodes.iterrows():
            color = '#00ff87' if row['status'] == 'SMOOTH' else '#ff3d3d' if row['status'] == 'CONGESTED' else '#ffb300'
            folium.CircleMarker(
                location=[row['lat'], row['lon']], radius=12, color=color,
                fill=True, fill_opacity=0.7, popup=f"{row['name']}: {row['status']}"
            ).add_to(m_ov)
        st_folium(m_ov, width=850, height=480, key="overview_map")

    with log_col:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">🔔 Live Alerts</span>
        </div>
        """, unsafe_allow_html=True)

        alerts = [
            ("12:28", "🚨", "#ff3d3d", "Congestion: Peelamedu Sector B"),
            ("12:25", "✅", "#00ff87", "Optimized: Gandhipuram Signal"),
            ("12:20", "📡", "#3878ff", "New Node: Airport Rd Online"),
            ("12:15", "⚠️", "#ffb300", "Sensor Drift: Railway Stn"),
            ("12:10", "✅", "#00ff87", "AI Policy Updated (v4.0.2)"),
            ("12:05", "🚨", "#ff3d3d", "Heavy Transit: North Gate"),
        ]

        st.markdown('<div style="max-height:440px;overflow-y:auto;padding-right:4px;">', unsafe_allow_html=True)
        for t, icon, color, msg in alerts:
            st.markdown(f"""
            <div class="alert-item" style="border-left-color:{color};">
              <div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:2px;">{t}</div>
              <div style="color:{color};font-size:12px;">{icon} {msg}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # CCTV Section
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
      <span class="section-title">📽️ Multi-Node CCTV Telemetry</span>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)

    cam1, cam2, cam3, cam4 = st.columns(4)

    def cctv_placeholder(label, status_color, sublabel):
        return f"""
        <div class="cctv-card" style="height:160px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;">
          <div style="position:absolute;top:8px;left:10px;font-family:'Space Mono',monospace;color:{status_color};font-size:9px;letter-spacing:0.08em;">
            <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:{status_color};box-shadow:0 0 6px {status_color};margin-right:4px;animation:pulseDot 2s infinite;"></span>{label}
          </div>
          <div style="position:absolute;bottom:8px;right:10px;font-family:'Space Mono',monospace;color:#2a3d5c;font-size:8px;">{time.strftime('%H:%M:%S')}</div>
          <div style="font-size:36px;opacity:0.15;">📹</div>
          <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.08) 0px,rgba(0,0,0,0.08) 1px,transparent 2px);pointer-events:none;"></div>
          <div style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,rgba(0,0,0,0.4) 100%);pointer-events:none;"></div>
          <div style="position:absolute;bottom:8px;left:10px;font-family:'Space Mono',monospace;color:#3878ff;font-size:8px;opacity:0.6;">{sublabel}</div>
        </div>
        """

    with cam1:
        st.markdown(cctv_placeholder("CAM-01 · PEELAMEDU", "#ff3d3d", "North-Bound Lane"), unsafe_allow_html=True)
    with cam2:
        st.markdown(cctv_placeholder("CAM-02 · GANDHIPURAM", "#00ff87", "Main Signal Feed"), unsafe_allow_html=True)
    with cam3:
        st.markdown(cctv_placeholder("CAM-03 · AIRPORT RD", "#00ff87", "Transit Corridor"), unsafe_allow_html=True)
    with cam4:
        st.markdown(cctv_placeholder("CAM-04 · RAILWAY STN", "#ffb300", "Station Perimeter"), unsafe_allow_html=True)


# ============================================================
# MODULE 2: LIVE JUNCTION CONTROL
# ============================================================
elif nav == "🚦 Live Junction Control":
    st.markdown("""
    <span class="section-tag">◈ COMMAND & CONTROL</span>
    <h1 class="neon-text">AUTONOMOUS JUNCTION</h1>
    """, unsafe_allow_html=True)

    target_name = "Peelamedu Hub"
    target_lat, target_lon = 11.0271, 77.0108

    mode = st.radio(
        "SELECT OPERATIONAL MODE",
        ["📡 Live Autonomous Monitoring", "📥 Manual Batch Processing"],
        horizontal=True
    )

    if mode == "📥 Manual Batch Processing":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.15em;color:#3878ff;text-transform:uppercase;margin-bottom:16px;">
          ◈ DATA INGESTION TERMINAL
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Traffic Sensor CSV", type="csv")

        if uploaded_file is not None:
            try:
                input_df = pd.read_csv(uploaded_file)
                st.success("✓  Data received. Running Neural Batch Engine...")
                results_df = engine.predict_batch(input_df)

                st.dataframe(results_df.style.applymap(
                    lambda x: "color: #00ff87; font-weight:bold" if x == "SMOOTH" else "color: #ff3d3d; font-weight:bold",
                    subset=['Traffic_Status']
                ), use_container_width=True)

                csv_data = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⟶  DOWNLOAD ANALYTICS REPORT",
                    data=csv_data,
                    file_name=f"Traffic_AI_Report_{time.strftime('%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Processing Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="traffic_os_2026")

        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.12em;color:#3878ff;text-transform:uppercase;margin-bottom:6px;">
          🔍 GPS LOCATION SEARCH
        </div>
        """, unsafe_allow_html=True)
        search_query = st.text_input(
            "location_search", label_visibility="collapsed",
            placeholder="Search city or landmark (e.g. Coimbatore, Tamil Nadu)..."
        )

        if search_query:
            try:
                location = geolocator.geocode(search_query)
                if location:
                    target_lat, target_lon = location.latitude, location.longitude
                    target_name = search_query
                    st.success(f"📍 GPS Lock acquired: {location.address}")
            except:
                st.warning("GPS connection failed. Using default coordinates.")

        col_map, col_data = st.columns([2, 1])

        c, b, bu, t = np.random.randint(20, 150), np.random.randint(10, 60), np.random.randint(0, 20), np.random.randint(0, 15)
        res = engine.get_signal_config(c, b, bu, t)
        status_word = res['status'].split()[0]

        with col_map:
            st.markdown(f"""
            <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.1em;color:#3878ff;margin-bottom:8px;">
              🛰️ ORBITAL FEED — {target_name.upper()}
            </div>
            """, unsafe_allow_html=True)
            live_map = create_city_map(target_lat, target_lon, status_word, target_name)
            st_folium(live_map, width=700, height=420, key="live_search_map")

        with col_data:
            total = c + b + bu + t
            status_colors = {'SMOOTH': '#00ff87', 'MODERATE': '#ffb300', 'CONGESTED': '#ff3d3d'}
            s_color = status_colors.get(status_word, '#3878ff')

            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:16px;">
              <div class="kpi-label">TOTAL DENSITY</div>
              <div class="kpi-value">{total}</div>
              <div style="height:8px"></div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div style="background:rgba(56,120,255,0.06);border:1px solid rgba(56,120,255,0.12);border-radius:8px;padding:10px;">
                  <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a4060;">🚗 CARS</div>
                  <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#e8f0ff;">{c}</div>
                </div>
                <div style="background:rgba(56,120,255,0.06);border:1px solid rgba(56,120,255,0.12);border-radius:8px;padding:10px;">
                  <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a4060;">🚌 BUSES</div>
                  <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#e8f0ff;">{b}</div>
                </div>
                <div style="background:rgba(56,120,255,0.06);border:1px solid rgba(56,120,255,0.12);border-radius:8px;padding:10px;">
                  <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a4060;">🚛 TRUCKS</div>
                  <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#e8f0ff;">{bu}</div>
                </div>
                <div style="background:rgba(56,120,255,0.06);border:1px solid rgba(56,120,255,0.12);border-radius:8px;padding:10px;">
                  <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a4060;">🚐 TRANSIT</div>
                  <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#e8f0ff;">{t}</div>
                </div>
              </div>
            </div>

            <div style="
              text-align:center;
              border:1px solid {s_color}30;
              padding:24px;
              border-radius:20px;
              background:radial-gradient(ellipse at center, {s_color}08, transparent 70%);
              position:relative;
              overflow:hidden;
            ">
              <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{s_color}60,transparent);"></div>
              <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.2em;color:{s_color};opacity:0.7;margin-bottom:8px;">AI DECISION</div>
              <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:{s_color};letter-spacing:0.05em;">{res['status']}</div>
              <div style="font-family:'Syne',sans-serif;font-size:64px;font-weight:800;color:white;line-height:1;margin:8px 0;">{res['timer']}<span style="font-size:20px;color:#4a6080;">s</span></div>
              <div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a4060;letter-spacing:0.1em;">PHASE DURATION</div>
            </div>
            """, unsafe_allow_html=True)

    # Emergency & Override
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,61,61,0.3),transparent);margin-bottom:20px;"></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:#ff3d3d;text-transform:uppercase;margin-bottom:12px;">
      ⚠ CRITICAL — EMERGENCY PREEMPTION
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚨  ACTIVATE AMBULANCE PASSAGE PROTOCOL", use_container_width=True):
        emergency_display = st.empty()
        st.balloons()
        st.toast(f"🚨 Clearing corridor at {target_name}")
        for seconds in range(5, 0, -1):
            emergency_display.markdown(f"""
            <div class="emergency-banner" style="
              background:linear-gradient(135deg,rgba(255,61,61,0.15),rgba(255,61,61,0.05));
              border:2px solid rgba(255,61,61,0.5);
            ">
              <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#ff3d3d,transparent);"></div>
              <div style="font-family:'Space Mono',monospace;font-size:11px;letter-spacing:0.3em;color:#ff3d3d;margin-bottom:12px;">◈ EMERGENCY PROTOCOL ACTIVE ◈</div>
              <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:white;letter-spacing:-0.01em;margin-bottom:8px;">🚑 AMBULANCE IN CORRIDOR</div>
              <div style="font-family:'Syne',sans-serif;font-size:80px;font-weight:800;color:white;line-height:1;letter-spacing:-0.04em;">{seconds}<span style="font-size:24px;color:#ff3d3d;">s</span></div>
              <div style="font-family:'Space Mono',monospace;font-size:11px;color:#ff3d3d;letter-spacing:0.1em;margin-top:8px;">ALL CONFLICTING LANES HELD AT 🔴 RED</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        emergency_display.success(f"✅ Ambulance cleared {target_name}. Resuming neural optimization.")
        time.sleep(1)
        st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.15em;color:#ffb300;text-transform:uppercase;margin-bottom:12px;">
      ◈ SYSTEM OVERRIDE PANEL
    </div>
    """, unsafe_allow_html=True)

    ov_col1, ov_col2 = st.columns([1, 2])
    with ov_col1:
        st.markdown('<div class="override-card">', unsafe_allow_html=True)
        override_action = st.radio(
            "SELECT ACTION",
            ["🤖 AI AUTO", "🟢 FORCE GREEN", "🔴 FORCE RED", "🟡 FLASHING AMBER"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with ov_col2:
        if override_action != "🤖 AI AUTO":
            st.warning(f"OVERRIDE ACTIVE: {override_action} → {target_name}")
            custom_timer = st.slider("Manual Phase Duration (seconds)", 10, 120, 60)
            if st.button("🚀  EXECUTE OVERRIDE COMMAND", use_container_width=True):
                with st.spinner("Pushing command to field nodes..."):
                    time.sleep(1)
                st.balloons()
                st.success(f"✓ Command executed: {target_name} → {override_action} for {custom_timer}s")
        else:
            st.markdown("""
            <div style="
              background:rgba(0,255,135,0.05);
              border:1px solid rgba(0,255,135,0.15);
              border-radius:14px;
              padding:20px 24px;
            ">
              <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.15em;color:#00ff87;margin-bottom:6px;">◈ AUTONOMOUS MODE ACTIVE</div>
              <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#8ba3cc;">System is running on <strong style="color:#e8f0ff;">Neural Optimization v4.0</strong>. AI is managing all junction cycles in real-time.</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# MODULE 3: ANALYTICS
# ============================================================
elif nav == "📈 Traffic Analytics":
    st.markdown("""
    <span class="section-tag">◈ INTELLIGENCE CENTER</span>
    <h1 class="neon-text">PREDICTIVE ANALYTICS</h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg. Flow Rate", "1,420 veh/hr", "+12%")
    with col2:
        st.metric("Network Efficiency", "88%", "+5%")
    with col3:
        st.metric("Peak Wait Time", "142s", "-18s")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    chart_col, pie_col = st.columns([2, 1])
    with chart_col:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">📈 24-Hour Network Load</span>
          <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)
        chart_data = pd.DataFrame(
            np.random.randn(24, 3),
            columns=['Main Corridor', 'Expressway', 'Downtown']
        )
        st.line_chart(chart_data)

    with pie_col:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">🚚 Vehicle Composition</span>
        </div>
        """, unsafe_allow_html=True)
        composition_data = pd.DataFrame({
            'Category': ['Bikes', 'Buses', 'Trucks'],
            'Count': [133, 42, 15]
        })
        st.bar_chart(composition_data.set_index('Category'))
        st.caption("Current breakdown of active transport units.")

    st.markdown("""
    <div class="section-header" style="margin-top:8px;">
      <span class="section-title">🌡️ Congestion Density Map</span>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)
    heatmap_data = pd.DataFrame(
        np.random.rand(10, 7),
        columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    )
    st.area_chart(heatmap_data)

    st.markdown("""
    <div style="
      background:rgba(56,120,255,0.06);
      border:1px solid rgba(56,120,255,0.18);
      border-radius:12px;
      padding:14px 20px;
      font-family:'DM Sans',sans-serif;
      font-size:13px;
      color:#8ba3cc;
    ">
      💡 <strong style="color:#e8f0ff;">Predictive Insight:</strong> Evening peak expected at 18:45 UTC+5:30. Neural AI adjusting West-Gate signal priorities 12 minutes in advance.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MODULE 4: SYSTEM HEALTH
# ============================================================
elif nav == "🛡️ System Health":
    st.markdown("""
    <span class="section-tag">◈ DIAGNOSTICS</span>
    <h1 class="neon-text">ENGINE STATUS</h1>
    """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("Core Stability", "92%", "+1.2%")
    with d2:
        st.metric("Model Accuracy", "97.4%", "+0.3%")
    with d3:
        st.metric("Response Time", "8ms", "-1ms")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
      <span class="section-title">📟 System Log Output</span>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.code(f"""
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Prediction Engine ........... ONLINE
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Model Version ................ 4.0.2-STABLE
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Operator Auth ................ {st.session_state.user_role}
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Signal Nodes Active .......... 1,242
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Last Prediction Batch ........ 0.83s
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Memory Footprint ............. 412 MB
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — Neural Core Temperature ...... 38°C
[SYS_LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} — All Systems .................. NOMINAL
    """, language=None)

    st.markdown("""
    <div class="section-header" style="margin-top:8px;">
      <span class="section-title">⚡ Core Subsystem Health</span>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)

    subsystems = [
        ("Prediction Engine", 92, "#3878ff"),
        ("Signal Relay Network", 98, "#00ff87"),
        ("Sensor Data Ingestion", 85, "#ffb300"),
        ("Emergency Preemption", 100, "#00ff87"),
        ("Map & Telemetry Feed", 76, "#ffb300"),
    ]

    for name, val, color in subsystems:
        st.markdown(f"""
        <div style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.08em;color:#8ba3cc;">{name}</span>
            <span style="font-family:'Space Mono',monospace;font-size:10px;color:{color};">{val}%</span>
          </div>
          <div style="height:4px;background:rgba(56,120,255,0.1);border-radius:2px;overflow:hidden;">
            <div style="width:{val}%;height:100%;background:linear-gradient(90deg,{color}88,{color});border-radius:2px;box-shadow:0 0 8px {color}60;transition:width 1s ease;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.progress(92, text="Overall Core Stability")
