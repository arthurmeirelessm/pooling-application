import json 
from src.backend.apis.create_status.service.create_status_service import CreateStatusService

class CreateStatusController:
    def __init__(self):
        self.service = CreateStatusService()

    def handle_request(self, event):
        body_json = json.loads(event.get("body"))
        id = body_json.get("id")
        send_service = self.service.create_status(id)
        return {
                "statusCode": 200,
                 "headers": {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                    },
                "body": json.dumps(
                    {
                        "message": "criado no dynamo!",
                    }
                ),
            }
