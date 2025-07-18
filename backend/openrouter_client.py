import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("OPENROUTER_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "JobCopilot"
    },
    http_client=httpx.Client(verify=False)
)

def ask_model(prompt: str, model="mistralai/mistral-7b-instruct") -> str:
    response = client.chat.completions.create(
        model = model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content