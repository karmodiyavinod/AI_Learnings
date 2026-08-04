import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

load_dotenv('local.env');

llm = GoogleGenerativeAI(
    model = os.environ["GEMINI_MODEL"],
    google_api_key = os.environ["GEMENI_API_KEY"],
    temperature=0.7)

def invoke(message:str)-> str:
    result = llm.invoke(message)    
    return result

