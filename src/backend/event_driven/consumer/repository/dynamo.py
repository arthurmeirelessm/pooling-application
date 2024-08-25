from botocore.exceptions import ClientError
from dotenv import load_dotenv
from typing import Dict, Any
from src.backend.clients.secrets_manager_client import SecretsManagerClient
import boto3
import os
import json



class DynamoDBUpdateStatusClient:
    load_dotenv()

    def __init__(self):
        self.dynamodb = boto3.client("dynamodb")
        self.secretsmanager = SecretsManagerClient()

    def update_requested_data(
        self, id: int, result: str
    ) -> Any:
        try:
            key = {
                "id": {"S": str(id)} 
            }
            
            update_expression = "SET #status = :status, #result = :result"
            expression_attribute_names = {
                "#status": "status",
                "#result": "result"
            }
            expression_attribute_values = {
                ":status": {"S": "completed"},
                ":result": {"S": result}
            }

            initiate_SM_client = self.secretsmanager.initiate_secrets_manager()
            dynamo_database = initiate_SM_client.get("DYNAMO-DB-TABLE")
            
            update_response = self.dynamodb.update_item(
                TableName=dynamo_database,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW" 
            )
            
            print("Update Response:", update_response)
            return update_response
        except ClientError as e:
            print(f"Ocorreu um erro ao acessar o DynamoDB: {e.response['Error']['Message']}")
