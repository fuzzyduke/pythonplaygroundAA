import os
import logging
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging to see more output
logging.basicConfig(level=logging.DEBUG)

async def main():
    agent = Agent(
        task="open the brave browser, and Compare the price of GPT-4o and DeepSeek-V3.",
        llm=ChatOpenAI(model="gpt-3.5-turbo")
    )

    await agent.run()

asyncio.run(main())
