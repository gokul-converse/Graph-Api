import asyncio

from delegated.src.agent import agent


async def main():

    session = agent.create_session()

    print("\n--- FIRST MESSAGE ---")

    result = await agent.run(
        "Hi, my name is Gokul",
        session=session,
    )

    print(result.text)

    print("\n--- SECOND MESSAGE ---")

    result = await agent.run(
        "What is my name?",
        session=session,
    )

    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())