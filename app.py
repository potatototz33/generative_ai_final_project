"""
Starter Backend for Your Final Project
========================================

This file already does the boring plumbing for you:
  - starts a small web server (Flask)
  - loads your OpenAI API key safely from a .env file
  - lets your frontend talk to it without CORS errors
  - has one route, /chat, that your frontend can send messages to

Right now, /chat just echoes back whatever you send it. That's on
purpose. Your job is to use your BACKEND PROMPT (from your workbook)
to ask an AI coding assistant to fill in the TODO section below so
that /chat actually calls the OpenAI API using YOUR system prompt
and YOUR user prompt.

HOW TO RUN THIS:
  1. Open a terminal in this folder
  2. pip install -r requirements.txt
  3. Copy .env.example to a new file named .env and paste in your real API key
  4. python app.py
  5. Your server is now running at http://localhost:5000

HOW YOUR FRONTEND TALKS TO THIS:
  Send a POST request to http://localhost:5000/chat with a JSON body
  like {"message": "hello"}. You'll get back {"reply": "..."}.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file and loads OPENAI_API_KEY

app = Flask(__name__)
CORS(app)  # lets your frontend, running on a different port, talk to this server

# TODO: import the OpenAI library and create your client here.
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # ------------------------------------------------------------
    # TODO: Replace this echo with a real call to the OpenAI API.
    #
    # Use YOUR system prompt and YOUR user prompt from your workbook.
    # It should look something like this:
    #
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "YOUR SYSTEM PROMPT HERE"},
    #         {"role": "user", "content": user_message},
    #     ],
    # )
    # reply = response.choices[0].message.content
    #
    # Then return that instead of the placeholder line below.
    # ------------------------------------------------------------
    reply = f"(placeholder) You said: {user_message}"

    return jsonify({"reply": reply})


@app.route("/")
def home():
    return "Backend is running. Send a POST request to /chat to talk to it."


if __name__ == "__main__":
    app.run(debug=True, port=5000)