import google.generativeai as genai
import os


genai.configure(api_key="AIzaSyAALJ-v5wcxzh75DZyMhdyp55bTyjcSkYI")


model = genai.GenerativeModel("gemini-1.5-pro")

def review_content(text: str) -> str:
    prompt = (
        "You're an expert editor. Review the following content for clarity, grammar, and flow. "
        "Provide suggestions for improvement:\n\n" + text
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating review: {str(e)}"
