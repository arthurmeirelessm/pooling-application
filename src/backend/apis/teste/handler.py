from typing import Dict, Any
from src.backend.clients.openai_client import GPT4ChatClient
import json
import re


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    controller = GPT4ChatClient()
    response = controller.generate_content()
    return {
                "statusCode": 200,
                 "headers": {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                    },
                "body": json.dumps(
                    {
                        "message": response,
                    }
                )
            }        
