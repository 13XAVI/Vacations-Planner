
from pydantic import BaseModel

class  WeatherReq(BaseModel):
    name:str
    
class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    wind_speed: float
    weather_code: int