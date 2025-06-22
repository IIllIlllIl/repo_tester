import requests
import json
from openai import OpenAI


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
        openai_api(): Call openai API
        call_llm_api(): Abandoned method
    """
    def __init__(self, based_url, model, message, key, temperature=0.0, relative_url=None,):
        self.based_url = based_url
        self.relative_url = relative_url
        self.model = model
        self.message = message
        self.temperature = temperature
        self.headers = {"Content-Type": "application/json"}
        self.key = key

    def openai_api(self):
        client = OpenAI(api_key=self.key, base_url=self.based_url)

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional Python developer."},
                {"role": "user", "content": f"{self.message}"},
            ],
            stream=False
        )

        return response.choices[0].message.content

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

