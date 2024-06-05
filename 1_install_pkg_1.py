import subprocess
import os

def install_requirements():
    """requirements.txt 파일에서 패키지를 설치"""
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True, text=True)
        print("Requirements 설치가 성공적으로 완료되었습니다.")
    except subprocess.CalledProcessError as e:
        print("Requirements 설치 중 오류 발생:", e)

def set_environment_variable():
    """환경 변수 HF_TOKEN을 사용자 입력을 통해 설정"""
    print("export your HF token, found here: https://huggingface.co/settings/account")
    token = input("Please enter your HF_TOKEN: ")
    os.environ['HF_TOKEN'] = token
    print("환경 변수 HF_TOKEN이 설정되었습니다.")

# 사용 예시
install_requirements()
set_environment_variable()

