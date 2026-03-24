import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def ask_ai(question):
    try:
        prompt = f"""You are a helpful academic assistant for college students.
Answer this question clearly and concisely: {question}"""
        response = model.generate_content(prompt)
        return {"answer": response.text, "error": None}
    except Exception as e:
        return {"answer": None, "error": str(e)}