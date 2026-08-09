import os
from dotenv import load_dotenv
load_dotenv('local.env');

def get_gemini_api_key():
    return os.environ["GEMENI_API_KEY"]

def get_gemini_llm_model():
    return os.environ["GEMINI_MODEL"]

def get_gemini_embedding_model():
    return os.environ["GEMINI_EMBEDDING_MODEL"]
