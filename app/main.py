from os import access
from fastapi import FastAPI, Header, status, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from .config import settings
import requests
# from sqlalchemy.orm import Session
# from . import models
# from .database import SessionLocal, engine
from starlette.middleware.cors import CORSMiddleware
from .survey123 import survey

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class Req(BaseModel):
    code: str


@app.post("/api/authorize")
async def authorize_mediavalet(code: Req):

    url = "https://login.mediavalet.com/connect/token"

    response = requests.post(
        url,
        data={
            "grant_type": "authorization_code",
            "code": code.code,
            "redirect_uri": settings.frontend_url,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'})

    result = response.json()
    print(result)

    return result


@app.post("/api/authorizerefresh")
async def authorize_mediavalet(rtoken: str):

    url = "https://login.mediavalet.com/connect/token"

    response = requests.post(
        url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": rtoken,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'})

    result = response.json()
    print(result)

    return result


@app.get("/categories")
async def get_categories(req: Request):
    url = "https://api.mediavalet.com/categories"

    header = req.headers["Authorization"].split()
    access_token = ""
    if header[0] == "Bearer":
        access_token = header[1]
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = requests.get(url,
                            headers={
                                'Content-Type':
                                'application/x-www-form-urlencoded',
                                "Ocp-Apim-Subscription-Key":
                                settings.primary_key,
                                "Authorization": "Bearer " + access_token,
                            })

    result = response.json()
    categories = []
    for res in result["payload"]:
        cat_name = str(res["tree"]["name"]).split("_", maxsplit=1)
        if res["assetCount"] > 0 and res["subcats"]["total"] == 0 and res[
                "tree"]["name"].count("_") == 3:
            category = {
                "id": res["id"],
                "name": cat_name[0],
                "date": cat_name[1]
            }
            categories.append(category)

    return categories


@app.get("/categories/{category_id}")
async def get_assets_in_category(category_id: str, req: Request):
    url = "https://api.mediavalet.com/assets"

    header = req.headers["Authorization"].split()
    access_token = ""
    if header[0] == "Bearer":
        access_token = header[1]
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = requests.get(url,
                            headers={
                                'Content-Type':
                                'application/x-www-form-urlencoded',
                                "Ocp-Apim-Subscription-Key":
                                settings.primary_key,
                                "Authorization": "Bearer " + access_token,
                            })
    result = response.json()

    assets = []
    for res in result["payload"]["assets"]:
        if category_id in res["categories"]:
            asset = {"id": res["id"], "link": res["media"]["medium"]}
            assets.append(asset)

    print(assets)

    return assets


@app.get("/user")
async def get_user():
    url = "https://api.mediavalet.com/users/current"

    try:
        f = open("media_token.txt", "r")
        auth_token = f.read()
        f.close()
    except FileNotFoundError:
        return {"error": "Auth token not found"}

    response = requests.get(url,
                            headers={
                                'Content-Type':
                                'application/x-www-form-urlencoded',
                                "Ocp-Apim-Subscription-Key":
                                settings.primary_key,
                                "Authorization": "Bearer " + auth_token,
                            })
    result = response.json()
    print(result["payload"]["id"])

    return result


@app.get("/survey123/")
async def get_survey123(camera_id: str, date: str):

    return survey.get_info(camera_id=camera_id, date=date)
