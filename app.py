import os

os.environ["MLFLOW_USE_DEFAULT_TRACER_PROVIDER"] = "false"

import mlflow
import streamlit as st
from strands import Agent
from strands.models.litellm import LiteLLMModel


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

if "agent" not in st.session_state:
    model = LiteLLMModel(
        model_id="hosted_vllm/Qwen/Qwen3-0.6B",
        client_args={"base_url": "http://localhost:8000/v1"},
    )
    #model = LiteLLMModel(
    #    client_args={
    #        "api_key": "sk-1234",
    #        "base_url": "http://localhost:4000",
    #    },
    #    model_id="litellm_proxy/gemma3",
    #)
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
