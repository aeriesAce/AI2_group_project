import google.generativeai as genai 
from dotenv import load_dotenv
import os 

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def Gemini(prompt: str) -> str:

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Fel {e}"




