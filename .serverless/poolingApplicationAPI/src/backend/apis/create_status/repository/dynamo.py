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
        self.table = os.getenv(("DYNAMO_DB_TABLE"))

    def save_requested_data(
        self, id: int
    ) -> Any:
        print(id)
        try:
            item = {
                "id": {"S": id},
                "status": {"S":"pending"},
                "result": {"S": ""},
            }

            put_requested = self.dynamodb.put_item(TableName=self.table, Item=item)
            return put_requested
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
        