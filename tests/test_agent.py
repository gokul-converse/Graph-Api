import asyncio

from delegated.src.agent import agent


async def main():

    result = await agent.run(
        "Show me the latest 5 messages from Pragadheeswaran."
    )

    print("AGENT RESPONSE:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())