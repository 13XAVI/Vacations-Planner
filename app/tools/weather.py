
import requests
from app.schemas.weather import WeatherResponse,WeatherReq


def get_weather(city:WeatherReq)-> WeatherResponse:
    response =  requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name" :city,
            "count":1    
        }
    )
    
    response.raise_for_status()
    results =  response.json()["results"]
    
    location = results[0]
    
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,weather_code,wind_speed_10m"
        }
    )
    weather.raise_for_status()
    
    current = weather.json()["current"]
    return WeatherResponse(
        city= location["name"],
        country=location["country"],
        temperature=current["temperature_2m"],
        wind_speed=current["wind_speed_10m"],
        weather_code=current["weather_code"]
    )

    