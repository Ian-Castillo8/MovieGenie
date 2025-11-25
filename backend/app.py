import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Load movie data
def load_movie_data(filepath="movieData.txt"):
    movies = {}
    current_movie = None
    questions = []

    if not os.path.exists(filepath):
        print("⚠ movieData.txt not found. Running without movie list.")
        return movies

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                if current_movie and questions:
                    movies[current_movie] = questions[:]
                current_movie = line[1:-1]
                questions = []
            else:
                questions.append(line)

        if current_movie and questions:
            movies[current_movie] = questions

    print("✔ Loaded movieData.txt successfully.")
    return movies

movie_data = load_movie_data()
movie_list_text = "\n".join([f"- {m} ({len(q)} questions)" for m, q in movie_data.items()])

SYSTEM_PROMPT = f"""
You are MovieGenie, a movie-guessing chatbot.

Movies you know:
{movie_list_text}

Rules:
- Ask only YES/NO questions.
- Ask ONE question at a time.
- When confident, say:
  "I think your movie is _____. Am I right?"
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat_response(user_msg):
    messages.append({"role": "user", "content": user_msg})

    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages
    )

    bot_message = response.output[0].content[0].text
    messages.append({"role": "assistant", "content": bot_message})

    return bot_message

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chat_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
