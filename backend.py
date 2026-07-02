import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
#from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

app=FastAPI(title="AI Agent Backend")

# Request Schema
class RequestState(BaseModel):
    model_names: str
    model_provider: str
    system_prompt: str
    message: str
    allow_search: bool

# Gemini LLM
llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature=0.7,google_api_key=os.getenv("GEMINI_API_KEY"))

# Tavily Search Tool
search_tool=TavilySearch(max_results=5,tavily_api_key=os.getenv("TAVILY_API_KEY"))

# Agent
agent=create_react_agent(model=llm,tools=[search_tool])

@app.get("/")
def home():
    return {'status':'running','message':'AI Agent Backend is live'}

@app.post('/chat')
def chat(request: RequestState):
    try:
        result=agent.invoke({'message':[{'role':'system','content':request.system_prompt},{'role':'user','content':request.message}]})
        return {'success':True,'response':result['messages'][-1].content}
    except Exception as e:
        return {'success':False,'error':str(e)}