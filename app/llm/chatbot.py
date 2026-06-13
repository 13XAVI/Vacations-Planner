import json

from anthropic import  Anthropic
from app.core.config import settings
from app.llm.prompts import ITINERARY_SYSTEM_PROMPT, build_itinerary_prompt

client = Anthropic( api_key=settings.ANTHROPIC_API_KEY)
model = settings.MODEL_NAME


def generate_itineraries(destination: str, days: int, budget: float, travel_style: str):
    prompt = build_itinerary_prompt(destination, days, budget, travel_style)
    full_prompt = ""
    params = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "model": model,
        "temperature":0.3,
        "system":ITINERARY_SYSTEM_PROMPT
    }

    with client.messages.stream(**params) as stream:
        for chunk in stream.text_stream:
            full_prompt += chunk
            print(chunk, end="", flush=True)
    print()
    raw_response = full_prompt.strip()
    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]
    raw_response = raw_response.strip()

    try:
        itinerary_data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}")
    return itinerary_data
