import boto3
import requests

class TranscribeClient:
    def __init__(self):
        self.transcribe_client = boto3.client("transcribe")

    def start_job(self, job_name, media_uri, media_format, language_code):
        try:
            job_args = {
                "TranscriptionJobName": job_name,
                "Media": {"MediaFileUri": media_uri},
                "MediaFormat": media_format,
                "LanguageCode": language_code,
            }
            
            response = self.transcribe_client.start_transcription_job(**job_args)
            print(f"Started transcription job {job_name}.")
            return response
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
    
    def check_job_status(self, job_name):
        try:
            response = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            return status
        except Exception as e:
            print(f"An unexpected error occurred while checking job status: {e}")
            return None
    
    
    def get_transcription_result(self, job_name):
        try:
            response = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            
            if status == "COMPLETED":
                transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
                transcript_response = requests.get(transcript_uri)
                transcript_data = transcript_response.json()
                return transcript_data["results"]["transcripts"][0]["transcript"]
            elif status == "FAILED":
                print(f"Transcription job {job_name} failed.")
                return None
            else:
                print(f"Transcription job {job_name} is still in progress.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting the transcription result: {e}")
            return None
