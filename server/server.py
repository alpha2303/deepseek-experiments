import gc
import json
from pathlib import Path
from typing import Dict, List

import torch
from fastapi import FastAPI
from pydantic import BaseModel

from .src import LLMService
from .src.helpers import load_config

DEFAULT_MODEL_KEY = "DeepSeek-R1-Distill-Qwen-1.5B"

llm: LLMService = None
try:
    config = load_config(Path("./model_configs.json").resolve())
    llm = LLMService.from_config(config_dict=config, model_key=DEFAULT_MODEL_KEY)
except torch.OutOfMemoryError as e:
    print(e)
    print(torch.cuda.memory_summary())
finally:
    torch.cuda.empty_cache()
    gc.collect()


app = FastAPI()


class PromptQuery(BaseModel):
    prompt: str


@app.post("/", response_model=dict)
async def llm_generate_text(prompt_query: PromptQuery):
    prompt = prompt_query.prompt.strip()
    return {"message": llm.generate_text(prompt=prompt)}


@app.post("/chat", response_model=dict)
async def llm_generate_chat(prompt_query: PromptQuery):
    prompt = prompt_query.prompt.strip()
    message = ""
    if prompt == "history":
        message = json.dumps(llm.chat_history())
    else:
        message = llm.generate_chat_response(prompt=prompt)
    return {"message": message}


@app.get("/history", response_model=List[Dict[str, str]])
async def llm_history():
    return llm.chat_history()
