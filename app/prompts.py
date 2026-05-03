## to give instructions to the LLM

from langchain_core.prompts import ChatPromptTemplate

def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful tech AI assistant. Your name is Alex and you should strictly answer the questions if they are from the tech domain. else mention I dont know"),  ## system for behaviour ddefinition
        ("human", "{input}")  ## placeholder for user input
    ])