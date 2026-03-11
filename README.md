# Mini-Chatbot

This repository is a tiny experiment where I put together few toolboxes together to get a realistic chatbot system:

- `streamlit` for the interface,
- `strands` for the agentic aspects,
- `mlflow` for the trace and evaluation,
- `ollama` as default local LLM backend,
- `nginx` to add basic authentication and url remapping, 
- `podman-compose` to orchestrate the services.

## Development mode

No need to start everything when developing, just run ollama and the app:

- in a first terminal, run the ollama server:

```bash
pixi run ollama serve
```

- in *another* terminal, start the app

```bash
export MODEL_ID="phi3:mini-4k"
pixi run chatbot
```

- (optional), in *another* terminal run mlflow server to check saved traces:

```bash
pixi run mlflow server
```

## Deployment mode

TODO setup docker-compose to run all services

```bash
podman compose up -d
```
