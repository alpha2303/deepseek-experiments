import json
import requests


def send_message(prompt: str):
    res: requests.Response = requests.post(
        "http://localhost:3000/chat/",
        headers={"Content-Type": "application/json", "accept": "application/json"},
        data=json.dumps({"prompt": prompt}),
    )
    res_msg: str = ""
    try:
        res_msg = res.json()["message"]
    except Exception as e:
        res_msg = str(e)
    return res_msg


def start_client() -> None:
    prompt: str = input("Enter Prompt: ").strip()
    while len(prompt) > 0 and not prompt.lower().startswith("bye"):
        response_text: str = send_message(prompt)
        print(f"Deepseek: {response_text}")
        prompt: str = input("Enter Prompt: ").strip()


if __name__ == "__main__":
    print("""
** DeepSeek Communicator **

Welcome to DeepSeek Communicator!
Model: DeepSeek-R1-Distill-Qwen-1.5B
          
""")
    start_client()
