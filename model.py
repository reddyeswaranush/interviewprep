from google import generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API keys from .env
API_KEYS = os.getenv("API_KEYS", "").split(",")

# Try each key until one works
def get_model():
    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            model.generate_content("ping")  # Test the key
            return model
        except Exception:
            continue
    raise Exception("All API keys failed")

def getscore(question, answer):
    model = get_model()
    prompt = f"""
You are an interview expert but be a little free not toooo strict. A user was asked the following interview question:

Question: {question}

Their answer was: "{answer}"

Please do the following:
1. Rate the answer from 1 to 10 based on relevance, clarity, and depth.
2. Provide detailed feedback on how the answer can be improved in a single line.
Respond in the format:
1.  **Rating:** <score>/10
2.  **Feedback:** <your feedback here>
"""
    response = model.generate_content(prompt)
    text = response.text.strip()

    score = -1
    feedback = "No feedback"
    for line in text.split("\n"):
        if "**Rating:**" in line:
            try:
                score = int(line.split("**Rating:**")[1].split("/")[0].strip())
            except:
                score = -1
        if "**Feedback:**" in line:
            feedback = line.split("**Feedback:**")[1].strip()

    return score, feedback

def finalsummary(feedback_list):
    model = get_model()
    prompt = f"""
You are given a list of feedback. You need to summarize it and give an ultimate feedback in 5-6 points.

feedback: {feedback_list}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
