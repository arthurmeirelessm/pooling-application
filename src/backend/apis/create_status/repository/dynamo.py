import boto3
import os
import uuid
import json
import datetime
from decimal import Decimal
from typing import Dict, Any
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class DynamoDBCreateStatusClient:
    load_dotenv()

    def __init__(self):
        self.dynamodb = boto3.client("dynamodb")
        self.secretsmanager = self.initiate_secrets_manager()

    def save_requested_data(
        self, id: int
    ) -> Any:
        try:
            item = {
                "id": {"S": id},
                "status": {"S":"pending"},
                "result": {"S": ""},
            }

            put_requested = self.dynamodb.put_item(TableName=self.secretsmanager, Item=item)
            return put_requested
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
        
    
    def initiate_secrets_manager(
        self
    ) -> Any:
        secretsmanager = boto3.client("secretsmanager")
        get_secret_value_response = secretsmanager.get_secret_value(SecretId="pooling-application-secrets")
        secret = json.loads(get_secret_value_response['SecretString'])
        dynamo_database = secret.get("DYNAMO-DB-TABLE") 
        return dynamo_database