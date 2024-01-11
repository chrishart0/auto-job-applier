# helpers/resume_pdf_summarizer.py
# Takes a resume PDF and returns a short summary of the types of jobs the user is qualified to apply for
from langchain.tools import Tool
from langchain.agents import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import os

##################
### Setup keys ###
##################

# Import all keys from keys.env file as environment variables
from dotenv import load_dotenv
load_dotenv()

##################

resume_fixer_prompt = """
The following text is a resume which has been converted from a PDF to text. It may be poorly formatted. 
Please return a cleaned up version of the resume in markdown format.
-----------------
Here is the resume:

{resume_text}
"""

def pdf_to_text(path):
    """Converts a PDF to markdown maintaining the formatting"""
    # Check if converted file already exists at "{path}.md"
    if os.path.exists(f"{path}.md"):
        print("Converted PDF already exists, returning existing file")
        with open(f"{path}.md", "r") as f:
            return f.read()

    # Convert the PDF to text
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()

    print("Raw PDF")
    print(pages)
    print("\n\n")

    # Use AI to fix the formatting
    prompt = ChatPromptTemplate.from_template(resume_fixer_prompt)
    model = ChatOpenAI(model="gpt-4")
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"resume_text": pages})

    # Save the fixed resume to a file
    with open(f"{path}.md", "w") as f:
        f.write(response)

    return response

resume_summarizer_prompt = """
You are an expert in the field of job searching, the number one recruiter at a large recruiting firm. 
You have been asked to make a list of the types of jobs this person is qualified for.
Be specific about the level of job, such as junior designer, sr full stack engineer, etc
If information is missing or minimal, leave it out of the list.
Give a markdown bulleted list of potential job titles which can be looked for with a justifiable reason for each.
Only return the list of jobs and nothing else. 
-----------------
Here is the resume:
 
{resume_text}
"""

def summarize_resume(resume_text):
    prompt = ChatPromptTemplate.from_template(resume_summarizer_prompt)
    model = ChatOpenAI(model="gpt-4")
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"resume_text": resume_text})
    return response


resume_text =  pdf_to_text("resumes/Resume.pdf")
print(resume_text)
print("\n\n")

print(summarize_resume(resume_text))