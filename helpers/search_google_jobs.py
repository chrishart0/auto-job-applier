# helpers/search_google_jobs.py
from langchain.tools import Tool
from langchain.agents import tool

import requests
import os

##################
### Setup keys ###
##################

# Import all keys from keys.env file as environment variables
from dotenv import load_dotenv
load_dotenv()

##################

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

        return jobs
    except Exception as e:
        print(f"Error in jobs call: {e}")
        return f"Error in jobs call, please tell the user about this: {e}"

@tool
def search_google_jobs_Tool(query: str) -> int:
    """Takes a search query and search for jobs"""
    return search_google_jobs(query)

