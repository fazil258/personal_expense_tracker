import os
import json
import pandas as pd
from dotenv import load_dotenv 
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def image_to_json(uploaded_file):
    prompt = """
    Extract all transaction records from this image into a list of objects.

    Rules:
    - Output MUST be valid JSON only.
    - Do not include markdown formatting tags (like ```json).
    - If transaction ID is missing, use "0".
    - Dates must be converted to YYYY-MM-DD.
    - Amount must be numeric (no negative values).

    Expected Format:
    [
        {
            "transaction_id": "string",
            "description": "string",
            "amount_spent": 12.34,
            "date": "YYYY-MM-DD"
        }
    ]
    """
    image_bytes = uploaded_file.getvalue()

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=uploaded_file.type
    )
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview", 
        config=types.GenerateContentConfig(
            system_instruction="You are a precise data extractor.",
            response_mime_type="application/json",
            response_schema=types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "transaction_id": types.Schema(type=types.Type.STRING),
                        "description": types.Schema(type=types.Type.STRING),
                        "amount_spent": types.Schema(type=types.Type.NUMBER),
                        "date": types.Schema(type=types.Type.STRING)
                    }
                )
            )
        ),
        contents=[image_part, prompt]
    )

    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    
    return json.loads(clean_text)

def image_to_df(image):
    data = image_to_json(image)
    return pd.DataFrame(data)