FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel

WORKDIR /app
RUN pip install uv
RUN uv venv .venv --seed
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install huggingface_hub
RUN huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B config.json model.safetensors
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen
COPY server.py .
CMD ["fastapi", "run", "server.py", "--port", "3000", "--host", "0.0.0.0"]