# DeepSeek Experiments

Experimentations on building LLM systems, leveraging DeepSeek AI's DeepSeek-R1 series of models.

**LLM Model:** [DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)

**LLM Inference Interface:** [vLLM](https://docs.vllm.ai/en/latest/)

**API Server:** [FastAPI](https://fastapi.tiangolo.com/)

Current logic functions out of two programs: `server.py` and `client.py`

## Package setup

1. This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/#pypi) for Python package management. Ensure uv is installed on your system.

2. Use `uv sync` to sync dependency installation based on `uv.lock` file.

## Setting up the LLM Server using Docker

1. Ensure Docker is installed on your system
2. Start a terminal in the root folder of the repository and run the following command to build the Docker image:

```
docker build -t alpha2303/deepseek-experiments:latest .
```

3. Once the Docker image is built, run it in a container using the following command:

```
docker run --gpus=all -p 3000:3000 -t alpha2303/deepseek-experiments:latest
```

This will start the LLM server with port forwarding at Port 3000, which can be accessed from the local system through the URL `http://localhost:3000`.

## Starting the Client

1. Ensure that all dependencies are installed without issues.
2. Once the server is up and running, open a terminal in the root folder and run `uv run ./client/client.py` to start the chat client.
3. To stop the chat client, enter `bye` into the `Enter Prompt:` input prompt .

## Challenge Log
All challenges encountered during this development journey, both pending and accomplished, will be logged in the [Challenge Log](./CHALLENGES.md) for future reference.