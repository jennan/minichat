# Mini-Chatbot

This repository is a tiny experiment where I put together few toolboxes together to get a realistic chatbot system:

- `streamlit` for the interface,
- `strands` for the agentic aspects,
- `mlflow` for the trace and evaluation,
- `litellm` proxy to support multiple backends and control budget,
- `vllm` as default local LLM backend,
- `nginx` to add basic authentication and url remapping, 
- `podman-compose` to orchestrate the services.

## Development mode

No need to start everything when developing, just run vllm and the app:

- in a first terminal, run the vllm server

```bash
podman run \
  --device nvidia.com/gpu=all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 8000:8000 \
  --ipc=host \
  docker.io/vllm/vllm-openai:latest --model Qwen/Qwen3-0.6B --reasoning-parser qwen3
```

- in *another* terminal, start the app:

```bash
export MODEL_ID="hosted_vllm/Qwen/Qwen3-0.6B"
export BASE_URL="http://localhost:8000/v1"
pixi run chatbot
```

- (optional) in *another* terminal run mlflow server to check saved traces:

```bash
pixi run mlflow server
```

## Deployment mode

TODO setup docker-compose to run all services

```bash
podman compose up
```
