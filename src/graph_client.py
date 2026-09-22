# access token → Graph API → data

# import httpx

# from auth import get_access_token


# # GRAPH_URL = "https://graph.microsoft.com/v1.0/users"
# # GRAPH_URL = (
# #     "https://graph.microsoft.com/v1.0/users"
# #     "?$select=id,displayName,mail"
# #     "&$top=5"
# # )
# # GRAPH_URL = (
# #     "https://graph.microsoft.com/v1.0/users"
# #     "?$select=id,displayName,mail"
# #     "&$filter=startswith(displayName,'Gokul')"
# # )
# # GRAPH_URL = (
# #     "https://graph.microsoft.com/v1.0/users"
# #     "?$select=id,displayName,mail"
# #     "&$filter=startswith(displayName,'G')"
# #     "&$orderby=displayName"
# #     "&$count=true"
# #     "&$top=5"
# # )

# # GRAPH_URL = (
# #     "https://graph.microsoft.com/v1.0/users"
# #     "?$select=id,displayName,mail"
# #     "&$top=2"
# # )

# GRAPH_URL = "https://graph.microsoft.com/v1.0/users"

# access_token = get_access_token()

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "ConsistencyLevel": "eventual",                 # That's incomplete. $orderby=displayName alone can work normally, but combining $filter and $orderby requires advanced-query handling for /users
# }

# # response = httpx.get(
# #     GRAPH_URL,
# #     headers=headers,
# # )

# # response.raise_for_status()

# # data = response.json()

# all_users=[]
# url=GRAPH_URL

# while url:
#     response = httpx.get(url, headers=headers)
#     response.raise_for_status()

#     data = response.json()

#     all_users.extend(data["value"])

#     url = data.get("@odata.nextLink")

# print(f"Total users: {len(all_users)}")
# print(all_users)






# # dynamic url gen
# import httpx

# from auth import get_access_token


# GRAPH_URL = "https://graph.microsoft.com/v1.0/users"


# # 1. Get access token
# access_token = get_access_token()


# # 2. Headers
# headers = {
#     "Authorization": f"Bearer {access_token}",
# }


# # 3. Query parameters
# params = {
#     "$select": "id,displayName,mail",
#     "$top": 5,
# }


# # 4. Call Microsoft Graph
# response = httpx.get(
#     GRAPH_URL,
#     headers=headers,
#     params=params,
# )


# # 5. Check for errors
# response.raise_for_status()


# # 6. Read response
# data = response.json()


# # 7. Print result
# print(data)



# Dynamic query param
import httpx

from auth import get_access_token


GRAPH_URL = "https://graph.microsoft.com/v1.0/users"


def search_users(
    name: str | None = None,
    email: str | None = None,
    top: int = 10,
):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "$select": "id,displayName,mail",
        "$top": top,
    }

    filters = []

    if name:
        filters.append(
            f"startswith(displayName,'{name}')"
        )

    if email:
        filters.append(
            f"mail eq '{email}'"
        )

    if filters:
        params["$filter"] = " and ".join(filters)

    # -----------------------------
    # Pagination
    # -----------------------------

    all_users = []

    url = GRAPH_URL
    first_request = True

    while url:

        if first_request:
            response = httpx.get(
                url,
                headers=headers,
                params=params,
            )

            first_request = False

        else:
            response = httpx.get(
                url,
                headers=headers,
            )

        response.raise_for_status()

        data = response.json()

        all_users.extend(data["value"])

        url = data.get("@odata.nextLink")

    return all_users

