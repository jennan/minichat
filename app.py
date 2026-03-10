import os

os.environ["MLFLOW_USE_DEFAULT_TRACER_PROVIDER"] = "false"

import mlflow
import streamlit as st
from strands import Agent
from strands.models.ollama import OllamaModel


@mlflow.trace
def process_message(user_input):
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": "test_user",
            "mlflow.trace.session": "test_session",
        }
    )
    msg = st.session_state.agent(prompt)
    return msg


mlflow.set_experiment("Test Experiment")
mlflow.strands.autolog()

# TODO add widget to enter username in sidebar
# TODO add button to start new session (use uuid for session name)

if "agent" not in st.session_state:
    model_id = os.environ["MODEL_ID"]
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    # TODO pull model via REST API
    model = OllamaModel(host=ollama_host, model_id=model_id)
    agent = Agent(model=model)
    st.session_state.agent = agent

for message in st.session_state.agent.messages:
    with st.chat_message(message["role"]):
        text = message["content"][0]["text"]
        st.markdown(message["content"][0]["text"])

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)
    process_message(prompt)
    st.rerun()
