import requests
import json


class Model:
    """
    Call LLM api to generate assertions

    Attributes:
        based_url (str): The basic url of LLM server
        relative_url (str): The relative url of LLM server
        model (str): The name of model
        message (str): The input user message
        temperature (float): The input temperature of the LLM
        headers (Dict): Headers of the request

    Methods:
        call_llm_api(): Call LLM sever API
    """
    def __init__(self, based_url, relative_url, model, message, temperature=0.2):
        self.based_url = based_url
        self.relative_url = relative_url
        self.model = model
        self.message = message
        self.temperature = temperature
        self.headers = {"Content-Type": "application/json"}

    def call_llm_api(self):
        print("Calling LLM API...")
        url = f"{self.based_url}/{self.relative_url}"
        
        # 调整为chat completions格式
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": self.message}],  # 调整消息格式
            "temperature": self.temperature
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # 打印更详细的错误信息
            print(f"Request Error: {e}")
            if response.content:
                print(f"Response content: {response.content.decode('utf-8')}")
            return None

