from app.tools.weather import get_weather
from app.schemas.llm import weather_tool_schema

Tools = { weather_tool_schema["name"]:get_weather}

def excecute_tools(block):
    tool_func = Tools[block.name]
    try:
        result = tool_func(**block.input)
        is_error = False
    except Exception as e:
        result = f"Error: {e}"
        is_error = True

    return {
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": str(result),
        "is_error": is_error,
    }