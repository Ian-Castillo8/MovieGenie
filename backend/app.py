import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are MovieGenie, a movie-guessing chatbot.
Ask ONLY yes/no questions.
Ask ONE question at a time.
Use logic based on the movie list provided.
When confident, guess the movie using:
"I think your movie is _____. Am I right?"
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat_response(user_msg):
    messages.append({"role": "user", "content": user_msg})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    bot = response.choices[0].message["content"]
    messages.append({"role": "assistant", "content": bot})
    return bot

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chat_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
