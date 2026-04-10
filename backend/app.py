"""
app.py
Streamlit UI for Lexi Legal Assistant (client for core_logic.py).

- Uses get_legal_response from core_logic.py
- Keeps UI logic, no RAG logic duplication
"""

import streamlit as st
from backend.core_logic import get_legal_response

st.set_page_config(page_title="Lexi Legal Assistant", layout="centered")
st.title("Lexi Legal Assistant")

st.markdown("""
- Ask legal questions about Nepali law
- Choose your response style: Professional (GitHub) or Gen-Z
""")

query = st.text_input("Enter your legal question:")
mode = st.selectbox("Response Style", ["github", "gen-z"], format_func=lambda x: "Professional" if x=="github" else "Gen-Z")

if st.button("Ask Lexi") and query:
    with st.spinner("Lexi is thinking..."):
        result = get_legal_response(query, mode)
        st.markdown(f"**Answer:** {result['answer']}")
        st.markdown(f"**Source:** {result['metadata']}")
        st.markdown("**Process Logs:**")
        for log in result["process_logs"]:
            st.write(f"- {log}")
