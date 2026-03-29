import numpy as np
from pathlib import Path
import wave
import utils.music as music
import utils.waveforms as waveforms

# 16 bit audio, generate a 440Hz (A4) sine wave for 1 second
sampling_rate = 44100 #44.1kHz
test = music.Note(["E4", "G#4", "B4"], "whole")


data = waveforms.wave_to_int16(test.create_array(120, "sine", sampling_rate)).tobytes()

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

with wave.open(str(output_dir / "output.wav"), "w") as f:
    f.setnchannels(1) # 1 for mono
    f.setsampwidth(2) # 16 bit signed audio
    f.setframerate(sampling_rate) # 44.1kHz audio
    f.writeframes(data)