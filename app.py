import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from weather_tool import get_weather
from search_tool import google_search


# ----------------------------------------
# 1. Load environment variables
# ----------------------------------------

load_dotenv()


# ----------------------------------------
# 2. Create Gemini LLM
# ----------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash"
)


# ----------------------------------------
# 3. Create LangChain Agent
# ----------------------------------------

agent = create_agent(
    model=llm,

    tools=[
        get_weather,
        google_search
    ],

    system_prompt="""
You are a helpful AI assistant.

You have two tools.

TOOL 1: get_weather

Use get_weather when the user asks about:
- weather
- temperature
- humidity
- rain
- precipitation
- wind
- forecast

The current weather tool supports Hyderabad, India.


TOOL 2: google_search

Use google_search when the user asks about:
- companies
- company leadership
- CEOs
- executives
- people
- organizations
- recent news
- current events
- latest technology information
- information that may have changed recently
- any question that requires current web information


IMPORTANT:

Choose the appropriate tool based on the
user's intent.

Do not invent current information.

If the user asks for current information
that may have changed, use google_search.

If the user asks about Hyderabad weather,
use get_weather.

If the user's question requires information
from both tools, use both tools.

After receiving the tool results, provide
a clear and concise answer.
"""

)


# ----------------------------------------
# 4. Start conversation
# ----------------------------------------

print("==========================================")
print("        Multi-Tool AI Agent")
print("==========================================")
print()
print("Available tools:")
print("1. Weather - Open-Meteo")
print("2. Google Search - Gemini Search Grounding")
print()
print("Type 'exit' to quit.")
print()


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
        )

        final_message = result["messages"][-1]

        # Gemini 3.x can return content blocks.
        if hasattr(final_message, "text"):
            print("\nAgent:", final_message.text)

        else:
            print("\nAgent:", final_message.content)

        print()

    except Exception as e:

        print("\nAgent error:", str(e))
        print()