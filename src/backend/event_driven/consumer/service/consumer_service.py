import json 
import time
import boto3
from botocore.exceptions import ClientError
from src.backend.clients.amazon_transcribe_client import TranscribeClient
from src.backend.clients.openai_client import GPT4ChatClient
from src.backend.event_driven.consumer.repository.dynamo import DynamoDBUpdateStatusClient

class ConsumerService:
    def __init__(self):
        self.transcribe = TranscribeClient()
        self.gpt = GPT4ChatClient() 
        self.dynamo = DynamoDBUpdateStatusClient()
        self.sqs = boto3.client("sqs")
    
    def consumer(self, bucket: str, object: str, receipt_handle: str, eventSourceARN: str):
        split_media_format = self.formatMedia(object)
        self.transcribe.start_job(job_name=object, media_uri=f'https://{bucket}.s3.us-east-1.amazonaws.com/{object}', media_format=split_media_format, language_code='pt-BR')
        while True:
            status = self.transcribe.check_job_status(object)
            if status == "COMPLETED":
                transcript = self.transcribe.get_transcription_result(object)
                generate_response = self.gpt.generate_content(transcript)
                self.dynamo.update_requested_data(object, generate_response)
                self.delete_SQS_queue_message(receipt_handle, eventSourceARN)
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
  
    
    def delete_SQS_queue_message(self, receipt_handle: str, eventSourceARN: str):
        try:
            q_region, q_acct_id, q_name = eventSourceARN.split(':')[3:6]
            q_url = f'https://{q_region}.queue.amazonaws.com/{q_acct_id}/{q_name}'
            
            response = self.sqs.delete_message(QueueUrl=q_url, ReceiptHandle=receipt_handle)
            
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("Mensagem deletada com sucesso.")
            else:
                print("Falha ao deletar a mensagem.")
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Erro ao deletar mensagem da fila SQS: {error_code} - {error_message}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {str(e)}")
     
