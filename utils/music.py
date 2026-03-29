import numpy as np
import utils.waveforms as waveforms

WAVEFORMS = {
    "sine": waveforms.sine,
    "square": waveforms.square,
    "sawtooth": waveforms.sawtooth,
    "triangle": waveforms.triangle
}

NOTE_SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NOTE_ACCIDENTALS = {"#": 1, "b": -1}
NOTE_TYPES = {"whole" : 4, "half" : 2, "quarter" : 1, "eighth" : 0.5, "sixteenth" : 0.25}

def note_to_midi(note):
    letter = note[0]
    accidental = note[1] if len(note) == 3 else ""
    octave = note[2] if len(note) == 3 else note[1]
    return (int(octave)+1) * 12 + NOTE_SEMITONES[letter] + NOTE_ACCIDENTALS.get(accidental, 0)

def midi_to_freq(midi):
    return 440 * (2 ** ((midi-69) / 12))

def note_to_freq(note):
    return midi_to_freq(note_to_midi(note))

def durations_to_seconds(duration, bpm):
    return (NOTE_TYPES[duration] / bpm) * 60

class Note:
    def __init__(self, note_names, duration, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
        self.note_names = note_names
        self.duration = duration
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

    def create_array(self, bpm, waveform, sample_rate=44100):
        waveform_function = WAVEFORMS[waveform]
        duration_seconds = durations_to_seconds(self.duration, bpm)
        if isinstance(self.note_names, list):
            # for chords create all the waveforms, add them, and then normalize them
            note_waves = [waveform_function(note_to_freq(n), duration_seconds, sample_rate) for n in self.note_names]
            note_wave = waveforms.normalize(sum(note_waves))
        else:
            note_wave =  waveform_function(note_to_freq(self.note_names), duration_seconds, sample_rate)
        return waveforms.apply_adsr(note_wave, self.attack, self.decay, self.sustain, self.release, sample_rate)

    
    def __repr__(self):
        if isinstance(self.note_name, list):
            notes = ", ".join(self.note_name)
            return f"Note([{notes}], {self.duration})"
        return f"Note({self.note_name}, {self.duration})"
