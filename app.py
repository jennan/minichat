import os
import uuid
from pathlib import Path

os.environ["MLFLOW_USE_DEFAULT_TRACER_PROVIDER"] = "false"

import ollama
import mlflow
import streamlit as st
from strands import Agent
from strands.models.ollama import OllamaModel
from strands import tool


@tool
def list_files():
    """list files in current project folder"""
    return sorted(str(p) for p in Path(__file__).parent.iterdir())


@tool
def read_file(filename):
    """return the content of a file in current project folder"""
    root_folder = Path(__file__).parent
    filepath = (Path(__file__).parent / filename).resolve()
    if not filepath.is_relative_to(root_folder):
        raise ValueError(f"{filename} is not inside the project folder")
    if not filepath.is_file():
        raise ValueError(f"{filename} is not a file.")
    return filepath.read_text()


@mlflow.trace
def process_message(user_input, user_id, session_id):
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": user_id,
            "mlflow.trace.session": session_id,
        }
    )
    msg = st.session_state.agent(prompt)
    return msg


mlflow.set_experiment("Test Experiment")
mlflow.strands.autolog()

with st.sidebar:
    user_id = st.text_input("User ID", "test_user")
    new_session = st.button("New session")

if "agent" not in st.session_state or new_session:
    model_id = os.environ["MODEL_ID"]
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    ollama.Client(ollama_host).pull(model_id)
    model = OllamaModel(host=ollama_host, model_id=model_id)
    agent = Agent(model=model, tools=[list_files, read_file])
    st.session_state.agent = agent
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.caption(f"**Session ID:** {st.session_state.session_id}")

for message in st.session_state.agent.messages:
    with st.chat_message(message["role"]):
        content = message["content"][0]
        if "text" in content:
            st.markdown(content["text"])
        else:
            st.json(content)

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)
    process_message(prompt, user_id, st.session_state.session_id)
    st.rerun()
