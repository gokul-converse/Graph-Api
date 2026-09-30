import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from urllib.parse import urlencode
from config.settings import settings
from delegated.src.graph_client import find_chat, get_messages, send_message
from delegated.src.agent import agent
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# TENANT_ID = os.getenv("TENANT_ID")
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TENANT_ID=settings.tenant_id
CLIENT_ID=settings.client_id
CLIENT_SECRET = settings.client_secret

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
AUTHORIZE_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"

REDIRECT_URI = "http://localhost:8000/auth/callback"

TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"

SCOPES = "User.Read Chat.ReadWrite ChatMessage.Send offline_access"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
access_token_store = None


@app.get("/auth/callback")
def callback(code: str):

    global refresh_token_store
    global access_token_store

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
    access_token_store = token_response["access_token"]

    print("GRANTED SCOPES:")
    print(token_response.get("scope"))

    # Refresh Token
    refresh_token_store = token_response["refresh_token"]

    print("LOGIN SUCCESSFUL")

    # # Get messages from one particular chat
    # chat_id = "19:864bf157-ab10-43fe-839b-0422daeef2d6_edf83f23-cb9e-4a80-b44e-365ffa4f6d25@unq.gbl.spaces"

    # Send message to the selected chat

    return RedirectResponse(url="http://localhost:5173")

@app.get("/auth/status")
def auth_status():

    if access_token_store:
        return {
            "authenticated": True
        }

    return {
        "authenticated": False
    }

@app.get("/messages")
def messages():

    chat_id = find_chat(
        access_token_store,
        "Pragadheeswaran"
    )

    messages_data = get_messages(
        access_token_store,
        chat_id
    )

    return messages_data


@app.post("/send-message")
def send_teams_message(message: str):

    chat_id = find_chat(
        access_token_store,
        "Pragadheeswaran"
    )

    sent_message = send_message(
        access_token_store,
        chat_id,
        message
    )

    return {
        "message": "Message sent successfully",
        "chat_id": chat_id,
        "sent_message": sent_message
    }

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


@app.post("/agent")
async def run_agent(message: str):

    result = await agent.run(message)

    return {
        "response": result.text
    }