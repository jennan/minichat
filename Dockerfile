FROM ghcr.io/prefix-dev/pixi:0.65.0 AS build
COPY . .
RUN pixi install --locked
CMD [ "pixi", "run", "chatbot" ]
