import numpy as np

NOTE_SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NOTE_ACCIDENTALS = {"#": 1, "b": -1}

def note_to_midi(note):
    letter = note[0]
    accidental = note[1] if len(note) == 3 else ""
    octave = note[2] if len(note) == 3 else note[1]
    return (int(octave)+1) * 12 + NOTE_SEMITONES[letter] + NOTE_ACCIDENTALS.get(accidental, 0)

def midi_to_freq(midi):
    return 440 * (2 ** ((midi-69) / 12))

def note_to_freq(note):
    return midi_to_freq(note_to_midi(note))