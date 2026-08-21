import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv('local.env');

llm = ChatGoogleGenerativeAI(
    model = os.environ["GEMINI_MODEL"],
    google_api_key = os.environ["GEMENI_API_KEY"],
    temperature=0.7)

def get_llm():
    return llm

def llm_with_tools(tools: list):
    return llm.bind_tools(tools)

    # return llm.bind_tools(tools, parallel_tool_calls=False)

def invoke(message:str)-> str:
    result = llm.invoke(message) 
    return result

def llm_ollama():
    return ChatOllama(
    model="llama3.2:3b",
    temperature=0
)
