from langchain_groq import ChatGroq
from app.config import settings

def get_llm():
    return ChatGroq(
        groq_api_key = settings.GROQ_API_KEY,  ## authentication
        model_name = settings.MODEL_NAME,  ## which model to use
        temperature = 0.3)  ## deterministic model