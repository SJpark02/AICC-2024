from pydub import AudioSegment
import os

def split_wav(source_directory, target_directory, split_length=540000):  # split_length는 밀리초 단위
    # 저장할 경로가 존재하지 않으면 생성
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    for filename in os.listdir(source_directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(source_directory, filename)
            audio = AudioSegment.from_wav(file_path)
            total_length = len(audio)
            parts = total_length // split_length + (1 if total_length % split_length > 0 else 0)

            for i in range(parts):
                start = i * split_length
                end = start + split_length
                split_audio = audio[start:end]
                split_filename = f"{filename.rsplit('.', 1)[0]}_part{i+1}.wav"  # 파일명만 사용
                split_file_path = os.path.join(target_directory, split_filename)  # 저장할 전체 경로
                split_audio.export(split_file_path, format="wav")
                print(f"Saved: {split_file_path}")

# 원본 파일이 있는 폴더 경로
source_directory_path = ""

# 분할된 파일을 저장할 폴더 경로
target_directory_path = ""

# 함수 호출
split_wav(source_directory_path, target_directory_path)
