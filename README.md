# generative_ai_final_project

This is your starting point for the backend part of your final project. It
already runs, it just doesn't talk to OpenAI yet, that's the part you'll
add using your backend prompt from the workbook.

## Setup

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to a new file named `.env` and paste in your real
   OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Run the server:
   ```
   python app.py
   ```
4. You should see it running at `http://localhost:5000`

## Test it without a frontend

You can check the server works before connecting your frontend, using a
terminal command:

```
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"hello\"}"
```

You should get back something like `{"reply": "(placeholder) You said: hello"}`.

## Connecting your frontend

From your frontend's JavaScript, send a POST request to `/chat`:

```javascript
const response = await fetch("http://localhost:5000/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: userInput }),
});
const data = await response.json();
console.log(data.reply);
```

## What's left to do

Open `app.py` and look for the `TODO` comments. That's where your backend
prompt comes in: give it to your AI coding assistant along with this file
and ask it to fill in the real OpenAI call using your system prompt and
user prompt.