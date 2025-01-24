FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Env Setup
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt update && apt install python3.10 python3-pip -y

WORKDIR /app
RUN pip install uv
RUN uv venv .venv --seed
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install huggingface_hub
RUN huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B config.json model.safetensors
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen
COPY /server .
CMD ["fastapi", "run", "server.py", "--port", "3000", "--host", "0.0.0.0"]