import json 
from src.backend.apis.get_pooling_result.service.get_pooling_result_service import GetPoolingResultService

class GetPoolingResultController:
    def __init__(self):
        self.service = GetPoolingResultService()

    def handle_request(self, event):
        print(event)
        query_params = event.get('queryStringParameters', {})
        id = list(query_params.keys())[0] if query_params else None
        send_service = self.service.get_result_by_id(id)
        return {
                "statusCode": 200,
                 "headers": {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                    },
                "body": json.dumps(
                    {
                        "message": send_service,
                    }
                ),
            }
