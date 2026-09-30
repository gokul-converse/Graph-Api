import os
import httpx
def find_chat(access_token, person_name):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    chats_url = "https://graph.microsoft.com/v1.0/me/chats"

    params = {
        "$top": 50
    }

    response = httpx.get(
        chats_url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    chats = response.json()["value"]

    for chat in chats:

        if chat.get("chatType") != "oneOnOne":
            continue

        chat_id = chat["id"]

        members_url = (
            f"https://graph.microsoft.com/v1.0/chats/"
            f"{chat_id}/members"
        )

        members_response = httpx.get(
            members_url,
            headers=headers
        )

        members_response.raise_for_status()

        members = members_response.json()["value"]

        print("\nCHAT MEMBERS:")

        for member in members:
            print(
                "Display Name:",
                member.get("displayName"),
                "| User ID:",
                member.get("userId"),
                "| Email:",
                member.get("email")
            )

        for member in members:

            display_name = member.get("displayName", "")

            if display_name.lower() == person_name.lower():

                print("MATCH FOUND!")
                print("Person:", display_name)
                print("Chat ID:", chat_id)
                print("Chat type:", chat.get("chatType"))
                print("Chat topic:", chat.get("topic"))

                # print("ALL MEMBERS:")
                # for m in members:
                #     print(
                #         m.get("displayName"),
                #         m.get("email"),
                #         m.get("userId")
                #     )

                return chat_id

    return None

def get_messages(access_token, chat_id):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    messages_url = (
        f"https://graph.microsoft.com/v1.0/chats/"
        f"{chat_id}/messages"
    )

    params = {
        "$top": 5
    }

    response = httpx.get(
        messages_url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    messages_data = response.json()

    return messages_data

def send_message(access_token, chat_id, message):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    send_url = (
        f"https://graph.microsoft.com/v1.0/chats/"
        f"{chat_id}/messages"
    )

    message_data = {
        "body": {
            "contentType": "text",
            "content": message
        }
    }

    response = httpx.post(
        send_url,
        headers=headers,
        json=message_data
    )

    response.raise_for_status()

    return response.json()