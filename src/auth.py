# # credentials → Entra → access token


########### This is for testing, we need to know how manual token gen is done with out msal ..

# import os
# import httpx
# from dotenv import load_dotenv

# import base64
# import json

# load_dotenv()

# TENANT_ID = os.getenv("TENANT_ID")
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# # manually constructed the token endpoint:
# TOKEN_URL = (f"https://login.microsoftonline.com/"              # URL belongs to the Microsoft identity platform / Entra ID token endpoint
#              f"{TENANT_ID}/oauth2/v2.0/token")

# # manually constructed the OAuth parameters:
# data = {
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET,
#     "scope": "https://graph.microsoft.com/.default",
#     "grant_type": "client_credentials",
# }

# # manually sent the HTTP request:
# response = httpx.post(TOKEN_URL, data= data)

# """# Hey Entra, here are my application credentials. I want an access token for Microsoft Graph.""" 

# print("Status:", response.status_code)

# token_response = response.json()

# access_token = token_response["access_token"]

# print("Token received:", bool(access_token))
# print("Expires in:", token_response["expires_in"])

# # Decode JWT payload for learning/debugging
# parts = access_token.split(".")

# payload = parts[1]

# padding = "=" * (-len(payload) % 4)

# decoded_payload = base64.urlsafe_b64decode(
#     payload + padding
# )

# claims = json.loads(decoded_payload)

# print("\nToken claims:")
# print(json.dumps(claims, indent=2))


# """
# Application permissions are represented in the token's roles claim.

# Delegated permissions are represented in scp.
# """

import os

import httpx
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = (
    f"https://login.microsoftonline.com/"
    f"{TENANT_ID}/oauth2/v2.0/token"
)


def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }

    response = httpx.post(
        TOKEN_URL,
        data=data,
    )

    response.raise_for_status()

    token_response = response.json()

    return token_response["access_token"]