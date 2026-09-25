import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from urllib.parse import urlencode

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
AUTHORIZE_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"

REDIRECT_URI = "http://localhost:8000/callback"

TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"

SCOPES = "User.Read offline_access"

app = FastAPI()


@app.get("/login")
def login():

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }

    authorization_url = (
        f"{AUTHORIZE_URL}?{urlencode(params)}"
    )

    return {
        "authorization_url": authorization_url
    }

# @app.get("/callback")
# def callback(code: str):
#     return {
#         "authorization_code": code
#     }

refresh_token_store = None

@app.get("/callback")
def callback(code: str):

    global refresh_token_store

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }

    response = httpx.post(
        TOKEN_URL,
        data=data,
    )

    response.raise_for_status()

    token_response = response.json()

    print("TOKEN RESPONSE:")
    print(token_response)

    # Get the access token
    access_token = token_response['access_token']

    # Refresh Token
    refresh_token_store = token_response["refresh_token"]

    # Call MS Graph
    graph_url = "https://graph.microsoft.com/v1.0/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    graph_response = httpx.get(
        graph_url,
        headers= headers
    )

    graph_response.raise_for_status()

    # Return the graph response
    user_data = graph_response.json()

    print("Graph response:")
    print(user_data)

    return user_data


@app.get("/refresh")
def refresh():

    if not refresh_token_store:
        return {
            "error": "No refresh token available. Login first."
        }

    refresh_data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token_store,
        "scope": SCOPES,
    }

    response = httpx.post(
        TOKEN_URL,
        data=refresh_data,
    )

    response.raise_for_status()

    new_token_response = response.json()

    print("Refresh response:")
    print(new_token_response)

    new_access_token = new_token_response["access_token"]

    graph_url = "https://graph.microsoft.com/v1.0/me"

    headers = {
        "Authorization": f"Bearer {new_access_token}"
    }

    graph_response = httpx.get(
        graph_url,
        headers=headers
    )

    graph_response.raise_for_status()

    user_data = graph_response.json()

    print("Graph response using refreshed token:")
    print(user_data)

    return user_data
