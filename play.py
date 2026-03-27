import numpy as np
from pathlib import Path
import wave
from utils.notes import note_to_freq
import utils.waveforms as waveforms

# 16 bit audio, generate a 440Hz (A4) sine wave for 1 second
sampling_rate = 44100 #44.1kHz
frequency = note_to_freq("A4")
song = waveforms.triangle(frequency, 1, sampling_rate)


data = waveforms.wave_to_int16(song).tobytes()

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

with wave.open(str(output_dir / "output.wav"), "w") as f:
    f.setnchannels(1) # 1 for mono
    f.setsampwidth(2) # 16 bit signed audio
    f.setframerate(sampling_rate) # 44.1kHz audio
    f.writeframes(data)