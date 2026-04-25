import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def summarize_expenses(top_expenses, bottom_expenses,income, investment, savings):  
    prompt = f"""
    You are an expense summarizer for a personal expense tracker application.
    Analyze the provided information and generate a concise summary of the user's financial situation.
    
    Data:
    - Top 5 expenses by category: {top_expenses.to_dict()}  
    - Bottom 5 expenses by category: {bottom_expenses.to_dict()}
    - Total income amount: {income}
    - Total investment amount: {investment}
    - Total savings amount: {savings}
    
    Provide insights into spending habits, income sources, and overall financial health.
    Suggest actionable recommendations for improvement.
    """
    
    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            config=genai.types.GenerateContentConfig(
                system_instruction="You are a helpful financial advisor.",
            ),
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

