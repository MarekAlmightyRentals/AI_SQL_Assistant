import streamlit as st
from agent import get_agent

st.set_page_config(page_title="AI SQL Assistant", layout="centered")
st.title("🤖 AI SQL Assistant")
st.markdown("Ask questions about your MSSQL database using natural language.")

query = st.text_input("Enter your question:")

if "agent" not in st.session_state:
    try:
        st.session_state.agent = get_agent()
    except Exception as e:
        st.error(f"❌ Failed to initialize AI agent: {e}")

if st.button("Run") and query:
    with st.spinner("🤖 Thinking..."):
        try:
            result = st.session_state.agent.run(query)
            st.success("✅ Done!")
            st.text_area("Result:", result, height=200)
        except Exception as e:
            st.error(f"❌ Error during execution: {e}")
