import boto3
import os
import uuid
import json
import datetime
from decimal import Decimal
from typing import Dict, Any
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from src.backend.clients.secrets_manager_client import SecretsManagerClient


class DynamoDBCreateStatusClient:
    load_dotenv()

    def __init__(self):
        self.dynamodb = boto3.client("dynamodb")
        self.secretsmanager = SecretsManagerClient()

    def save_requested_data(
        self, id: int
    ) -> Any:
        try:
            item = {
                "id": {"S": id},
                "status": {"S":"pending"},
                "result": {"S": ""},
            }
            initiate_SM_client = self.secretsmanager.initiate_secrets_manager()
            print(initiate_SM_client)
            dynamo_database = initiate_SM_client.get("DYNAMO-DB-TABLE")
            put_requested = self.dynamodb.put_item(TableName=dynamo_database, Item=item)
            print(put_requested)
            return put_requested
        except ClientError as e:
            print(f"Ocorreu um erro ao acessar o DynamoDB: {e.response['Error']['Message']}")

        
