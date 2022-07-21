from configparser import ConfigParser
from fastapi import Depends, FastAPI, HTTPException, Header
from authmiddleware import AuthMiddleware
from config import getConfig
from starlette.middleware.base import BaseHTTPMiddleware


from db_helper import getTimezoneInfo, getAlltimeZones
app = FastAPI()
my_middleware = AuthMiddleware(['/'])
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)


@app.get("/")
def hello():
  return {"greetings" : "Hello how are you?"}

@app.get("/convert")
def convert(from_zone: str, to_zone: str, time_info: str):
    info = getTimezoneInfo(from_zone,to_zone, time_info)
    return info

@app.get("/timezones")
def timezones():
    info = getAlltimeZones()
    return info

