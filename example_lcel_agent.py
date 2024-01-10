# This guide will walk you through creating a basic tool using agent with memory using LangChain's LCEL (Language Chain Execution Language) and OpenAI under the hood.

# Video Overview: https://www.youtube.com/watch?v=08qXj9w-CG4
# Agent Concepts: https://python.langchain.com/docs/modules/agents/concepts

##################
### Setup keys ###
##################


import requests

# Import all keys from keys.env file as environment variables
from dotenv import load_dotenv
load_dotenv()