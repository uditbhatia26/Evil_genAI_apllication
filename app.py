import os

from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests  # Importing requests to handle the ConnectionError exception

## Langsmith Tracking
## Langsmith Tracking using Streamlit secrets
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY']="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"
os.environ['LANGCHAIN_PROJECT']="SIMPLE GEN AI PROJECT"

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
