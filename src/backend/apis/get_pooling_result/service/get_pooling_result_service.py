import boto3
from botocore.exceptions import ClientError
from src.backend.clients.secrets_manager_client import SecretsManagerClient


class GetPoolingResultService:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.secretsmanager = SecretsManagerClient()

    def get_result_by_id(self, id: str):
        try:
            initiate_SM_client = self.secretsmanager.initiate_secrets_manager()
            dynamo_database = initiate_SM_client.get("DYNAMO-DB-TABLE")
            response = self.dynamodb.get_item(
                TableName=dynamo_database, Key={"id": {"S": id}}
            )
            item = response.get("Item", {})
            if item:
                return {k: v.get("S") for k, v in item.items()}
            else:
                return {}

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return f"Erro ao buscar o item do DynamoDB: {error_code} - {error_message}"
        except Exception as e:
            return f"Ocorreu um erro inesperado: {str(e)}"

