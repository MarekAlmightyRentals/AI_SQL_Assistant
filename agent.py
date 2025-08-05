import os
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from db import get_engine

def get_agent():
    # Use env first, then Streamlit secrets
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

    engine = get_engine()
    db = SQLDatabase(engine)

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini",  # or "gpt-4" if you prefer
        api_key=openai_key,
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # import here so it uses the same version as toolkit
    from langchain_community.agent_toolkits.sql.base import create_sql_agent

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        handle_parsing_errors=True,
    )
