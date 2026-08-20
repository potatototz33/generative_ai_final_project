"""Protestant Potato Flask application.

Run with: python app.py
Then visit http://127.0.0.1:5000
"""

import json
import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import OpenAI, OpenAIError

load_dotenv()

SYSTEM_PROMPT = (
    "You are a encouraging robot, who is cheerful, informative, and inspiring. "
    "You are a search engine that gives the user protest events to go to. "
    "Always factcheck yourself, and remain on topic. Respond in a kind, "
    "informative, but concise tone."
)
EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array", "minItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}, "location": {"type": "string"},
                    "date": {"type": "string"}, "time": {"type": "string"},
                    "description": {"type": "string"}, "source_url": {"type": "string"},
                },
                "required": ["name", "location", "date", "time", "description", "source_url"],
                "additionalProperties": False,
            },
        },
        "search_note": {"type": "string"},
    },
    "required": ["events", "search_note"], "additionalProperties": False,
}

app = Flask(__name__, static_folder="static")


def validate_search(data: dict) -> tuple[dict | None, str | None]:
    """Validate the JSON body without adding a separate validation dependency."""
    required_fields = ("city", "state", "event_type", "day")
    if not isinstance(data, dict) or any(not str(data.get(field, "")).strip() for field in required_fields):
        return None, "city, state, event_type, and day are required."

    values = {field: str(data[field]).strip() for field in required_fields}
    if len(values["city"]) > 80 or len(values["state"]) > 80 or len(values["event_type"]) > 120:
        return None, "One or more fields are too long."
    try:
        values["day"] = date.fromisoformat(values["day"])
    except ValueError:
        return None, "day must use the YYYY-MM-DD format."
    return values, None


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.post("/api/events")
def find_events():
    """Find at least three verified, display-ready local events."""
    search, error = validate_search(request.get_json(silent=True))
    if error:
        return jsonify({"detail": error}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"detail": "OPENAI_API_KEY is not configured. Add it to your .env file and restart the server."}), 503

    user_prompt = (
        "Please enter an event, day, city and state.\n\n"
        f"Event: {search['event_type']}\nDay: {search['day'].strftime('%A, %B %d, %Y')}\n"
        f"City: {search['city']}\nState: {search['state']}\n\n"
        "Search the web before answering. Return exactly three or more real, public events "
        "that are on the requested day and relevant to the event. Do not invent events. "
        "For each result, provide the published name, venue/address, local date, start time, "
        "a 2-3 sentence description, and a direct source URL. If fewer than three verified "
        "matches exist, include nearby or closely related public civic events and explain that in search_note."
    )
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.6"),
            instructions=SYSTEM_PROMPT,
            input=user_prompt,
            tools=[{"type": "web_search"}],
            text={"format": {"type": "json_schema", "name": "event_search_results", "strict": True, "schema": EVENT_SCHEMA}},
        )
        return jsonify(json.loads(response.output_text))
    except json.JSONDecodeError:
        return jsonify({"detail": "The event search returned invalid JSON. Please try again."}), 502
    except OpenAIError as error:
        return jsonify({"detail": f"Unable to search for events: {error}"}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)
