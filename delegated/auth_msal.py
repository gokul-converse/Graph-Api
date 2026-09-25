import os
import msal
from dotenv import load_dotenv
import httpx

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

app = msal.PublicClientApplication(                                     # Our application participating in a user authentication flow
    client_id=CLIENT_ID,
    authority=AUTHORITY,
)

SCOPES = [
    "User.Read"
]

result = app.acquire_token_interactive(
    scopes=SCOPES
)

access_token = result["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = httpx.get(
    "https://graph.microsoft.com/v1.0/me",
    headers=headers,
)

print(response.json())