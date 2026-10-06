from . import auth_state
from typing import Annotated
from agent_framework import tool

from delegated.src.graph_client import find_chat, get_messages, send_message


@tool(name="get_messages", description="Get the latest messages from a person's one-on-one Teams chat.")
def get_messages_tool(person_name: Annotated[str, "Name of the person whose one-on-one Teams chat messages should be retrieved."]):

    if not auth_state.access_token_store:
        return {
            "status": "error",
            "message": "User is not logged in. Please log in first.",
            "error_code": "NotAuthenticated",
        }

    chat_id = find_chat(
        auth_state.access_token_store,
        person_name
    )

    if not chat_id:
        return {
            "error": f"No one-on-one chat found with {person_name}."
        }

    messages = get_messages(
        auth_state.access_token_store,
        chat_id
    )

    return messages


# print("TOOL:")
# print(get_messages_tool)



@tool(name="send_message", description="Send a message to a person's one-on-one Teams chat as the logged-in user.")
def send_message_tool(
    person_name: Annotated[str, "Name of the person whose one-on-one Teams chat the message should be sent to."],
    message: Annotated[str, "The message text to send."]):

    if not auth_state.access_token_store:
        return {
            "status": "error",
            "message": "User is not logged in. Please log in first.",
            "error_code": "NotAuthenticated",
        }

    chat_id = find_chat(
        auth_state.access_token_store,
        person_name
    )

    if not chat_id:
        return {
            "error": f"No one-on-one chat found with {person_name}."
        }

    result = send_message(
        auth_state.access_token_store,
        chat_id,
        message
    )

    return result


print("GET MESSAGES SCHEMA:")
print(get_messages_tool.parameters())

print("\nSEND MESSAGE SCHEMA:")
print(send_message_tool.parameters())