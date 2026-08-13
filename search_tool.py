import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from langchain.tools import tool


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Create Google Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# --------------------------------------------------
# Google Search Tool
# --------------------------------------------------

@tool
def google_search(query: str) -> str:
    """
    Search the web using Google's Search grounding.

    Use this tool when the user asks for:
    - company information
    - CEO or leadership information
    - current events
    - recent news
    - latest technology information
    - people or organizations
    - information that may have changed recently
    """

    try:

        # Enable Google's native Search grounding
        google_search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # Call Gemini with Google Search enabled
        response = client.models.generate_content(
            model="gemini-3.5-flash",

            contents=query,

            config=types.GenerateContentConfig(
                tools=[
                    google_search_tool
                ]
            )
        )

        # -----------------------------------------
        # Get Gemini's answer
        # -----------------------------------------

        answer = response.text

        # -----------------------------------------
        # Extract search sources
        # -----------------------------------------

        sources = []

        try:

            grounding_metadata = (
                response.candidates[0].grounding_metadata
            )

            if grounding_metadata:

                grounding_chunks = (
                    grounding_metadata.grounding_chunks
                )

                if grounding_chunks:

                    for chunk in grounding_chunks:

                        web = getattr(
                            chunk,
                            "web",
                            None
                        )

                        if web:

                            title = getattr(
                                web,
                                "title",
                                "Unknown title"
                            )

                            uri = getattr(
                                web,
                                "uri",
                                None
                            )

                            if uri:

                                sources.append(
                                    f"- {title}: {uri}"
                                )

        except Exception:
            pass

        # -----------------------------------------
        # Return answer + sources
        # -----------------------------------------

        if sources:

            return (
                f"{answer}\n\n"
                "Sources:\n"
                + "\n".join(sources)
            )

        return answer

    except Exception as e:

        return f"Google Search failed: {str(e)}"