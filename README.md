# 💰 FinBot — AI Personal Finance Assistant 

Finance Agent is an AI-powered conversational assistant designed to help users with finance-related queries and tasks. It leverages the Groq API for fast large language model inference, enabling quick and intelligent responses. The project uses a local SQLite database (finbot.db) to persist data such as chat history or financial records. It is built in Python and follows best practices like environment variable management via .env for secure API key storage. The agent is structured as a command-line or backend application, making it easy to extend with new financial tools or integrations. Overall, it serves as a smart financial assistant that combines AI capabilities with local data storage for a personalized experience.


---

## 📁 Project Structure

```
finbot-streamlit/
│
├── app.py                          ← 🏠 Home page (run this!)
├── requirements.txt                ← All dependencies
├── .env.example                    ← Copy to .env and add API key
│
├── pages/
│   ├── 1_💬_Chat.py               ← AI Chat with memory
│   ├── 2_📊_Budget_Planner.py     ← Budget analysis + charts
│   ├── 3_🏷️_Expense_Tracker.py   ← Add & categorize transactions
│   └── 4_💡_Financial_Advice.py  ← Savings & investment advice
│
├── agent/
│   ├── claude_agent.py             ← Core AI agent (agentic loop)
│   ├── tools.py                    ← 5 finance tools Claude uses
│   └── prompts.py                  ← System prompts
│
└── database/
    └── db.py                       ← SQLite database
```

---

## ⚙️ Step-by-Step Setup

### STEP 1 — Extract the zip
```
Unzip finbot-streamlit.zip
cd finbot-streamlit
```

### STEP 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### STEP 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### STEP 4 — Get Claude API Key
1. Go to https://console.anthropic.com
2. Sign up / Login → API Keys → Create Key
3. Copy the key (starts with sk-ant-...)

### STEP 5 — Setup .env file
```bash
# Create .env file in project root
# Add this line:
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### STEP 6 — Run the App! 🚀
```bash
streamlit run app.py
```

### STEP 7 — Open Browser
```
http://localhost:8501
```

---

## 🖥️ Pages & Features

| Page | Features |
|------|----------|
| 🏠 Home | Project overview |
| 💬 Chat | Free-form AI finance chat with memory |
| 📊 Budget Planner | Income/expense input + pie chart + bar chart + AI analysis |
| 🏷️ Expense Tracker | Add transactions + AI auto-categorize + spending charts |
| 💡 Financial Advice | Savings plans + investment advice + full checkup |

---

## 🤖 How Claude AI Works Here

```
User Input (Streamlit Form)
         ↓
run_agent() called
         ↓
Claude reads data + decides which tool to use
         ↓
Tools execute (calculate_budget, categorize_expenses, etc.)
         ↓
Results sent back to Claude
         ↓
Claude writes human-friendly advice
         ↓
Displayed on Streamlit UI
```

---

## 🛠️ Tech Stack

| Technology     | Purpose                     |
|----------------|-----------------------------|
| Streamlit      | Web UI framework            |
| Claude API     | AI brain (claude-sonnet-4-6)|
| Plotly         | Interactive charts          |
| SQLAlchemy     | Database ORM                |
| SQLite         | Local database              |
| Python-dotenv  | Environment variables       |

---

*Made with ❤️ 
Anii
