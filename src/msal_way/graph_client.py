
import httpx

from auth import get_access_token


GRAPH_URL = "https://graph.microsoft.com/v1.0/users"


access_token = get_access_token()
print(access_token)

headers = {
    "Authorization": f"Bearer {access_token}",
}


params = {
    "$select": "id,displayName,mail",
    "$top": 2,
}


response = httpx.get(
    GRAPH_URL,
    headers=headers,
    params=params,
)


response.raise_for_status()


data = response.json()


print(data)


