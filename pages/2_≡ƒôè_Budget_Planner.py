"""
📊 Budget Planner Page
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from agent.claude_agent import run_agent

st.set_page_config(page_title="📊 Budget Planner | FinBot", page_icon="📊", layout="wide")

st.markdown("## 📊 Budget Planner")
st.caption("Enter your monthly income and expenses to get a personalized AI budget plan.")

# ── Input Form ────────────────────────────────────────────────────────────────
with st.form("budget_form"):
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 💰 Income")
        income = st.number_input(
            "Monthly Income (₹)",
            min_value    = 0,
            value        = 50000,
            step         = 1000,
            format       = "%d",
            help         = "Your total monthly take-home salary in INR"
        )
        savings_goal = st.slider(
            "Savings Goal (%)",
            min_value = 5,
            max_value = 60,
            value     = 20,
            step      = 5,
            help      = "What % of income do you want to save?"
        )

    with col2:
        st.markdown("### 💸 Monthly Expenses (₹)")
        rent          = st.number_input("🏠 Rent / EMI",         min_value=0, value=12000, step=500)
        food          = st.number_input("🍔 Food & Groceries",   min_value=0, value=8000,  step=500)
        transport     = st.number_input("🚗 Transport / Fuel",   min_value=0, value=3000,  step=500)
        entertainment = st.number_input("🎬 Entertainment",      min_value=0, value=2000,  step=500)
        utilities     = st.number_input("💡 Utilities & Bills",  min_value=0, value=2000,  step=500)
        healthcare    = st.number_input("🏥 Healthcare",         min_value=0, value=1000,  step=500)
        shopping      = st.number_input("🛍️ Shopping",           min_value=0, value=3000,  step=500)
        others        = st.number_input("📦 Others",             min_value=0, value=2000,  step=500)

    submitted = st.form_submit_button("🔍 Analyze My Budget", use_container_width=True, type="primary")

# ── Process ───────────────────────────────────────────────────────────────────
if submitted:
    expenses = {
        "Rent/EMI":      rent,
        "Food":          food,
        "Transport":     transport,
        "Entertainment": entertainment,
        "Utilities":     utilities,
        "Healthcare":    healthcare,
        "Shopping":      shopping,
        "Others":        others
    }
    # Remove zero expenses
    expenses = {k: v for k, v in expenses.items() if v > 0}

    total_expenses = sum(expenses.values())
    surplus        = income - total_expenses
    savings_pct    = round((surplus / income * 100), 1) if income > 0 else 0

    # ── Quick Stats ───────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 📈 Quick Summary")
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("💰 Monthly Income",   f"₹{income:,}")
    m2.metric("💸 Total Expenses",   f"₹{total_expenses:,}",
              delta=f"-₹{total_expenses:,}", delta_color="inverse")
    m3.metric("💵 Surplus",          f"₹{surplus:,}",
              delta=f"{savings_pct}% savings",
              delta_color="normal" if surplus >= 0 else "inverse")
    m4.metric("🎯 Savings Goal",     f"{savings_goal}%",
              delta="On Track ✅" if savings_pct >= savings_goal else "Below Target ⚠️",
              delta_color="normal" if savings_pct >= savings_goal else "inverse")

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown("### 📊 Expense Breakdown")
    c1, c2 = st.columns(2)

    with c1:
        fig_pie = px.pie(
            values = list(expenses.values()),
            names  = list(expenses.keys()),
            title  = "Expense Distribution",
            color_discrete_sequence = px.colors.qualitative.Set3,
            hole   = 0.4
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        # Budget vs 50-30-20 rule
        needs_50  = income * 0.50
        wants_30  = income * 0.30
        savings_20 = income * 0.20
        actual_needs  = rent + food + transport + utilities + healthcare
        actual_wants  = entertainment + shopping + others

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Your Budget",   x=["Needs", "Wants", "Savings"], y=[actual_needs, actual_wants, surplus],        marker_color=["#667eea","#f093fb","#4facfe"]))
        fig_bar.add_trace(go.Bar(name="50-30-20 Rule", x=["Needs", "Wants", "Savings"], y=[needs_50, wants_30, savings_20], marker_color=["#a8edea","#fed6e3","#d4fc79"]))
        fig_bar.update_layout(
            barmode = "group",
            title   = "Your Budget vs 50-30-20 Rule (₹)",
            height  = 400,
            yaxis_tickprefix = "₹"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── AI Analysis ───────────────────────────────────────────────────────────
    st.markdown("### 🤖 AI Budget Analysis")
    with st.spinner("FinBot is analyzing your budget... 💭"):
        try:
            result = run_agent(
                user_message = "Analyze my budget in detail. Give me: 1) Budget health score out of 10, 2) Top 3 overspending areas, 3) Specific tips to improve, 4) Ideal allocation using 50-30-20 rule",
                financial_data = {
                    "income":       income,
                    "expenses":     expenses,
                    "savings_goal": savings_goal,
                    "surplus":      surplus,
                    "savings_pct":  savings_pct
                }
            )
            st.markdown(result["reply"])

            if result["tool_calls_made"]:
                with st.expander("🔧 Tools Used by AI"):
                    for tool in result["tool_calls_made"]:
                        st.json(tool)
        except Exception as e:
            st.error(f"Error: {str(e)}")
