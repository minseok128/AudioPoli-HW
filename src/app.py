import sounddevice as sd
import numpy as np
import time as pytime  # 'time' 대신 'pytime'으로 모듈 이름 변경

def print_sound_level(indata, frames, time, status):
    global last_time
    current_time = pytime.time()  # 'pytime.time()' 사용
    if current_time - last_time > 0.5:
        volume_norm = np.linalg.norm(indata) * 10
        print(f"Current sound level: {volume_norm:.2f} dB")
        last_time = current_time

last_time = pytime.time()

with sd.InputStream(callback=print_sound_level):
    sd.sleep(10000)  # 10초 동안 실행
