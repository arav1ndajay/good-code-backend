from os import access
from fastapi import FastAPI, Header, status, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from .config import settings
import requests
from starlette.middleware.cors import CORSMiddleware
from .survey123 import survey
import base64
import json
from .docusign import embeded_sender

app = FastAPI()

origins = [
    "http://localhost", "http://localhost:3000",
    "https://hackathonjgi.software"
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
async def get_assets_with_metadata_in_category(category_id: str, req: Request):
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

    url2 = "https://api.mediavalet.com/attributes"
    response2 = requests.get(url2,
                             headers={
                                 "Ocp-Apim-Subscription-Key":
                                 settings.primary_key,
                                 "Authorization": "Bearer " + access_token,
                             })
    result2 = response2.json()

    attributes = []

    for res in result2["payload"]:
        if res["name"] == "X" or res["name"] == "Y":
            attributes.append({"id": res["id"], "name": res["name"]})

    print(attributes)

    assets = []
    for res in result["payload"]["assets"]:
        if category_id in res["categories"] and attributes[0]["id"] in res[
                "attributes"]:
            asset = {"id": res["id"], "link": res["media"]["medium"]}
            assets.append(asset)

    print(assets)

    return assets


@app.post("/updatemetadata")
async def updatemetada(req: Request):
    body = await req.json()
    account_id = body["sender"]["accountId"]
    envelope_id = body["envelopeId"]

    url_fetch = f"http://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes/{envelope_id}/form_data"
    res1 = requests.get(url_fetch,
                            headers={
                                'Content-Type':
                                'application/x-www-form-urlencoded',
                                "Authorization": "Bearer " + access_token,
                            })
    ids = []
    for ans in res1["formData"]:
	    if ans["value"] == "X":
             ids.append(ans["name"])

    url = f"https://api.mediavalet.com/assets/{ids[0]}"

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
    category_id = result["payload"]["categories"][0]

    url2 = f"https://api.mediavalet.com/categories/{category_id}"

    response2 = requests.get(url2,
                             headers={
                                 'Content-Type':
                                 'application/x-www-form-urlencoded',
                                 "Ocp-Apim-Subscription-Key":
                                 settings.primary_key,
                                 "Authorization": "Bearer " + access_token,
                             })

    result2 = response2.json()

    cat_name = str(result2["payload"]["name"]).split("_", maxsplit=1)
    survey_info = survey.get_info(camera_id=cat_name[0].title(),
                                  date=cat_name[1])

    x_coord = survey_info["X"]
    y_coord = survey_info["Y"]

    # X and Y attribute ids are hardcoded for now
    for id in ids:
        url = f"https://api.mediavalet.com/assets/{id}/"

        response = requests.patch(
            url,
            headers={
                "Ocp-Apim-Subscription-Key": settings.primary_key,
                "Authorization": "Bearer " + access_token,
            },
            json=[{
                "op": "replace",
                "path": "/attributes/c0c67677-b8eb-4522-844b-a4aeb9be7807",
                "value": x_coord
            }, {
                "op": "replace",
                "path": "/attributes/6ce37da1-e78f-426a-9505-671fe9161272",
                "value": y_coord
            }])

    return {"metadata": "updated"}


@app.get("/attributes")
async def get_attributes(req: Request):
    url = "https://api.mediavalet.com/attributes"

    header = req.headers["Authorization"].split()
    access_token = ""
    if header[0] == "Bearer":
        access_token = header[1]
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = requests.get(url,
                            headers={
                                "Ocp-Apim-Subscription-Key":
                                settings.primary_key,
                                "Authorization": "Bearer " + access_token,
                            })
    result = response.json()

    attributes = []
    for res in result["payload"]:
        attributes.append({"id": res["id"], "name": res["name"]})

    print(attributes)

    return attributes


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


@app.post("/survey123/")
async def get_survey123(req: Request):
    details = await req.json()
    return survey.get_info(camera_id=details['camera_id'],
                           date=details['date'])


@app.get("/docusign/authorize")
async def authorize_mediavalet(code: str):

    integrator_and_secret_key = b"Basic " + base64.b64encode(
        str.encode("{}:{}".format(settings.docusign_client_id,
                                  settings.docusign_client_secret)))

    access_token_request_url = "https://account-d.docusign.com/oauth/token"

    access_token_response = requests.post(
        access_token_request_url,
        headers={
            "Authorization": integrator_and_secret_key.decode("utf-8"),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code
        })

    access_token_result = access_token_response.json()
    base_uri_request_url = "https://account-d.docusign.com/oauth/userinfo"

    base_uri_response = requests.get(base_uri_request_url,
                                     headers={
                                         "Authorization":
                                         "Bearer " +
                                         access_token_result['access_token']
                                     })

    base_uri_result = base_uri_response.json()
    response = {
        'access_token': access_token_result['access_token'],
        'base_uri': base_uri_result['accounts'][0]['base_uri'],
        'account_id': base_uri_result['accounts'][0]['account_id']
    }

    # with open('convert.txt', 'w') as convert_file:
    #     convert_file.write(json.dumps(response))

    return response


@app.post("/docusign/notify")
async def docusign_notify(req: Request):
    args = {
        'envelope_args': {
            'status': 'create'
        },
        'starting_view': 'recipient'
    }

    details = await req.json()
    args['account_id'] = details['account_id']
    args['ds_return_url'] = details['ds_return_url']
    args['access_token'] = details['access_token']
    args['base_path'] = details['base_uri']

    result = embeded_sender.EmbeddedSender.worker(args, details['assets'])

    return result
