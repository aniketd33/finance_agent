import json

finance_tools = [
    {
        "name": "calculate_budget",
        "description": "Calculate monthly budget, savings percentage, and overspending warnings based on income and expenses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "income":               {"type": "number", "description": "Monthly income in INR"},
                "expenses":             {"type": "object", "description": "Category-wise expenses dict"},
                "savings_goal_percent": {"type": "number", "description": "Target savings % (default 20)"}
            },
            "required": ["income", "expenses"]
        }
    },
    {
        "name": "categorize_expenses",
        "description": "Categorize raw bank transactions into Food, Rent, Transport, Entertainment, Healthcare, Shopping, Utilities, Others.",
        "input_schema": {
            "type": "object",
            "properties": {
                "transactions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "amount":      {"type": "number"},
                            "date":        {"type": "string"}
                        }
                    }
                }
            },
            "required": ["transactions"]
        }
    },
    {
        "name": "analyze_spending_pattern",
        "description": "Analyze spending patterns across multiple months, detect trends and overspending.",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "month":    {"type": "string"},
                            "income":   {"type": "number"},
                            "expenses": {"type": "object"}
                        }
                    }
                }
            },
            "required": ["monthly_data"]
        }
    },
    {
        "name": "generate_savings_plan",
        "description": "Generate a personalized savings plan with monthly milestones to reach a financial goal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "income":          {"type": "number"},
                "expenses":        {"type": "object"},
                "goal":            {"type": "string"},
                "target_amount":   {"type": "number"},
                "timeline_months": {"type": "integer"}
            },
            "required": ["income", "expenses", "goal"]
        }
    },
    {
        "name": "investment_suggestions",
        "description": "Suggest Indian investment options (SIP, PPF, FD, ELSS, NPS) based on surplus and risk appetite.",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_surplus": {"type": "number"},
                "risk_appetite":   {"type": "string", "enum": ["low", "medium", "high"]},
                "investment_goal": {"type": "string"}
            },
            "required": ["monthly_surplus", "risk_appetite"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculate_budget":
        income       = tool_input["income"]
        expenses     = tool_input["expenses"]
        savings_goal = tool_input.get("savings_goal_percent", 20)
        total_exp    = sum(expenses.values())
        surplus      = income - total_exp
        savings_pct  = round((surplus / income * 100), 2) if income > 0 else 0
        return json.dumps({
            "total_income":     income,
            "total_expenses":   total_exp,
            "surplus":          surplus,
            "savings_percent":  savings_pct,
            "savings_goal":     savings_goal,
            "on_track":         savings_pct >= savings_goal,
            "expense_breakdown": expenses
        })

    elif tool_name == "categorize_expenses":
        keywords = {
            "food":          ["zomato", "swiggy", "restaurant", "cafe", "grocery", "bigbasket", "food", "hotel"],
            "transport":     ["uber", "ola", "petrol", "metro", "bus", "fuel", "rapido", "train", "flight"],
            "rent":          ["rent", "pg", "hostel", "house", "flat"],
            "entertainment": ["netflix", "amazon prime", "hotstar", "movie", "game", "spotify", "concert"],
            "healthcare":    ["pharmacy", "doctor", "hospital", "medicine", "apollo", "clinic", "lab"],
            "shopping":      ["amazon", "flipkart", "myntra", "mall", "clothes", "meesho"],
            "utilities":     ["electricity", "water", "internet", "airtel", "jio", "recharge", "wifi"]
        }
        categorized = []
        for txn in tool_input["transactions"]:
            desc = txn["description"].lower()
            cat  = "others"
            for category, kws in keywords.items():
                if any(kw in desc for kw in kws):
                    cat = category
                    break
            categorized.append({**txn, "category": cat})
        return json.dumps({"categorized_transactions": categorized})

    elif tool_name == "analyze_spending_pattern":
        analysis = []
        for m in tool_input["monthly_data"]:
            income  = m.get("income", 0)
            total   = sum(m.get("expenses", {}).values())
            savings = income - total
            analysis.append({
                "month":           m["month"],
                "total_spent":     total,
                "income":          income,
                "savings":         savings,
                "savings_percent": round(savings / income * 100, 2) if income > 0 else 0
            })
        return json.dumps({"monthly_analysis": analysis})

    elif tool_name == "generate_savings_plan":
        income   = tool_input["income"]
        expenses = tool_input["expenses"]
        surplus  = income - sum(expenses.values())
        target   = tool_input.get("target_amount", 0)
        months   = tool_input.get("timeline_months", 12)
        monthly_needed = target / months if months > 0 and target > 0 else surplus * 0.5
        return json.dumps({
            "monthly_surplus":     surplus,
            "recommended_savings": round(monthly_needed, 2),
            "feasible":            surplus >= monthly_needed,
            "goal":                tool_input.get("goal"),
            "target_amount":       target,
            "timeline_months":     months
        })

    elif tool_name == "investment_suggestions":
        risk    = tool_input.get("risk_appetite", "medium")
        surplus = tool_input["monthly_surplus"]
        options = {
            "low":    ["PPF (Public Provident Fund)", "Fixed Deposit (FD)", "Sukanya Samriddhi Yojana", "NSC"],
            "medium": ["SIP in Mutual Funds", "ELSS Tax Saving Funds", "NPS", "Balanced Mutual Funds"],
            "high":   ["Direct Equity (Stocks)", "Small Cap Mutual Funds", "REITs", "Index Funds"]
        }
        return json.dumps({
            "monthly_investment_capacity": surplus,
            "risk_appetite":               risk,
            "suggested_options":           options.get(risk, options["medium"]),
            "tip":                         "Always keep 3-6 months emergency fund before investing."
        })

    return json.dumps({"error": f"Unknown tool: {tool_name}"})
