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
async def authorize_mediavalet(code: str, scope: str, state: str):
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
    result = response.json()
    print(result)

    f = open("media_token.txt", "w")
    f.write(result["access_token"])
    f.close()

    return result

@app.get("/folders")
async def get_folders():
    url = "https://api.mediavalet.com/folders"
    f = open("media_token.txt", "r")
    auth_token = f.read()
    f.close()

    response = requests.get(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        "Ocp-Apim-Subscription-Key": "03e0a3d8270a432d9ede6e2cfca073dd",
        "Authorization": "Bearer " + auth_token,
    })
    result = response.json()
    print(result)

    return result


