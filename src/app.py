import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import requests
import io

def PI_ID():
    return "1"

def LATITUDE():
    return "37.503808691555875" 

def LONGTITUDE():
    return "126.95596349300216"

def post_to_server(data, fs):
    # 메모리에 있는 오디오 데이터를 wav 포맷으로 변환
    buffer = io.BytesIO()
    write(buffer, fs, data)
    buffer.seek(0)
    # 파일 형식으로 서버로 전송
    files = {
        'sound': (f"{PI_ID()}_{time.strftime('%Y%m%d_%H%M%S')}.wav", buffer, 'audio/wav')
    }
    post_data = {
        'id': PI_ID(),
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M:%S'),
        'latitude': LATITUDE(),
        'longtitude': LONGTITUDE()
    }
    try:
        response = requests.post('http://localhost:3000/rasberry', files=files, data=post_data)
        print(response.text)
        response.raise_for_status()  # 응답 상태 코드가 200 범위가 아닐 경우 예외 발생
    except Exception as err:
        print("error: ", err)

def sound_pressure_level(signal):
    rms = np.sqrt(np.mean(signal**2))
    spl = 20 * np.log10(rms / 20e-6)  # Sound Pressure Level in dB
    return spl

def record_audio(duration, fs):
    print("recording start")
    recording = sd.rec((duration * fs) & 0xFFFFFFFF, samplerate=fs, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("recording done")
    return recording

def main():
    threshold = 50  # dB
    fs = 44100  # Sample rate
    duration = 5  # seconds

    try:
        while True:
            recording = sd.rec(fs & 0xFFFFFFFF, samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            spl = sound_pressure_level(recording[:,0])
            print(f"now: {spl:.2f} dB")

            if spl > threshold:
                audio_data = record_audio(duration, fs)
                post_to_server(audio_data, fs)

    except KeyboardInterrupt:
        print("exit")

if __name__ == "__main__":
    main()
