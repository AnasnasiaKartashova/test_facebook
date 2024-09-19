from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    BASE_URL: str
    ACCESS_TOKEN: str
    VERIFY_TOKEN: str


settings = Settings()
