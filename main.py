from functools import lru_cache
from fastapi import FastAPI, Depends
from config.config import Settings
from db_config.sqlalchemy_connect import engine
from models.data.sqlalchemy_data import Base
from api import users

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router, prefix="/users")

@lru_cache
def fetch_config():
    return Settings()

@app.get('/users/ping')
def ping(): 
    return {'message': 'pong'}

@app.get('/users/config')
def index_student(config:Settings = Depends(fetch_config)): 
    return {
        'DB_NAME': config.db_name,
        'DB_USER': config.db_user,
        'DB_PASS': config.db_pass,
        'DB_HOST' : config.db_host,
        'DB_PORT': config.db_port,
        'SECRET_KEY': config.secret_key,
        'ALGORITHM' : config.algorithm,
        'DB_EXPIRE': config.access_token_expire_minutes,
      }


