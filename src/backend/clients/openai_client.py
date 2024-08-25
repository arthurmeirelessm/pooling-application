from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv
from src.backend.clients.secrets_manager_client import SecretsManagerClient
import os


class GPT4ChatClient:
    def __init__(self):
        self.secrets = SecretsManagerClient()
        self.initiate_secrets = self.secrets.initiate_secrets_manager()
        api_key = self.initiate_secrets.get("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=api_key
        )
        
    def generate_content(self, content_trancribed: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                {
                    "role": "system", "content": "Crie 10 perguntas com suas respectivas respostas usando como base o conteúdo do user"
                },
                {
                    "role": "user", "content": content_trancribed
                }
                ],
                model="gpt-3.5-turbo",
                )
            content = chat_completion.choices[0].message.content
            return content    
        
        except KeyError as e:
            print(f"KeyError: {e}")
            return {"error": "Invalid response format"}
    
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred"}
