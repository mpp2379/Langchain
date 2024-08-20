import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

def get_googleapi_response(input_text):
    response=requests.post("http://localhost:8000/essay/invoke",json={'input':{'topic':input_text}})
    return response.json()['output']

st.title("Language demo with Google API")
input_text=st.text_input("Write essay on")

if input_text:
    st.write(get_googleapi_response(input_text))
