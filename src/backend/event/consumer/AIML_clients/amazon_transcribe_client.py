import boto3

class TranscribeClient:
        def __init__(self):
            self.client = boto3.client("transcribe")

        def start_job(self, job_name: str, media_format: str, file_name: str):
            self.client.start_transcription_job(
                TranscriptionJobName=job_name,
                LanguageCode="en-IN",
                MediaFormat=media_format,
                Media={
                    "MediaFileUri": f"s3://lejdiprifti-stt-inputs/{file_name}.{media_format}",
                },
                OutputBucketName="lejdiprifti-stt-outputs",
                OutputKey=f"{file_name.replace(' ', '_')}.json",
            )