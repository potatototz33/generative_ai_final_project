# Protestant Potato

A Flask-powered, scrapbook-style search engine for local protests, civic actions, and community events.

## Run it

1. Create and activate a virtual environment (optional but recommended).
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`, then enter your OpenAI API key.
4. Start the app: `python app.py`
5. Open `http://127.0.0.1:5000`.

## API

`POST /api/events` expects city, state, event_type, and an ISO-format day. It returns JSON containing at least three results with a name, location, day, time, description, and source URL. The backend uses the OpenAI Responses API with web search and a strict JSON schema so event details can be fact-checked and displayed safely.
