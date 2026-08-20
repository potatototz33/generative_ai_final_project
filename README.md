# Backend Starter

This is your starting point for the backend part of your final project. It
already runs, it just doesn't talk to OpenAI yet, that's the part you'll
add using your backend prompt from the workbook.

## Folder structure

```
backend_starter/
  app.py
  requirements.txt
  .env.example
  static/
    index.html   <- your frontend goes here
```

Everything your frontend needs (HTML, CSS, JS, images) must live inside
`static/`. The backend can only serve files from that folder. When you
write your frontend prompt, tell your AI coding assistant to save its
files into `static/`.

## Setup

These steps take you from a fresh clone to a running app.

1. **Clone the repo**

   ```
   git clone <your-repo-url>
   cd pokedex-project
   ```

2. **Create a virtual environment** (recommended, keeps dependencies isolated)

   ```
   python3 -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Set up your API key**

   Copy the example env file and fill in your own key.

   ```
   cp .env.example .env
   ```

   Then open `.env` and replace the placeholder with your real OpenAI API key:

   ```
   OPENAI_API_KEY=sk-your-real-key-here
   ```

   You can get a key from https://platform.openai.com/api-keys. Never commit your
   real `.env` file, it's already excluded in `.gitignore`


5. **Run the app**

   ```
   python app.py
   ```

6. **Open it in your browser**

   Go to http://localhost:5000

## Test the /chat route without a frontend

```
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"hello\"}"
```

You should get back something like `{"reply": "(placeholder) You said: hello"}`.

## Connecting your real frontend

Once you build your real frontend and save it into `static/`, its
JavaScript can call the backend like this:

```javascript
const response = await fetch("/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: userInput }),
});
const data = await response.json();
console.log(data.reply);
```

Note it's just `/chat`, not a full URL, since your frontend and backend
are now served from the same place.

## What's left to do

Open `app.py` and look for the `TODO` comment inside the `/chat` route.
That's where your backend prompt comes in: give it to your AI coding
assistant along with this file and ask it to fill in the real OpenAI
call using your system prompt and user prompt. The OpenAI client is
already set up for you, `client`, you just need to use it.