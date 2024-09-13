from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")

class Config(BaseSettings):
    bot_token: str
    admin_id: int
    db_path: str = Field(default="db/users.db")

    model_config = SettingsConfigDict(env_file=DOTENV)
