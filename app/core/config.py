from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATA_BASE_URL: str
    TOKEN_EXPIRE_MINUTES:int
    SECRET_KEY:str
    ALGORITHM:str
    class Config:
        env_file=".env"
settings = Settings()