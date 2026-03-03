"""
🏷️ Expense Tracker Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from agent.claude_agent import run_agent
from database.db import get_session, Transaction

st.set_page_config(page_title="🏷️ Expenses | FinBot", page_icon="🏷️", layout="wide")

st.markdown("## 🏷️ Expense Tracker")
st.caption("Add your transactions and let AI automatically categorize them with spending insights.")

# ── Sidebar: Add Transaction ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ➕ Add Transaction")
    with st.form("add_txn_form"):
        desc   = st.text_input("Description", placeholder="e.g. Zomato biryani order")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, format="%.2f")
        txn_date = st.date_input("Date", value=date.today())
        add_btn = st.form_submit_button("➕ Add", use_container_width=True, type="primary")

    if add_btn and desc and amount > 0:
        db  = get_session()
        txn = Transaction(
            description = desc,
            amount      = amount,
            category    = "uncategorized",
            date        = str(txn_date)
        )
        db.add(txn)
        db.commit()
        db.close()
        st.success(f"✅ Added: {desc}")
        st.rerun()

    st.divider()
    st.markdown("### 📋 Bulk Add (CSV)")
    st.caption("Upload a CSV with columns: description, amount, date")
    csv_file = st.file_uploader("Upload CSV", type=["csv"])
    if csv_file:
        try:
            df  = pd.read_csv(csv_file)
            db  = get_session()
            count = 0
            for _, row in df.iterrows():
                db.add(Transaction(
                    description = str(row.get("description", "")),
                    amount      = float(row.get("amount", 0)),
                    category    = "uncategorized",
                    date        = str(row.get("date", date.today()))
                ))
                count += 1
            db.commit()
            db.close()
            st.success(f"✅ Imported {count} transactions!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ── Load Transactions ─────────────────────────────────────────────────────────
db   = get_session()
txns = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
db.close()

if not txns:
    st.info("👈 No transactions yet! Add some from the sidebar.")
    st.markdown("""
    **Sample transactions to try:**
    - Zomato biryani order — ₹450
    - Uber cab to office — ₹230
    - Netflix subscription — ₹649
    - Apollo pharmacy — ₹850
    - Amazon shopping — ₹2300
    """)
else:
    # ── Categorize Button ─────────────────────────────────────────────────────
    uncategorized = [t for t in txns if t.category == "uncategorized"]
    if uncategorized:
        st.warning(f"⚠️ {len(uncategorized)} transactions are uncategorized.")
        if st.button("🤖 Auto-Categorize with AI", type="primary"):
            with st.spinner("AI is categorizing your transactions..."):
                txn_list = [
                    {"description": t.description, "amount": t.amount, "date": t.date}
                    for t in uncategorized
                ]
                try:
                    result = run_agent(
                        user_message   = "Categorize these transactions.",
                        financial_data = {"transactions": txn_list}
                    )
                    # Update categories in DB
                    for tool_call in result["tool_calls_made"]:
                        if tool_call["tool"] == "categorize_expenses":
                            cats = tool_call["result"].get("categorized_transactions", [])
                            db = get_session()
                            for i, t in enumerate(uncategorized):
                                if i < len(cats):
                                    t.category = cats[i].get("category", "others")
                                    db.merge(t)
                            db.commit()
                            db.close()
                    st.success("✅ All transactions categorized!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Transactions Table ────────────────────────────────────────────────────
    st.markdown("### 📋 All Transactions")
    df = pd.DataFrame([{
        "Date":        t.date,
        "Description": t.description,
        "Amount (₹)":  t.amount,
        "Category":    t.category.title() if t.category else "—"
    } for t in txns])

    # Category color map
    category_colors = {
        "Food":          "🍔",
        "Transport":     "🚗",
        "Rent":          "🏠",
        "Entertainment": "🎬",
        "Healthcare":    "🏥",
        "Shopping":      "🛍️",
        "Utilities":     "💡",
        "Others":        "📦",
        "Uncategorized": "❓"
    }
    df["Category"] = df["Category"].apply(
        lambda x: f"{category_colors.get(x, '📌')} {x}"
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    categorized_txns = [t for t in txns if t.category != "uncategorized"]
    if categorized_txns:
        st.markdown("### 📊 Spending Analytics")
        c1, c2 = st.columns(2)

        # Spending by category
        cat_df = pd.DataFrame([{"Category": t.category.title(), "Amount": t.amount} for t in categorized_txns])
        cat_sum = cat_df.groupby("Category")["Amount"].sum().reset_index()

        with c1:
            fig = px.bar(
                cat_sum.sort_values("Amount", ascending=True),
                x     = "Amount",
                y     = "Category",
                title = "Spending by Category (₹)",
                color = "Amount",
                color_continuous_scale = "Viridis",
                orientation = "h"
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.pie(
                cat_sum,
                values = "Amount",
                names  = "Category",
                title  = "Expense Distribution",
                color_discrete_sequence = px.colors.qualitative.Set3,
                hole   = 0.4
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

        # ── Metrics ───────────────────────────────────────────────────────────
        total = sum(t.amount for t in categorized_txns)
        top_cat = cat_sum.loc[cat_sum["Amount"].idxmax()]

        m1, m2, m3 = st.columns(3)
        m1.metric("💸 Total Spent",   f"₹{total:,.0f}")
        m2.metric("🔢 Transactions",  len(categorized_txns))
        m3.metric(f"📌 Top Category", f"{top_cat['Category']} (₹{top_cat['Amount']:,.0f})")

        # ── AI Insights ───────────────────────────────────────────────────────
        st.markdown("### 🤖 AI Spending Insights")
        if st.button("💡 Get AI Insights on My Spending", type="primary"):
            with st.spinner("Analyzing your spending patterns..."):
                try:
                    result = run_agent(
                        user_message = "Analyze my spending and give 3 key insights and money-saving tips.",
                        financial_data = {
                            "transactions": [
                                {"description": t.description, "amount": t.amount,
                                 "category": t.category, "date": t.date}
                                for t in categorized_txns
                            ],
                            "total_spent": total,
                            "by_category": cat_sum.to_dict("records")
                        }
                    )
                    st.markdown(result["reply"])
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Clear Transactions ────────────────────────────────────────────────────
    st.divider()
    if st.button("🗑️ Clear All Transactions", type="secondary"):
        db = get_session()
        db.query(Transaction).delete()
        db.commit()
        db.close()
        st.success("All transactions cleared!")
        st.rerun()
