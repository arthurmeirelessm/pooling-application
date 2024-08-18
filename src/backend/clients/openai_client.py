import openai
from dotenv import load_dotenv
import os

class GPT4ChatClient:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = api_key
    
    def generate_content(gpt_assistant_prompt: str, gpt_user_prompt: str) -> dict:
        gpt_prompt = f"{gpt_assistant_prompt} {gpt_user_prompt}"
        messages = [
        {"role": "assistant", "content": gpt_assistant_prompt},
        {"role": "user", "content": gpt_user_prompt}
    ]
        response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
        max_tokens=256,
        frequency_penalty=0.0
    )
        response_text = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        return {"response": response_text, "tokens_used": tokens_used}


