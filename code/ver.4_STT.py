import boto3
import os
import time
import requests
import re
# AWS 설정
ACCESS_KEY = ''
SECRET_KEY = ''
REGION = ''  # 예: 'us-east-1'
BUCKET_NAME = ''

# 폴더 경로 설정
local_folder_path = 'segment_cencellation_path'
output_folder_path = 'stt_txt_files_path'
# S3와 Transcribe 클라이언트 생성
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
transcribe_client = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

def sanitize_filename(filename):
    """Sanitize filenames to conform to AWS requirements."""
    return re.sub(r'[^0-9a-zA-Z._-]', '_', filename)

def upload_files_to_s3(local_folder_path, bucket_name):
    for file_name in os.listdir(local_folder_path):
        if file_name.endswith('.mp3'):
            sanitized_file_name = sanitize_filename(file_name)
            local_path = os.path.join(local_folder_path, file_name)
            s3_key = f"input_audio/{sanitized_file_name}"
            s3_client.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded {sanitized_file_name} to S3 bucket {bucket_name} in folder input_audio")
    
def transcribe_files_from_s3(bucket_name, output_folder_path):
    counter = 0
    start_time = 0
    acc_time = 0    # sst 처리 시간 누적 변수
    result_time = 0
    for file_name in os.listdir(local_folder_path):
        counter  += 1
        if file_name.endswith('.mp3'):
            sanitized_file_name = sanitize_filename(file_name)
            job_name = f"{sanitized_file_name}-{int(time.time())}"
            s3_key = f"input_audio/{sanitized_file_name}"
            job_uri = f"s3://{bucket_name}/{s3_key}"
            transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat='mp3',
                LanguageCode='en-US'
            )
            print(f"Started transcription job for {sanitized_file_name}")
            start_time = time.time()
            while True:
                status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(5)
            acc_time += time.time() - start_time
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                transcription_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                result = requests.get(transcription_url).json()
                transcript_text = result['results']['transcripts'][0]['transcript']
                output_file_name = os.path.splitext(sanitized_file_name)[0] + '.txt'
                output_path = os.path.join(output_folder_path, output_file_name)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(transcript_text)
                print(f"Saved transcript to {output_path}")
    result = round(acc_time/counter, 2)
    print("ASR mp3 length: 10 minutes")
    print("number of working files", 5)
    print("avarage time: ", result)
    

# 파일 업로드
upload_files_to_s3(local_folder_path, BUCKET_NAME)

# Transcription 시작

transcribe_files_from_s3(BUCKET_NAME, output_folder_path)