from app.schemas.itinerary import ItineraryContent


itineraries_output_schema = {
    "format": {
        "type": "json_schema",
        "schema": ItineraryContent.model_json_schema(),
    }
}
weather_tool_schema = {
    "name": "get_weather",
    "description": (
        "Look up current weather conditions for a city, to help tailor "
        "itinerary recommendations (e.g. outdoor vs indoor activities)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Kigali'"}
        },
        "required": ["city"],
        "additionalProperties": False
    },
    "strict": True,
}