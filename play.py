import numpy as np
from pathlib import Path
import wave
from utils.notes import note_to_freq

# 16 bit audio, generate a 440Hz (A4) sine wave for 1 second
sampling_rate = 44100 #44.1kHz
frequency = 440
t = np.linspace(0, 1, sampling_rate)
note = (np.sin(2 * np.pi * t * frequency) * 32767).astype(np.int16)

data = note.tobytes()

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

with wave.open(str(output_dir / "output.wav"), "w") as f:
    f.setnchannels(1) # 1 for mono
    f.setsampwidth(2) # 16 bit signed audio
    f.setframerate(sampling_rate) # 44.1kHz audio
    f.writeframes(data)