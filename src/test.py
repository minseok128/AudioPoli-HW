import sounddevice as sd
import numpy as np
import time
import requests
import io

# 바이너리 파일 경로
file_path = '/Users/minseok128/Downloads/test.wav'


def PI_ID():
    return "1"

def LATITUDE():
    return "37.503808"

def LONGTITUDE():
    return "126.955963"

with open(file_path, 'rb') as file:
    now_id = f"{PI_ID()}{time.strftime('%Y%m%d%H%M%S')}"
    files = {
        'sound': (f"{now_id}.wav", file, 'audio/wav')
    }
    post_data = {
        'id': int(now_id),
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M:%S'),
        'latitude': LATITUDE(),
        'longitude': LONGTITUDE()
    }
    try:
        response = requests.post('http://localhost:3000/rasberry', files=files, data=post_data)
        print(response.text)
        response.raise_for_status()  # 응답 상태 코드가 200 범위가 아닐 경우 예외 발생
    except Exception as err:
        print("error: ", err)