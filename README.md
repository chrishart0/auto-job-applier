Relevant learning materials
* Intro to building with GenAI using LangChain and Open AI <https://learn.deeplearning.ai/langchain/lesson/1/introduction>
* https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction


### 1) Prepare the keys
First, prepare the OpenAPI key. 


Copy the `.env.example` file and rename the new file `.env`

This example uses OpenAI, search API, and LangChain. Follow the below links to get the proper values to fill our your key file
* OpenAI
    * <https://platform.openai.com/api-keys>
* SERP
    * <https://www.searchapi.io/>
    * This is used for making a google searche tool to be used by the AI agent

* We use LangChain's LangSmith for observability. You can also disable this if you like by setting the value for `LANGCHAIN_TRACING_V2` to false
    * <https://smith.langchain.com/>


 This file is added in the `.gitignore` so it will not be committed


### 2) Start up the chat


Install prereqs
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

Run the python script which starts the API, as shown below.
```
python app.py
```




