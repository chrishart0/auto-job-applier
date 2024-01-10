# This guide will walk you through creating a basic tool using agent with memory using LangChain's LCEL (Language Chain Execution Language) and OpenAI under the hood.

# Video Overview: https://www.youtube.com/watch?v=08qXj9w-CG4
# Agent Concepts: https://python.langchain.com/docs/modules/agents/concepts


import requests

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent, tool
from langchain.agents import AgentExecutor

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


# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

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
        # "api_key": get_search_api_key(),
        "num": num_results # Number of results to return
    }

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
    for job in jobs:
        print(f"""
            Title: {job['title']}
            Company: {job['company']}
            Job: {job['url']}"""
        )

    return jobs

### Configure all tools for agent ###
@tool
def search_google_jobs_Tool(query: str) -> int:
    """Takes a search query and search for jobs"""
    return search_google_jobs(query)

# ### Configure all tools for agent ###

tools = [
    Tool(
        name="Google-Jobs-Search",
        description="Search for open jobs listings with the Google Jobs API. Pay close attention to the sort of job the user is requesting before searching.",
        func=search_google_jobs_Tool.run,
    )
]


