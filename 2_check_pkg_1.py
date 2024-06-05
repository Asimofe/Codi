import subprocess
import re

def check_installed_packages():
    """설치된 패키지 목록을 출력, 특정 패키지들의 버전 확인"""
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    installed_packages = result.stdout

    # 설치된 패키지와 버전을 딕셔너리로 파싱
    packages_dict = {}
    lines = installed_packages.split('\n')
    for line in lines[2:]:  # 첫 두 줄은 헤더이므로 무시
        parts = line.split()
        if len(parts) >= 2:
            packages_dict[parts[0]] = parts[1]

    # 특정 패키지들의 설치 및 버전 확인
    required_packages = {
        "accelerate": "0.29.1",
        "datasets": "2.16.1",
        "bitsandbytes": "0.41.3",
        "peft": "0.8.2",
        "trl": "0.8.1",
        "wandb": "0.16.3",
        "huggingface-hub": "0.20.3"
    }

    print("특정 패키지 설치 및 버전 확인:")
    for package, required_version in required_packages.items():
        if package in packages_dict:
            installed_version = packages_dict[package]
            print(f"{package} 설치됨, 설치된 버전: {installed_version} (요구 버전: {required_version})")
        else:
            print(f"{package} 설치되지 않음")

check_installed_packages()

