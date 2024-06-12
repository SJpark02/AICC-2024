from pydub import AudioSegment

# MP3 파일 로드
audio = AudioSegment.from_file("")

# 샘플링 주파수 출력
print("Sampling Frequency:", audio.frame_rate, "Hz")

#결과: Sampling Frequency: 48000 Hz