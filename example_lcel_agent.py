# This guide will walk you through creating a basic tool using agent with memory using LangChain's LCEL (Language Chain Execution Language) and OpenAI under the hood.

# Video Overview: https://www.youtube.com/watch?v=08qXj9w-CG4
# Agent Concepts: https://python.langchain.com/docs/modules/agents/concepts

import requests
import os

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent, tool
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

##################
### Setup keys ###
##################


# Import all keys from keys.env file as environment variables
from dotenv import load_dotenv
load_dotenv()

##################


##### Create Agent #####

# An Agent is an LLM + Tools + Memory + the ability to think and execute tools until a goal is reached.

# Agent Types: https://python.langchain.com/docs/modules/agents/agent_types/
# Take a look at this, different agent types are better at different things, especially import if you are wanting to use a model other than OpenAI


###########################
### Configure all tools ###
###########################

# Track tool usage
tool_usage = []

### Tools Setup ###
def search_google_jobs( query, num_results=10):
    
    # https://www.searchapi.io/docs/google-jobs
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_jobs",
        "q": query,
        "gl": "us", # Country code
        #   "location": "Remote",
        "ltype": "1", # Work remote
        "api_key": os.getenv("SEARCHAPI_API_KEY"),
        "num": num_results # Number of results to return
    }

    try:
        response = requests.get(url, params = params)

        # Get just the Job titles and urls for each job
        jobs = []
        for job in response.json()['jobs']:
            jobs.append({
                'title': job['title'],
                'url': job['apply_link'],
                'company': job['company_name']
            })

        #Print jobs to console in a nice format
        # for job in jobs:
        #     print(f"""
        #         Title: {job['title']}
        #         Company: {job['company']}
        #         Job: {job['url']}"""
        #     )

        # Capture tool usage with unique key
        tool_usage.append(
            {
                "tool": "search_google_jobs",
                "query": query,
                "num_results": num_results,
                "results": jobs
            }
        )

        return jobs
    except Exception as e:
        print(f"Error in jobs call: {e}")
        return f"Error in jobs call, please tell the user about this: {e}"

@tool
def search_google_jobs_Tool(query: str) -> int:
    """Takes a search query and search for jobs"""
    return search_google_jobs(query)

### Configure all tools for agent ###

tools = [
    Tool(
        name="Google-Jobs-Search",
        description="Search for open jobs listings with the Google Jobs API. Pay close attention to the sort of job the user is requesting before searching.",
        func=search_google_jobs_Tool.run,
    )
]

#######################
### Setup the Agent ###
#######################

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def send_message(message, chat_history):
    response = agent_executor.invoke(
        {
            "input": message,
            "chat_history": chat_history,
        }
    )

    # Log tool usage just tool names
    if len(tool_usage) > 0:
        print("------")
        print("Tool Usage:")
        for tool in tool_usage:
            print("     - ", tool.get("tool"))
            
    return response.get("output")


#######################################
### Setup Chat interface in console ###
#######################################

# Now add a simple chat interface
def run_chat():
    chat_history = [ ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break
        response = send_message(user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        print("Bot:", response)

# Execute the chat interface
run_chat()