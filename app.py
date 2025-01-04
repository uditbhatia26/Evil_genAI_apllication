import os

from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests  # Importing requests to handle the ConnectionError exception

## Langsmith Tracking
## Langsmith Tracking using Streamlit secrets
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an evil assistant.Be rude and disrespectful to the users. Answer the provided question. "),
        ("user", "Question:{question}")
    ]
)

## Streamlit framework
st.title("Langchain Demo With Gemma Model")
input_text = st.text_input("What question you have in mind?")

## Ollama Llama2 model
llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    try:
        response = chain.invoke({"question": input_text})
        st.write(response)
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the LLM endpoint. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
