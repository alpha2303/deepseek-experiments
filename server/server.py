import gc
import json
from typing import List
import torch
from vllm import LLM, RequestOutput, SamplingParams
from fastapi import FastAPI
from pydantic import BaseModel

HF_DEEPSEEK_REPONAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"


class LLMService:
    llm_engine: LLM = None
    params: SamplingParams = None
    conversation = []

    def __init__(
        self,
        llm_engine: LLM = LLM(
            model=HF_DEEPSEEK_REPONAME,
            trust_remote_code=True,
            gpu_memory_utilization=0.96,
            enforce_eager=True,
            max_model_len=8196,
        ),
        params: SamplingParams = SamplingParams(
            temperature=0.5, top_p=0.95, max_tokens=2048
        ),
    ) -> None:
        self.llm_engine = llm_engine
        self.params = params

    def generate_text(self, prompt) -> str:
        outputs = self.llm_engine.generate(prompt, self.params)
        return outputs[0].outputs[0].text

    def generate_chat_response(self, prompt) -> str:
        self.conversation.append({"role": "user", "content": prompt})
        outputs = self.llm_engine.chat(self.conversation, self.params, use_tqdm=False)

        chat_output = extract_output(outputs)
        self.conversation.append({"role": "assistant", "content": chat_output})

        return chat_output

    def chat_history(self) -> List[dict[str, str]]:
        return self.conversation


llm: LLMService = None
try:
    llm = LLMService()
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


@app.get("/history", response_model=List[dict[str, str]])
async def llm_history():
    return llm.chat_history()


def extract_output(outputs: List[RequestOutput]) -> str:
    return outputs[0].outputs[0].text
