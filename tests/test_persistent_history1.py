import asyncio

from delegated.src.agent import agent


async def main():

    session_id = "test-session-001"

    session = agent.create_session(
        session_id=session_id
    )

    print("SESSION ID:")
    print(session.session_id)

    result = await agent.run(
        "What is my name?",
        session=session
    )

    print("\nAGENT RESPONSE:")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())