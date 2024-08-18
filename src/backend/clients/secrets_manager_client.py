import boto3
import json
import types

class SecretsManagerClient:
    def __init__(self):
        self.secretsmanager = boto3.client("secretsmanager")
    
    def initiate_secrets_manager(
        self
    ) -> str:
        get_secret_value_response = self.secretsmanager.get_secret_value(SecretId="pooling-application-secrets")
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret