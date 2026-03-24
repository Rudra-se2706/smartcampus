from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful academic assistant for college students. Answer questions clearly and concisely."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return {"answer": response.choices[0].message.content, "error": None}
    except Exception as e:
        return {"answer": None, "error": str(e)}