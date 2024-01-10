from langchain import hub
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent, tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI


import requests

# Import all keys from keys.env file as environment variables
from dotenv import load_dotenv
load_dotenv()




def search_google_jobs( query, num_results=10):
    
    # https://www.searchapi.io/docs/google-jobs
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_jobs",
        "q": query,
        "gl": "us", # Country code
        #   "location": "Remote",
        "ltype": "1", # Work remote
        "api_key": get_search_api_key(),
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

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-tools-agent")

# Choose the LLM that will drive the agent
# Only certain models support this
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def send_message(message):
    response = agent_executor.invoke({"input": message})
    return response.get("output")

# agent_executor.invoke({"input": "give me an entry level job posting related to AWS DevOps that is remote"})


#######################################
### Setup Chat interface in console ###
#######################################

# Now add a simple chat interface
def run_chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break
        print("Bot:", send_message(user_input))


# Execute the chat interface
run_chat()