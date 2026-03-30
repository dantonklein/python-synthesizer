import numpy as np
from pathlib import Path
import wave
import utils.music as music
import utils.waveforms as waveforms

# 16 bit audio, generate a 440Hz (A4) sine wave for 1 second
sampling_rate = 44100 #44.1kHz
bpm = 123
notes = []
notes.append(music.Note(["E4"], "quarter", "0:0"))
notes.append(music.Note(["D4"], "quarter", "0:1"))
notes.append(music.Note(["C4"], "quarter", "0:2"))
notes.append(music.Note(["D4"], "quarter", "0:3"))

notes.append(music.Note(["E4"], "quarter", "1:0"))
notes.append(music.Note(["E4"], "quarter", "1:1"))
notes.append(music.Note(["E4"], "half", "1:2"))

notes.append(music.Note(["D4"], "quarter", "2:0"))
notes.append(music.Note(["D4"], "quarter", "2:1"))
notes.append(music.Note(["D4"], "half", "2:2"))

notes.append(music.Note(["E4"], "quarter", "3:0"))
notes.append(music.Note(["G4"], "quarter", "3:1"))
notes.append(music.Note(["G4"], "half", "3:2"))

notes.append(music.Note(["E4"], "quarter", "4:0"))
notes.append(music.Note(["D4"], "quarter", "4:1"))
notes.append(music.Note(["C4"], "quarter", "4:2"))
notes.append(music.Note(["D4"], "quarter", "4:3"))

notes.append(music.Note(["E4"], "quarter", "5:0"))
notes.append(music.Note(["E4"], "quarter", "5:1"))
notes.append(music.Note(["E4"], "quarter", "5:2"))
notes.append(music.Note(["E4"], "quarter", "5:3"))

notes.append(music.Note(["D4"], "quarter", "6:0"))
notes.append(music.Note(["D4"], "quarter", "6:1"))
notes.append(music.Note(["E4"], "quarter", "6:2"))
notes.append(music.Note(["D4"], "quarter", "6:3"))

notes.append(music.Note(["C4"], "whole", "7:0"))

test = music.Track("test", waveforms.Sine(), "0:0", 8, 1, notes)

data = waveforms.wave_to_int16(test.create_array(bpm, sampling_rate, "4/4")).tobytes()

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

with wave.open(str(output_dir / "output.wav"), "w") as f:
    f.setnchannels(1) # 1 for mono
    f.setsampwidth(2) # 16 bit signed audio
    f.setframerate(sampling_rate) # 44.1kHz audio
    f.writeframes(data)