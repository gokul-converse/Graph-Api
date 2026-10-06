import asyncio

from delegated.src.agent import agent


async def main():

    session_id = "test-session-001"

    session = agent.create_session(
        session_id=session_id
    )

    result = await agent.run(
        "My name is Gokul",
        session=session
    )

    print("AGENT RESPONSE:")
    print(result.text)

    print("\nSESSION ID:")
    print(session.session_id)


if __name__ == "__main__":
    asyncio.run(main())