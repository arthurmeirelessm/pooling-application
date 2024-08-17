from src.backend.apis.create_status.repository.dynamo import DynamoDBCreateStatusClient
import json 

class CreateStatusService:
    def __init__(self):
        self.dynamodbClient = DynamoDBCreateStatusClient()

    def create_status(self, id):
        send_to_dynamo = self.dynamodbClient.save_requested_data(id)
        return send_to_dynamo
        
