import subprocess

Link_text_file_path = "your path"

# 다운로드할 비디오 URL 리스트
with open(Link_text_file_path, 'r') as file:
    video_urls = [line.strip() for line in file.readlines() if line.strip()]

output_url = "D:\\Data\\AICC_data\\%(title)s.%(ext)s"
for url in video_urls:
    # yt-dlp를 사용하여 비디오(mp4)와 자막(srt) 다운로드
    # --embed-subs 옵션은 자막을 비디오 파일에 내장하지만, 별도의 srt 파일도 저장합니다.
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--write-sub",
        "--sub-format", "vtt",
        "--embed-subs",
        "--output", output_url,
        "--ffmpeg-location", "D:\\Tools\\ffmpeg\\bin\\ffmpeg.exe",  # 이 부분을 추가

        url
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")

