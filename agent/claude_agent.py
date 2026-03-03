"""
FinBot — AI Agent using Groq API (FREE Alternative)
Model: llama-3.3-70b-versatile (Free, Fast)
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from agent.tools import finance_tools, execute_tool
from agent.prompts import FINANCE_SYSTEM_PROMPT

load_dotenv()

MODEL = "llama-3.3-70b-versatile"   # Free Groq model


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found! "
            "Get FREE key from: https://console.groq.com "
            "Add to .env: GROQ_API_KEY=gsk_your_key_here"
        )
    return Groq(api_key=api_key)


def run_agent(
    user_message:   str,
    financial_data: dict = {},
    extra_prompt:   str  = "",
    chat_history:   list = []
) -> dict:
    """
    Agentic loop using Groq API with tool use.
    Returns: { "reply": str, "tool_calls_made": list }
    """
    client = get_client()

    # Build content
    if financial_data:
        content = (
            f"Financial Data:\n{json.dumps(financial_data, indent=2)}"
            f"\n\nUser Query: {user_message}"
        )
    else:
        content = user_message

    # Build system prompt
    system = FINANCE_SYSTEM_PROMPT
    if extra_prompt:
        system += f"\n\nExtra Context:\n{extra_prompt}"

    # Build messages with history
    messages = [{"role": "system", "content": system}]
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": content})

    # Convert tools to Groq/OpenAI format
    groq_tools = [
        {
            "type": "function",
            "function": {
                "name":        tool["name"],
                "description": tool["description"],
                "parameters":  tool["input_schema"]
            }
        }
        for tool in finance_tools
    ]

    tool_calls_made = []
    final_reply     = ""

    # ── Agentic Loop ──────────────────────────────────────────────────────────
    for _ in range(10):
        response = client.chat.completions.create(
            model       = MODEL,
            messages    = messages,
            tools       = groq_tools,
            tool_choice = "auto",
            max_tokens  = 2048
        )

        msg = response.choices[0].message

        # Model wants to use tools
        if msg.tool_calls:
            messages.append({
                "role":       "assistant",
                "content":    msg.content or "",
                "tool_calls": [
                    {
                        "id":       tc.id,
                        "type":     "function",
                        "function": {
                            "name":      tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in msg.tool_calls
                ]
            })

            for tc in msg.tool_calls:
                tool_name = tc.function.name
                try:
                    tool_input = json.loads(tc.function.arguments)
                except Exception:
                    tool_input = {}

                result_str = execute_tool(tool_name, tool_input)
                try:
                    result_parsed = json.loads(result_str)
                except Exception:
                    result_parsed = {"raw": result_str}

                tool_calls_made.append({
                    "tool":   tool_name,
                    "input":  tool_input,
                    "result": result_parsed
                })

                messages.append({
                    "role":         "tool",
                    "tool_call_id": tc.id,
                    "content":      result_str
                })

        # Done
        else:
            final_reply = msg.content or ""
            break

    return {
        "reply":           final_reply.strip(),
        "tool_calls_made": tool_calls_made
    }