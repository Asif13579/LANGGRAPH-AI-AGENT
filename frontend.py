import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="AI Agent",page_icon="🤖",layout="wide")

# Title
st.title("🤖 AI Agent Chatbot")
st.write("FastAPI + LangGraph + GEMINI+ Tavily")

# System Prompt
system_prompt=st.text_area("System Prompt",value="You are a helpful AI assistant",height=100)

# Models
MODEL_NAMES_GEMINI=["llama-3.3-70b-versatile"]

# Model Selection
selected_model=st.selectbox("Select Model",MODEL_NAMES_GEMINI)

# Search Toggle
allow_search=st.checkbox("Enable Web Search",value=True)

# User Input
user_query=st.text_area("Ask Anything",height=150,placeholder="Type your question here...")

# Submit Button
if st.button("Ask Agent"):
    if not user_query.strip():
        st.warning("Pleae enter a question")
        st.stop()
    payload={
        "model_name": selected_model,
        "model_provider": "groq",
        "system_prompt": system_prompt,
        "message": user_query,
        "allow_search": allow_search
    }

    try:
        with st.spinner("Thinking ..."):
            response=requests.post("http://127.0.0.1:8000/chat",json=payload,timeout=120)
            data=response.json()
            if data.get("success"):
                st.subheader("🤖 Response")
                st.write(data['response'])
            else:
                st.error(data.get("error","Unknown Error"))
    except Exception as e:
        st.error(f"Connection Error: {e}")
        