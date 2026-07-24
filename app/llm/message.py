import json
import logging
from anthropic import  Anthropic
from fastapi import HTTPException
from pydantic import ValidationError
from app.core.config import settings
from app.llm.use_tools import excecute_tools
from app.schemas.itinerary import ItineraryContent
from app.schemas.llm import itineraries_output_schema,weather_tool_schema
from app.tools.weather import get_weather
from app.utils.prompt_registry import load_prompt_name



client = Anthropic( api_key=settings.ANTHROPIC_API_KEY)
model = settings.MODEL_NAME
max_token = settings.MAX_TOKEN
temperature= float(settings.TEMPERATURE)
logger = logging.getLogger(__name__)

def add_user_message(messages,text):
    message = {
        "role":"user",
        "content":text
    }
    messages.append(message)
    
def add_assistant_message(messages,response):
    message = {
        "role":"assistant",
        "content":response.content
    }
    messages.append(message)

def text_from_message(message):
    return "\n".join(block.text for block in message.content if block.type =="text")

system_prompt = load_prompt_name("travel_planner_system",version=2).template
itinerary_prompt = load_prompt_name("itinerary_generation",version=2).template



def run_tools(user_prompt, tools=None, system=None):
    messages = []
    add_user_message(messages, user_prompt)

    params = {
        "model": model,
        "messages": messages,
        "max_tokens": max_token,
        "system": system or system_prompt,
        "temperature":temperature,
        "output_config":itineraries_output_schema
    }
    if tools:
        params["tools"] = tools

    response = client.messages.create(**params)
    add_assistant_message(messages, response)

    while response.stop_reason == "tool_use":
        tools_result = [
            excecute_tools(block)
            for block in response.content
            if block.type == "tool_use"
        ]
        add_user_message(messages, tools_result)
        response = client.messages.create(**params)
        add_assistant_message(messages, response)
        
        if response.stop_reason == "refusal":
            raise HTTPException(status_code=422, detail="Model declined to generate this itinerary")
        if response.stop_reason == "max_tokens":
            raise HTTPException(status_code=502, detail="Itinerary generation was truncated")


    return text_from_message(response)



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
    
