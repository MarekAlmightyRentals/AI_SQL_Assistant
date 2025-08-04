import os
import streamlit as st
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from db import get_engine

def get_agent():
    # Get OpenAI key from .env or secrets.toml
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

    # Get SQLAlchemy-compatible engine
    engine = get_engine()

    # Initialize LangChain database and model
    db = SQLDatabase(engine)
    llm = OpenAI(
        temperature=0,
        model="gpt-4",
        openai_api_key=openai_key
    )

    # Bind LLM to SQL database
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create SQL Agent
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        handle_parsing_errors=True
    )
