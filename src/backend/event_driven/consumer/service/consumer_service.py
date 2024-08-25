import json 
import time
from src.backend.clients.amazon_transcribe_client import TranscribeClient
from src.backend.clients.openai_client import GPT4ChatClient
from src.backend.event_driven.consumer.repository.dynamo import DynamoDBUpdateStatusClient

class ConsumerService:
    def __init__(self):
        self.transcribe = TranscribeClient()
        self.gpt = GPT4ChatClient() 
        self.dynamo = DynamoDBUpdateStatusClient()
    
    def consumer(self, bucket: str, object: str):
        split_media_format = self.formatMedia(object)
        self.transcribe.start_job(job_name=object, media_uri=f'https://{bucket}.s3.us-east-1.amazonaws.com/{object}', media_format=split_media_format, language_code='pt-BR')
        while True:
            status = self.transcribe.check_job_status(object)
            if status == "COMPLETED":
                print("Transcription job completed.")
                transcript = self.transcribe.get_transcription_result(object)
                print("Transcription Result:", transcript)
                generate_response = self.gpt.generate_content(transcript)
                self.dynamo.update_requested_data(object, generate_response)
                return generate_response
            elif status == "FAILED":
                print("Transcription job failed.")
                break
            else:
                print("Transcription job is in progress. Checking again in 30 seconds...")
                time.sleep(30)    
    
    def formatMedia(self, object = str):
      split = object.split(".")[1]
      return split
  
     
