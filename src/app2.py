import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import requests

import base64


def PI_ID():
    return "1"

def LATITUDE():
    return "37.503808691555875" 

def LONGTITUDE():
    return "126.95596349300216"

# {
#     id : 2,
#     date : "2024-01-24",
#     time : "13:51:50",
#     latitude : 37.5058,
#     longtitude : 126.956,
#     sound: "base 64 string"
# }

# WAV 파일을 읽고 Base64로 인코딩
def encode_audio(file_path):
    with open(file_path, 'rb') as audio_file:
        encoded_audio = base64.b64encode(audio_file.read())
    return encoded_audio

def post_to_server(filename):
    print("서버로 전송 시도")
    data = {
            'id': PI_ID(), 
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S'),
            'latitude': LATITUDE(),
            'longtitude': LONGTITUDE(),
            'sound': encode_audio(filename)
        }
    response = requests.post('http://localhost:3000/rasberry', data=data)

def sound_pressure_level(signal):
    """ Calculate the sound pressure level of the signal """
    rms = np.sqrt(np.mean(signal**2))
    spl = 20 * np.log10(rms / 20e-6)  # Sound Pressure Level in dB
    return spl

def record_audio(duration, fs, filename):
    """ Record audio for a given duration and save it to a file """
    print("녹음 시작...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)  # Save the recording
    print(f"녹음 완료: {filename}")
    post_to_server(filename)

def main():
    threshold = 50  # dB
    fs = 44100  # Sample rate
    duration = 5  # seconds

    try:
        while True:
            print("데시벨 측정 중...")
            recording = sd.rec(int(fs * 2), samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            spl = sound_pressure_level(recording[:,0])
            print(f"현재 데시벨: {spl:.2f} dB")

            if spl > threshold:
                filename = f"{PI_ID()}_{time.strftime('%Y%m%d_%H%M%S')}.wav"
                record_audio(duration, fs, filename)

    except KeyboardInterrupt:
        print("프로그램 종료")

if __name__ == "__main__":
    main()
