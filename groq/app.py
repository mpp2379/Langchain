import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time

from dotenv import load_dotenv

load_dotenv()

## Load groq api key
groq_api_key= os.environ['GROQ_API_KEY']

if 'vector' not in st.session_state:
    st.session_state.embeddings= OllamaEmbeddings()
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs=st.session_state.loader.load()
    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.final_docs=st.session_state.text_splitter.split_documents(st.session_state.docs)
    st.session_state.vectors=FAISS.from_documents(st.session_state.final_docs,st.session_state.embeddings)

st.title("Chat Groq Demo")

llm=ChatGroq(groq_api_key=groq_api_key,
              model="Gemma-7b-It")

prompt= ChatPromptTemplate.from_template(
"""
Answer the question based on provided context only.
Please provide the most accurate response based on context.
<context>
{context}
<context>
Questions:{input}
"""
)


document_chain= create_stuff_documents_chain(llm,prompt)
retriever= st.session_state.vector.as_retriever()
retriever_chain= create_retrieval_chain(retriever, document_chain)

prompt=st.text_input("Input your prompt here")

if prompt:
    start=time.process_time()
    response= retriever_chain.invoke({"input":prompt})
    print("Response Time:",time.process_time()-start)
    st.write(response['Answer'])

    # streamlit expander
    with st.expander("Document similartity search"):
        # Find relevant chunks
        for i, doc in enumerate(response['Answer']):
            st.write(doc.page_content)
            st.write("----------------------")

