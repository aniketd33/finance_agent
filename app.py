"""
╔══════════════════════════════════════════════╗
║   💰 FinBot — AI Personal Finance Assistant  ║
║   Built with Streamlit + Claude AI           ║
╚══════════════════════════════════════════════╝
Run: streamlit run app.py
"""

import streamlit as st
from database.db import create_tables

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "💰 Finance Agent",
    page_icon  = "💰",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# Create DB tables on first run
create_tables()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e0e0e0;
        height: 100%;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #333;
    }
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    .stat-box {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">💰 Finance Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-Powered Personal Finance Assistant for Users</div>', unsafe_allow_html=True)

st.divider()

# ── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown("### 🚀 What can Finance Agent do?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">AI Chat</div>
        <div class="feature-desc">Ask anything about personal finance. Finance Agent remembers your conversation.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Budget Planner</div>
        <div class="feature-desc">Enter income & expenses. Get a personalized budget plan instantly.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏷️</div>
        <div class="feature-title">Expense Tracker</div>
        <div class="feature-desc">Add transactions. AI auto-categorizes and shows spending insights.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Smart Advice</div>
        <div class="feature-desc">Get savings plans & investment suggestions (SIP, PPF, ELSS, FD).</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Quick Start ───────────────────────────────────────────────────────────────
st.markdown("### 🎯 Quick Start")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.info("""
    **👈 Use the sidebar to navigate:**
    - 💬 **Chat** — Free-form finance assistant
    - 📊 **Budget Planner** — Monthly budget analysis
    - 🏷️ **Expense Tracker** — Track & categorize expenses
    - 💡 **Financial Advice** — Savings & investment tips
    """)

with col_b:
    st.success("""
    **🇮🇳 Built for Indian Users:**
    - All amounts in ₹ INR
    - SIP, PPF, ELSS, NPS, FD advice
    - Tax saving options (80C, 80D)
    - UPI transaction support
    """)

st.divider()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#999; font-size:0.85rem; padding:1rem'>
    💰 Finance Agent | Aniket Dombale | Major Project
</div>
""", unsafe_allow_html=True)
