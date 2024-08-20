from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

app=FastAPI(
    title="Langchain Server",
    version="1.0.0",
    description="A simple API server"
)

add_routes(
    app,
    GoogleGenerativeAI(model="gemini-pro"),
    path="/googleai"
)

llm= GoogleGenerativeAI(model="gemini-pro")

prompt=ChatPromptTemplate.from_template("Write an essay about {topic} with 100 words")

add_routes(
    app,
    prompt | llm,
    path="/essay"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)