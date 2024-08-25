from src.backend.event_driven.consumer.service.consumer_service import ConsumerService
import json 

class ConsumerController:
    def __init__(self):
        self.service = ConsumerService()
    
    def handle_request(self, event):
        print(event)
        for i in event['Records']:
            receipt_handle = i['receiptHandle']
            eventSourceARN = i['eventSourceARN']
            s3_event = json.loads(i['body'])
            for j in s3_event['Records']:
                bucket = j['s3']['bucket']['name']
                object = j['s3']['object']['key']
                print("Bucket Name: {}".format(j['s3']['bucket']['name']))
                print("Object Name: {}".format(j['s3']['object']['key']))
        send_service = self.service.consumer(bucket, object, receipt_handle, eventSourceARN)
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
                )
            }        
            
            
            

