import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import requests
import io
import os
from dotenv import load_dotenv


def PI_ID():
    return "02"

def LATITUDE():
    latitudes = {
        "01": "37.506700",
        "02": "37.506241",
        "03": "37.505782",
        "04": "37.505323",
        "05": "37.504864",
        "06": "37.504405",
        "07": "37.504100",
        "08": "37.504500",
        "09": "37.504800",
        "10": "37.504241"
    }
    return latitudes.get(PI_ID())

def LONGITUDE():
    longitudes = {
        "01": "126.959567",
        "02": "126.959900",
        "03": "126.960233",
        "04": "126.960566",
        "05": "126.960899",
        "06": "126.951232",
        "07": "126.951565",
        "08": "126.951898",
        "09": "126.952231",
        "10": "126.951557"
    }
    return longitudes.get(PI_ID())

def post_to_server(data, fs):
    # 메모리에 있는 오디오 데이터를 wav 포맷으로 변환
    buffer = io.BytesIO()
    write(buffer, fs, data)
    buffer.seek(0)
    # 파일 형식으로 서버로 전송
    now_id = f"{time.strftime('%Y%m%d%H%M%S')}{PI_ID()}"
    files = {
        'sound': (f"{now_id}.wav", buffer, 'audio/wav')
    }
    post_data = {
        'id': int(now_id),
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M:%S'),
        'latitude': LATITUDE(),
        'longitude': LONGITUDE()
    }
    try:
        response = requests.post(os.getenv("SERVERURL"), files=files, data=post_data)
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
    recording = sd.rec((duration * fs) & 0xFFFFFFFF, samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("recording done")
    return recording

def main():
    load_dotenv()
    threshold = 50  # dB
    fs = 44100  # Sample rate
    duration = 5  # seconds

    try:
        while True:
            recording = sd.rec(fs & 0xFFFFFFFF, samplerate=fs, channels=1, dtype='int16')
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
