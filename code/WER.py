import os
import re
from difflib import SequenceMatcher

def preprocess_text(text):
    # 텍스트를 소문자로 변환하고 특수문자를 공백으로 치환
    text = re.sub(r'\W', ' ', text.lower())
    # 연속된 공백을 하나의 공백으로 치환
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_wer(reference, hypothesis):
    # 참조 텍스트와 가설 텍스트를 단어 단위로 분할
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    sm = SequenceMatcher(None, ref_words, hyp_words)
    
    # 삭제, 삽입, 대체가 필요한 단어 수 계산
    deletions = insertions = substitutions = 0
    for opcode, a0, a1, b0, b1 in sm.get_opcodes():
        if opcode == 'replace':
            substitutions += max(a1 - a0, b1 - b0)
        elif opcode == 'insert':
            insertions += b1 - b0
        elif opcode == 'delete':
            deletions += a1 - a0
    
    # 참조 텍스트의 단어 수
    N = len(ref_words)
    if N == 0:
        return float('inf')  # 참조 텍스트가 비어 있으면 무한대 반환
    # WER 계산
    WER = (substitutions + deletions + insertions) / N
    return WER

def load_text_from_file(file_path):
    # 파일을 열어 내용을 읽어 텍스트를 추출
    try:
        content = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if file_path.endswith('.vtt') and not line.strip().startswith(('NOTE', 'WEBVTT', 'STYLE', '00:')):
                    content.append(line.strip())
                elif file_path.endswith('.txt'):
                    content.append(line.strip())
        text = ' '.join(content).strip()
        if text == "":
            print(f"경고: {file_path} 파일이 비어 있습니다.")
        return text
    except Exception as e:
        print(f"파일 읽기 오류 {file_path}: {e}")
        return None

def compute_wer_for_folders(folder_path_original, folder_path_merge, output_file):
    results = {}
    original_files = {f[:-4]: os.path.join(folder_path_original, f) for f in os.listdir(folder_path_original) if f.endswith('.vtt')}
    merge_files = {f[:-4]: os.path.join(folder_path_merge, f) for f in os.listdir(folder_path_merge) if f.endswith('.txt')}

    common_files = set(original_files).intersection(set(merge_files))
    if not common_files:
        print("지정된 폴더에 공통 파일이 없습니다.")
        return None

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Filename,WER\n")
        for base_filename in common_files:
            original_text = load_text_from_file(original_files[base_filename])
            merge_text = load_text_from_file(merge_files[base_filename])
            
            if original_text is None or merge_text is None or original_text == "" or merge_text == "":
                continue  # 파일이 비어 있거나 오류가 있는 경우 계산 제외
            
            original_text = preprocess_text(original_text)
            merge_text = preprocess_text(merge_text)
            
            wer = calculate_wer(original_text, merge_text)
            results[base_filename] = wer
            f.write(f"{base_filename},{wer:.2f}\n")

    return output_file

# 경로 설정
folder_path_original = 'original folder path'
folder_path_merge = 'merge folder path'
output_file_path = 'save folder'

# 결과 계산 및 출력 파일 저장
compute_wer_for_folders(folder_path_original, folder_path_merge, output_file_path)
print(f"결과가 저장된 파일: {output_file_path}")
