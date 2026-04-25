import os
from dotenv import load_dotenv 
from google import genai
from google.genai import types
import json
import pandas as pd

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_input(user_input, prompt):
    if not user_input.strip():
        return "[]"

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                response_mime_type="application/json" 
            ),
            contents=user_input
        )
        return response.text
    except Exception as e:
        print(f"Error analyzing input: {e}")
        return "[]"

def categorizer(user_input: pd.DataFrame, prompt=None):
    prompt = """
            You are a category analyzer for a personal expense tracker application.
            The user will provide a list of financial transactions.
            Analyze EACH transaction and categorize it into:
            Food, Travel, Entertainment, Utilities, Health, Education, Shopping, Others, Income, Investment, Savings.
            Reply ONLY in valid JSON as a LIST of objects:
            [
              {
                "description": "Original transaction description",
                "category": "CategoryName"
              },
              ...
            ]
            """
    json_input = user_input.to_json(orient="records")
    category_json = analyze_input(json_input, prompt)
    try:
        return json.loads(category_json)
    except:
        return []
