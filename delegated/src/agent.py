from agent_framework import Agent
from .tools import get_messages_tool, send_message_tool
from config.settings import client

agent = Agent(
    client=client,
    name="Teams Agent",
    description="An AI assistant that helps users interact with Microsoft Teams.",
    instructions="""
    You are a Microsoft Teams assistant.

    Understand the user's request and use the available
    Teams tools when required.

    Use tool results as the source of truth.
    Do not invent Teams messages or information.

    If a tool returns no results, clearly inform the user.

    If required information is missing, ask the user
    for clarification.

    Keep responses clear, concise, and useful.
    """,
    tools=[
        get_messages_tool,
        send_message_tool,
    ],

)

session = agent.create_session()