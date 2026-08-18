import json
from fastapi import HTTPException, logger
from pydantic import ValidationError
from app.llm.client import run_tools
from app.schemas.itinerary import ItineraryContent
from app.schemas.llm import itineraries_output_schema,weather_tool_schema
from app.utils.prompt_registry import load_prompt_name

itinerary_prompt = load_prompt_name("itinerary_generation",version=2).template
system_prompt = load_prompt_name("travel_planner_system",version=2).template


def buidld_iteneraries(destination, days, budget, travel_style):
    prompt = itinerary_prompt.format(
        destination=destination, days=days, budget=budget,
        travel_style=travel_style,
        output_schema=json.dumps(itineraries_output_schema["format"]["schema"], indent=2),
    )
    raw = run_tools(prompt, tools=[weather_tool_schema], system=system_prompt)
    try:
        content = ItineraryContent.model_validate_json(raw)
    except ValidationError as e:
        logger.error("Invalid itinerary payload from model: %s", e)
        raise HTTPException(status_code=502, detail="Model returned an invalid itinerary")
    return content