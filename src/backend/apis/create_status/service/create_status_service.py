from src.backend.apis.create_status.repository.dynamo import DynamoDBClient
import json 

class CreateStatusService:
    def __init__(self):
        self.dynamodbClient = DynamoDBClient()

    def my_method(self, id):
        send_to_dynamo = self.dynamodbClient.save_requested_data(id)
        return send_to_dynamo
        
