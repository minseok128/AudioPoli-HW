import sounddevice as sd
import pyaudio
import wave
import numpy as np
import time as pytime
import threading

# 소리 녹음에 사용되는 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

recording = False  # 녹음 상태 플래그

def print_sound_level(indata, frames, time, status):
    global recording
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > 50 and not recording:
        recording = True
        print("High volume detected, starting to record...")
        threading.Thread(target=record_audio).start()

# 오디오 녹음 함수
def record_audio():
    print("Start to record the audio.")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        print("Reading chunk number:", i)
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording finished and saved to", WAVE_OUTPUT_FILENAME)

# 소리 감지 시작
with sd.InputStream(callback=print_sound_level):
    sd.sleep(10000)  # 10초 동안 대기하며 소리 감지
