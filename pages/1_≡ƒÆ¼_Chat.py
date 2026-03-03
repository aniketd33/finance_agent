"""
💬 Chat Page — Free-form Finance Assistant with Memory
"""

import streamlit as st
from agent.claude_agent import run_agent
from database.db import get_session, ChatHistory

st.set_page_config(page_title="💬 Chat | FinBot", page_icon="💬", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .chat-header { font-size:1.8rem; font-weight:700; color:#667eea; }
    .user-msg {
        background: #667eea;
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 2px 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-msg {
        background: #f0f2f6;
        color: #333;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 15px 2px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .tool-badge {
        background: #e8f4fd;
        color: #1a73e8;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-header">💬 Chat with FinBot</div>', unsafe_allow_html=True)
st.caption("Ask anything about personal finance — budgeting, savings, investments, EMI calculations and more!")

# ── Initialize session state ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar: Quick Questions ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💡 Quick Questions")
    quick_questions = [
        "How can I save ₹1 lakh in 6 months?",
        "I earn ₹40,000/month, suggest a budget",
        "Should I invest in SIP or FD?",
        "How to build an emergency fund?",
        "Explain 50-30-20 budgeting rule",
        "Best tax saving options under 80C",
        "How to get out of debt quickly?",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True, key=f"quick_{q[:20]}"):
            st.session_state["prefill_message"] = q

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        db = get_session()
        db.query(ChatHistory).delete()
        db.commit()
        db.close()
        st.success("Chat cleared!")
        st.rerun()

# ── Display existing messages ─────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center; color:#999; padding:3rem'>
            <div style='font-size:3rem'>👋</div>
            <div style='font-size:1.1rem; margin-top:0.5rem'>Hi! I'm FinBot, your personal finance assistant.</div>
            <div style='font-size:0.9rem; margin-top:0.3rem'>Ask me anything about budgeting, savings, or investments!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant", avatar="💰"):
                    st.write(msg["content"])
                    if msg.get("tools_used"):
                        st.markdown(" ".join([
                            f'<span class="tool-badge">🔧 {t}</span>'
                            for t in msg["tools_used"]
                        ]), unsafe_allow_html=True)

# ── Chat Input ────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill_message", "")
user_input = st.chat_input(
    placeholder="Ask me about budgeting, savings, investments...",
)

# Use prefill if available
if prefill and not user_input:
    user_input = prefill

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Save to DB
    db = get_session()
    db.add(ChatHistory(role="user", message=user_input))
    db.commit()

    # Get AI response
    with st.spinner("FinBot is thinking... 🤔"):
        history_for_agent = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1][-10:]
        ]
        try:
            result = run_agent(
                user_message = user_input,
                chat_history = history_for_agent
            )
            reply      = result["reply"]
            tools_used = [t["tool"] for t in result["tool_calls_made"]]
        except ValueError as e:
            reply      = f"⚠️ Configuration Error: {str(e)}"
            tools_used = []
        except Exception as e:
            reply      = f"❌ Error: {str(e)}\n\nPlease check your API key in the .env file."
            tools_used = []

    # Save assistant reply to DB
    db.add(ChatHistory(role="assistant", message=reply))
    db.commit()
    db.close()

    # Add to session
    st.session_state.messages.append({
        "role":       "assistant",
        "content":    reply,
        "tools_used": tools_used
    })

    st.rerun()
