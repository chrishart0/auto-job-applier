# This guide will walk you through creating a basic tool using agent with memory using LangChain's LCEL (Language Chain Execution Language) and OpenAI under the hood.

# Video Overview: https://www.youtube.com/watch?v=08qXj9w-CG4
# Agent Concepts: https://python.langchain.com/docs/modules/agents/concepts

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent, tool
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from helpers.search_google_jobs import search_google_jobs_Tool
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

    return response.get("output")


#######################################
### Setup Chat interface in console ###
#######################################

# Now add a simple chat interface
def run_chat():
    chat_history = [ SystemMessage (content="Hello, I am a job search bot. I can help you find jobs. What kind of job are you looking for?")]

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