import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a personal finance assistant. Your main goal is to clarify user doubts about their financial analysis.
You are provided with an analysis context that includes:
- Total Income, Investment, and Savings.
- Top 5 Expenses by Category.
- Bottom 5 Expenses by Category.
- An AI-generated summary.

Rules:
- When responding, always try to reference specific figures from the analysis (e.g., "Your top expense was Shopping at $X").
- Explicitly mention the Top/Bottom 5 expenses and the Income/Investment/Savings balance when giving advice or clarifying queries.
- Focus on explaining 'why' and 'how' based on these specific metrics.
- Keep responses helpful, professional, and directly tied to these metrics.
"""


def get_chat_response(user_message: str, conversation_history: list, expense_context: str = "") -> str:
    """Generate a chatbot response using Gemini, with optional expense data context."""
    
    contents = []
    
    if expense_context:
        contents.append({"role": "user", "parts": [{"text": f"[Context - my current expense data]\n{expense_context}"}]})
        contents.append({"role": "model", "parts": [{"text": "Got it! I have your expense data loaded. Feel free to ask me anything about your finances."}]})
    
    for msg in conversation_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})
    
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
            contents=contents,
        )
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"
