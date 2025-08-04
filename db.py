import os
import pyodbc
import streamlit as st
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_engine():
    # Retrieve credentials from environment or Streamlit secrets
    server = os.getenv("MSSQL_SERVER") or st.secrets["MSSQL_SERVER"]
    database = os.getenv("MSSQL_DATABASE") or st.secrets["MSSQL_DATABASE"]
    username = os.getenv("MSSQL_USERNAME") or st.secrets["MSSQL_USERNAME"]
    password = os.getenv("MSSQL_PASSWORD") or st.secrets["MSSQL_PASSWORD"]
    driver = os.getenv("MSSQL_DRIVER") or st.secrets["MSSQL_DRIVER"]

    # Validate input
    if not all([server, database, username, password, driver]):
        raise ValueError("❌ One or more database settings are missing from environment or secrets.")

    # Fix escaped backslashes in server name (if any)
    server = server.replace('\\\\', '\\')

    # Create the ODBC connection string
    odbc_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    # Return a SQLAlchemy engine using the pyodbc connection
    def connect():
        return pyodbc.connect(odbc_str)

    return create_engine("mssql+pyodbc://", creator=connect)

def reflect_db():
    engine = get_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata.tables.keys()
