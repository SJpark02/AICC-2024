import os
import re

def clean_vtt_content(content):
    """ HTML 같은 태그와 다른 비텍스트 요소를 제거하여 VTT 콘텐츠를 정리합니다 """
    # HTML 같은 태그 제거
    content = re.sub(r'<[^>]+>', '', content)
    # ">>>"와 같은 특수 문자 제거
    content = re.sub(r'&gt;+', '', content)
    # 기타 원치 않는 문자나 시퀀스 제거
    content = re.sub(r'&[^;]+;', '', content)
    # 공백 정규화
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def process_text_files(source_folder, output_folder):
    """ 소스 폴더 내의 모든 텍스트 파일을 처리하고 결과를 다른 폴더에 저장합니다 """
    os.makedirs(output_folder, exist_ok=True)  # 출력 폴더가 존재하지 않으면 생성
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(source_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                cleaned_text = clean_vtt_content(content)
                
                # 정리된 내용을 저장
                output_file_path = os.path.join(output_folder, file_name)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_text)
                print(f"처리된 파일 {file_path} 를 {output_file_path}로 저장했습니다.")

# 사용자 입력을 통해 소스 및 출력 폴더 경로 설정
source_folder = input("텍스트 파일이 있는 소스 폴더 경로를 입력하세요: ")
output_folder = input("정리된 텍스트 파일을 저장할 출력 폴더 경로를 입력하세요: ")

# 파일 처리
process_text_files(source_folder, output_folder)
