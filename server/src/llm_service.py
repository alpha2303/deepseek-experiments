from typing import Dict, List
from vllm import LLM, RequestOutput, SamplingParams


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

    @classmethod
    def from_config(
        cls,
        config_dict: Dict[str, Dict[str, str | float | int]],
        model_key: str,
    ):
        try:
            model_config = config_dict["models"][model_key]
            llm_engine = LLM(
                model=model_config["repo_name"],
                gpu_memory_utilization=model_config["gpu_memory_utilization"],
                enforce_eager=True,
                max_model_len=model_config["max_model_len"],
            )
            samplingParams = SamplingParams(
                temperature=model_config["sampling_params"]["temperature"],
                top_p=model_config["sampling_params"]["top_p"],
                max_tokens=model_config["sampling_params"]["max_tokens"],
            )

            return cls(llm_engine, samplingParams)
        except Exception as e:
            raise e

    def generate_text(self, prompt) -> str:
        outputs = self.llm_engine.generate(prompt, self.params)
        return outputs[0].outputs[0].text

    def generate_chat_response(self, prompt) -> str:
        self.conversation.append({"role": "user", "content": prompt})
        outputs = self.llm_engine.chat(self.conversation, self.params, use_tqdm=False)

        chat_output = self._extract_output(outputs)
        self.conversation.append({"role": "assistant", "content": chat_output})

        return chat_output

    def chat_history(self) -> List[dict[str, str]]:
        return self.conversation

    def _extract_output(outputs: List[RequestOutput]) -> str:
        return outputs[0].outputs[0].text
