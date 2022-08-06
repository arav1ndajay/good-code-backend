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

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]

origins = ['*']

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


# print(settings.client_id)
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
        category = {
            "id": res["id"],
            "name": res["tree"]["name"]
        }
        categories.append(category)

    return categories


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


# @app.post("/")
# async def authorize_mediavalet(code: str, db: Session = Depends(get_db)):
#     # url2 = "https://api.mediavalet.com/users/current"
#     # response2 = requests.get(url2, headers={
#     #     'Content-Type': 'application/x-www-form-urlencoded',
#     #     "Ocp-Apim-Subscription-Key": settings.primary_key,
#     #     "Authorization": "Bearer " + auth_token,
#     # })
#     # result2 = response2.json()
#     # id = result2["payload"]["id"]

#     # db_user = models.User(id=id, auth_token=auth_token)
#     # user = db.get(models.User, id)
#     # if not user:
#     #     db.add(db_user)
#     #     db.commit()
#     #     db.refresh(db_user)
#     # else:
#     #     setattr(user, "auth_token", auth_token)
#     #     db.commit()
#     #     db.refresh(user)

#     # encoded_jwt = jwt.encode({"id": id}, "secret", algorithm="HS256")
#     # return RedirectResponse(settings.frontend_url + "/redirect/" + encoded_jwt.decode("UTF-8"))
