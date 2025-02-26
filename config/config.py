import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    db_name: str
    db_user: str
    db_pass: str 
    db_host: str
    db_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    model_config=SettingsConfigDict(env_file=os.getcwd() + "/config/.env")
