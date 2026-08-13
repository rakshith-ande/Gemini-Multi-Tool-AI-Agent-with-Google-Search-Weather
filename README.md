# Gemini-Multi-Tool-AI-Agent-with-Google-Search-Weather
LangChain-based Gemini AI agent that intelligently selects between Google Search and Open-Meteo Weather tools to provide real-time web information and weather insights based on user intent.

## Overview

This project demonstrates how to build a multi-tool AI agent using **LangChain and Google Gemini**. The agent understands the user's query and automatically selects the appropriate tool based on the user's intent.

The agent currently supports:

- **Google Search** – Retrieves current information from the web using Gemini's Google Search grounding.
- **Weather** – Retrieves weather and forecast information using the Open-Meteo API.

## Architecture

```text
                         User Query
                              |
                              v
                    +-------------------+
                    |   LangChain Agent |
                    |    Google Gemini  |
                    +---------+---------+
                              |
                       Analyze User Intent
                              |
                 +------------+------------+
                 |                         |
                 v                         v
        +----------------+        +------------------+
        | Weather Tool   |        | Google Search    |
        | get_weather()  |        | google_search()  |
        +-------+--------+        +--------+---------+
                |                          |
                v                          v
        +---------------+          +----------------+
        | Open-Meteo API|          | Google Search  |
        +-------+-------+          |   Grounding    |
                |                  +--------+-------+
                |                           |
                +-------------+-------------+
                              |
                              v
                         Gemini LLM
                              |
                              v
                        Final Response