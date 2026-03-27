import numpy as np
import wave

# 16 bit audio, generate a 440Hz (A4) sine wave for 1 second
sampling_rate = 44100 #44.1kHz
frequency = 440
t = np.linspace(0, 1, sampling_rate)
note = (np.sin(2 * np.pi * t * frequency) * 32767).astype(np.int16)

data = note.tobytes()

with wave.open("output.wav", "w") as f:
    f.setnchannels(1) # 1 for mono
    f.setsampwidth(2) # 16 bit signed audio
    f.setframerate(sampling_rate) # 44.1kHz audio
    f.writeframes(data)
