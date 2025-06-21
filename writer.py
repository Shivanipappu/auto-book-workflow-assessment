import google.generativeai as genai
import os


genai.configure(api_key="AIzaSyAALJ-v5wcxzh75DZyMhdyp55bTyjcSkYI")


model = genai.GenerativeModel("gemini-1.5-flash")

def spin_content(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating rewritten content: {str(e)}"
