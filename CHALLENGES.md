# Challenge Log

All challenges encountered during this development journey, both pending and accomplished, will be logged here for future reference.

## Pending Issues

[ ] Improve LLM reasoning capabilities
- Currently, it gets the right answer _with the wrong formula_. 
- It was able to get 3 'r's in strawberry but both its spelling (S T R A W B R E E R) and letter positioning during a follow-up prompt (second, sixth, and eighth letters) were incorrect.

## Challenges Navigated

1. **Challenge:** Core dependencies of vLLM are Linux-oriented, which caused issues since local system runs on Windows. 
   - **Solution:** Dockerize the system with a supportive environment, used PyTorch's docker image (pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel)
2. **Challenge:** Default LLM engine parameters of vLLM used in the configurations for loading the model, primarily `max_model_length`, far exceeded the 6GB VRAM capacity of local GPU. 
   - **Solution:** Configured multiple reduced parameters to bring model to executable status. 
   - **Future:** Additional research will be required to optimize for better results.
3. **Challenge:** From current observations, vLLM could only work with models downloaded to `${HOME}/.cache/huggingface/<model-name>` using `huggingface_hub` module or `huggingface-cli`.
   - **Solution:** `huggingface-cli` is currently used to fetch model during Docker build, which increases build time in initial build. Later builds have cached layers, thus reducing the need for re-downloads. 
   - HF tokens are not required for access as model is public.
   - **Future:** Optimizations will need to be looked into to improve initial build time.
4. **Challenge:** Model was initially giving the same reptitive outputs for different prompts. 
   - **Cause:** Occurred due to incorrect formatting of conversation data (added an extra list encapsulation before appending message to conversation context).
   - **Solution:**  Correcting the conversation message format resolved this problem.
5. **Challenge:** Docker image was reaching large sizes (~23GB).
   - **Cause:** Inspection of build commands showed number of commands with large memory contributions in the PyTorch image used as base.
      - Most are required dependencies (CUDA, CUDNN and drivers), but PyTorch base image also copies a conda directory, which contributed ~5.5GB but may not be relevant to our usecase.
   - **Solution:** Shifted base image to NVIDIA's CUDA 12.1.1 development image ([12.1.1-cudnn8-devel-ubuntu22.04](https://hub.docker.com/layers/nvidia/cuda/12.1.1-cudnn8-devel-ubuntu22.04/images/sha256-cc55d151af1e8e083f3210af753a5cfbcbc5455421531eb0459887026bb4699f)), then to its runtime version to reduce image size further ([12.1.1-cudnn8-runtime-ubuntu22.04](https://hub.docker.com/layers/nvidia/cuda/12.1.1-cudnn8-runtime-ubuntu22.04/images/sha256-810756cab1c28ce693499a5c2ebb66f6d10a61d026998c8606bad449643a4c49)). 
        - Current image reaches ~14GB, which while large still provides a ~39% decrease in size.
    - **Future:** Look into additional optimization techniques for smaller Docker images in this specific usecase.
6. **Challenge:** The LLM was providing very short, cut-off responses.
    - **Cause:** vLLM's inference engine has a `max_tokens` parameter that determines the number of output tokens to be considered from the model, and was set to `16` by default, which was responsible for the weird, short responses. Identified thanks to [this comment](https://github.com/vllm-project/vllm/issues/655#issuecomment-1679294790) on an issue reported on vLLM's Github page.
    - **Solution:** Added the `max_tokens` parameter to the `SamplingParams` object passed to the LLM engine with the value set to `2048`, which now allows the server to provide fully-fledged answers.
