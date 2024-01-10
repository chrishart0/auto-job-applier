Relevant learning materials
* Intro to building with GenAI using LangChain and Open AI <https://learn.deeplearning.ai/langchain/lesson/1/introduction>
* https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction


### 1) Prepare the keys
First, prepare the OpenAPI key. 


Create these key files in the `backend` directory filled in with values from the appropriate services: 
* `openai_api_key.txt`
    * <https://platform.openai.com/api-keys>
* `search_api_key.txt`
    * <https://www.searchapi.io/>
* `serp_api_key.txt`
    * <https://serpapi.com/>
* `langchain_key.txt`
    * <https://smith.langchain.com/>
 This file is added in the .gitignore so it will not be committed if you clone this repo.



### 2) Statup the API
There are two ways to run the backend. if you'd like to run FastAPI without docker then follow these steps. 

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

Startup te API with SAM to mock API Gateway and lambda locally



