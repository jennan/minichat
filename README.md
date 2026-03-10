# Mini-Chatbot

This repository is a tiny experiment where I put together few toolboxes together to get a realistic chatbot system:

- `streamlit` for the interface,
- `strands` for the agentic aspects,
- `mlflow` for the trace and evaluation,
- `ollama` as default local LLM backend,
- `nginx` to add basic authentication and url remapping, 
- `podman-compose` to orchestrate the services.

## Development mode

No need to start everything when developing, just run ollama and the app in a terminal:

```bash
podman run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama-gpu docker.io/ollama/ollama:latest
podman exec -it ollama-gpu ollama pull tinyllama:latest
MODEL_ID="tinyllama:latest" pixi run chatbot
podman stop ollama-gpu
```

Optionally, in *another* terminal run mlflow server to check saved traces:

```bash
pixi run mlflow server
```

## Deployment mode

TODO setup docker-compose to run all services

```bash
podman compose up
```
