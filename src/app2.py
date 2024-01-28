import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

def PI_ID():
    return "1"

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
