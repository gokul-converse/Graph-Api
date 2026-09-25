################ InMemory Token caching

# import os

# import msal
# from dotenv import load_dotenv


# load_dotenv()


# TENANT_ID = os.getenv("TENANT_ID")
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# AUTHORITY = (
#     f"https://login.microsoftonline.com/{TENANT_ID}"
# )

# SCOPES = [                                                                              #Use the permissions already configured/consented for this application for Microsoft Graph.
#     "https://graph.microsoft.com/.default"
# ]


# app = msal.ConfidentialClientApplication(
#     client_id=CLIENT_ID,
#     client_credential=CLIENT_SECRET,
#     authority=AUTHORITY,
# )


# def get_access_token():
#     result = app.acquire_token_for_client(
#         scopes=SCOPES
#     )

#     if "access_token" not in result:
#         raise Exception(
#             f"Could not acquire token: {result}"
#         )

#     print(result)

#     return result["access_token"]


# # if __name__ == "__main__":
# #     get_access_token()

# if __name__ == "__main__":
#     token1 = get_access_token()
#     token2 = get_access_token()

#     print("Same token:", token1 == token2)



########### Persistent Token Caching
import os

import msal
from dotenv import load_dotenv
from msal_extensions import (
    FilePersistence,
    PersistedTokenCache,
)


load_dotenv()


TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


AUTHORITY = (
    f"https://login.microsoftonline.com/{TENANT_ID}"
)


SCOPES = [
    "https://graph.microsoft.com/.default"
]


# ---------------------------------------
# Persistent token cache
# ---------------------------------------

cache_location = "token_cache.bin"

persistence = FilePersistence(cache_location)

cache = PersistedTokenCache(
    persistence
)


# ---------------------------------------
# MSAL application
# ---------------------------------------

app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY,
    token_cache=cache,
)


# ---------------------------------------
# Get access token
# ---------------------------------------

def get_access_token():

    result = app.acquire_token_for_client(
        scopes=SCOPES
    )

    if "access_token" not in result:
        raise Exception(
            f"Could not acquire token: {result}"
        )

    return result["access_token"]


# ---------------------------------------
# Test
# ---------------------------------------

if __name__ == "__main__":

    token1 = get_access_token()

    print("Token acquired.")

    token2 = get_access_token()

    print("Same token in same process:")
    print(token1 == token2)