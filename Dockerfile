FROM ghcr.io/prefix-dev/pixi:0.65.0
COPY pixi.toml pixi.lock app.py .
RUN pixi install --locked
CMD [ "pixi", "run", "chatbot" ]
