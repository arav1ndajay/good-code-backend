from fastapi import FastAPI
from pydantic import BaseModel
from .config import settings
import requests

app = FastAPI()

# print(settings.client_id)
class Req(BaseModel):
    code: str

# sample_response = {
#   "id_token":"ID_TOKEN_VALUE",
#   "access_token":"ACCESS_TOKEN_VALUE",
#   "expires_in":3600,
#   "token_type":"Bearer"
# }
  

@app.get("/")
async def lemmao(code: str, scope: str, state: str):
    url = "https://login.mediavalet.com/connect/token"
    print(code)
    response = requests.post(url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":settings.host_url,
        "client_id":settings.client_id,
        "client_secret":settings.client_secret,
    }, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    print(response.json())
    return response.json()

