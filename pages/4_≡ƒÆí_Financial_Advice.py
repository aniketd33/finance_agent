"""
💡 Financial Advice Page — Savings Plans & Investment Suggestions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from agent.claude_agent import run_agent

st.set_page_config(page_title="💡 Advice | FinBot", page_icon="💡", layout="wide")

st.markdown("## 💡 Financial Advice")
st.caption("Get personalized savings plans and investment suggestions based on your finances.")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💰 Savings Plan", "📈 Investment Advice", "🏥 Full Checkup"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: Savings Plan
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💰 Personalized Savings Plan")
    st.caption("Tell us your goal and we'll create a month-by-month savings plan.")

    col1, col2 = st.columns([1, 1])

    with col1:
        income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000, key="sav_inc")
        goal   = st.text_input("Your Financial Goal", value="Build emergency fund of ₹1 lakh")
        target = st.number_input("Target Amount (₹)", min_value=0, value=100000, step=5000)

    with col2:
        st.markdown("#### Monthly Expenses (₹)")
        s_rent      = st.number_input("Rent/EMI",   min_value=0, value=12000, step=500, key="s_rent")
        s_food      = st.number_input("Food",       min_value=0, value=8000,  step=500, key="s_food")
        s_transport = st.number_input("Transport",  min_value=0, value=3000,  step=500, key="s_tran")
        s_others    = st.number_input("Others",     min_value=0, value=5000,  step=500, key="s_oth")
        timeline    = st.slider("Timeline (months)", 1, 36, 12)

    if st.button("📅 Generate Savings Plan", type="primary", use_container_width=True):
        expenses = {
            "rent": s_rent, "food": s_food,
            "transport": s_transport, "others": s_others
        }
        surplus = income - sum(expenses.values())
        monthly_needed = target / timeline if timeline > 0 else 0

        # Quick metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("💵 Monthly Surplus",   f"₹{surplus:,}")
        m2.metric("🎯 Need to Save/Month", f"₹{monthly_needed:,.0f}")
        m3.metric("✅ Feasible?",
                  "Yes! 🟢" if surplus >= monthly_needed else "Tight ⚠️",
                  delta=f"₹{surplus - monthly_needed:,.0f} buffer")

        # Savings milestone chart
        months    = list(range(0, timeline + 1))
        saved     = [min(monthly_needed * m, target) for m in months]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=saved,
            fill="tozeroy", mode="lines+markers",
            name="Projected Savings",
            line=dict(color="#667eea", width=3),
            marker=dict(size=6)
        ))
        fig.add_hline(y=target, line_dash="dash", line_color="green",
                      annotation_text=f"Goal: ₹{target:,}")
        fig.update_layout(
            title  = f"Savings Milestone — Reach ₹{target:,} in {timeline} months",
            xaxis_title = "Month",
            yaxis_title = "Amount Saved (₹)",
            height = 350
        )
        st.plotly_chart(fig, use_container_width=True)

        # AI savings plan
        with st.spinner("Generating your personalized savings plan..."):
            try:
                result = run_agent(
                    user_message = f"Create a detailed month-by-month savings plan to reach my goal.",
                    financial_data = {
                        "income":          income,
                        "expenses":        expenses,
                        "goal":            goal,
                        "target_amount":   target,
                        "timeline_months": timeline,
                        "monthly_surplus": surplus
                    }
                )
                st.markdown(result["reply"])
            except Exception as e:
                st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: Investment Advice
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📈 Investment Suggestions")
    st.caption("Based on your surplus and risk appetite, get tailored investment recommendations.")

    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_surplus = st.number_input(
            "Monthly Investable Surplus (₹)",
            min_value = 500, value = 10000, step = 500
        )
    with col2:
        risk = st.select_slider(
            "Risk Appetite",
            options = ["low", "medium", "high"],
            value   = "medium"
        )
    with col3:
        inv_goal = st.selectbox(
            "Investment Goal",
            ["Wealth Creation", "Retirement", "Child Education",
             "Buy a House", "Emergency Fund", "Tax Saving"]
        )

    # Risk info cards
    risk_info = {
        "low":    ("🟢 Low Risk", "FD, PPF, NSC, Sukanya Samriddhi — Safe, steady returns 6-8% p.a."),
        "medium": ("🟡 Medium Risk", "SIP, ELSS, NPS, Balanced Funds — Good returns 10-14% p.a."),
        "high":   ("🔴 High Risk", "Direct Stocks, Small Cap Funds, Index Funds — High returns but volatile")
    }
    st.info(f"**{risk_info[risk][0]}** — {risk_info[risk][1]}")

    if st.button("📊 Get Investment Advice", type="primary", use_container_width=True):

        # Investment allocation chart
        if risk == "low":
            alloc = {"FD/RD": 40, "PPF": 35, "NSC": 15, "Emergency Fund": 10}
        elif risk == "medium":
            alloc = {"SIP Mutual Funds": 40, "ELSS": 25, "NPS": 20, "FD": 15}
        else:
            alloc = {"Direct Stocks": 35, "Small Cap Funds": 30, "Index Funds": 25, "REITs": 10}

        fig = px.pie(
            values = list(alloc.values()),
            names  = list(alloc.keys()),
            title  = f"Recommended Allocation — ₹{monthly_surplus:,}/month ({risk.title()} Risk)",
            color_discrete_sequence = px.colors.qualitative.Pastel,
            hole   = 0.4
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

        with st.spinner("Getting investment recommendations..."):
            try:
                result = run_agent(
                    user_message = f"Give detailed investment advice for my goal: {inv_goal}",
                    financial_data = {
                        "monthly_surplus": monthly_surplus,
                        "risk_appetite":   risk,
                        "investment_goal": inv_goal
                    }
                )
                st.markdown(result["reply"])
            except Exception as e:
                st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: Full Checkup
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🏥 Complete Financial Health Checkup")
    st.caption("Get a full analysis — budget health, savings plan, and investment advice all in one.")

    col1, col2 = st.columns(2)

    with col1:
        fc_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000, key="fc_inc")
        fc_goal   = st.text_input("Your Main Financial Goal", value="Financial freedom in 10 years", key="fc_goal")

    with col2:
        st.markdown("**Monthly Expenses (₹)**")
        fc_rent      = st.number_input("Rent/EMI",      min_value=0, value=12000, key="fc_rent")
        fc_food      = st.number_input("Food",          min_value=0, value=8000,  key="fc_food")
        fc_transport = st.number_input("Transport",     min_value=0, value=3000,  key="fc_tran")
        fc_emi       = st.number_input("Other EMI",     min_value=0, value=0,     key="fc_emi")
        fc_others    = st.number_input("Others",        min_value=0, value=7000,  key="fc_oth")

    if st.button("🏥 Run Full Financial Checkup", type="primary", use_container_width=True):
        fc_expenses = {
            "rent":      fc_rent,
            "food":      fc_food,
            "transport": fc_transport,
            "emi":       fc_emi,
            "others":    fc_others
        }
        fc_expenses = {k: v for k, v in fc_expenses.items() if v > 0}

        with st.spinner("FinBot is doing a complete analysis of your finances... 🔍"):
            try:
                result = run_agent(
                    user_message = (
                        "Do a COMPLETE financial health checkup. Include: "
                        "1) Financial health score out of 10 with explanation, "
                        "2) Budget analysis with 50-30-20 comparison, "
                        "3) 3-month savings plan with milestones, "
                        "4) Investment recommendations, "
                        "5) Top 5 priority action items. "
                        "Be specific with rupee amounts."
                    ),
                    financial_data = {
                        "income":   fc_income,
                        "expenses": fc_expenses,
                        "goal":     fc_goal
                    }
                )
                st.success("✅ Checkup Complete!")
                st.markdown(result["reply"])

                if result["tool_calls_made"]:
                    with st.expander("🔧 View AI Calculations"):
                        for tool in result["tool_calls_made"]:
                            st.json(tool)
            except Exception as e:
                st.error(f"Error: {e}")
