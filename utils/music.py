import numpy as np
import utils.waveforms as waveforms

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

def bars_to_samples_length(bars, bpm, time_signature, sample_rate=44100):
    beats_per_bar, beat_unit = time_signature.split("/")
    beats_per_bar, beat_unit = int(beats_per_bar), int(beat_unit)
    seconds_per_bar = (60 / bpm) * (4 / beat_unit) * beats_per_bar
    return int(bars * seconds_per_bar * sample_rate)

class Note:
    def __init__(self, note_names, duration, position, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
        self.note_names = note_names
        self.duration = duration
        self.position = position # in the form of "bar:beat"
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

    def create_array(self, bpm, waveform, sample_rate=44100):
        duration_seconds = durations_to_seconds(self.duration, bpm)
        if len(self.note_names) > 1:
            # for chords create all the waveforms, add them, and then normalize them
            note_waves = [waveform.generate(note_to_freq(n), duration_seconds, sample_rate) for n in self.note_names]
            note_wave = waveforms.normalize(sum(note_waves))
        else:
            note_wave =  waveform.generate(note_to_freq(self.note_names[0]), duration_seconds, sample_rate)
        return waveforms.apply_adsr(note_wave, self.attack, self.decay, self.sustain, self.release, sample_rate)

    def __repr__(self):
        if isinstance(self.note_name, list):
            notes = ", ".join(self.note_name)
            return f"Note([{notes}], {self.duration}, {self.position})"
        return f"Note({self.note_name}, {self.duration}, {self.position})"

class Track:
    def __init__ (self, name, waveform, position, length, volume, notes):
        self.name = name
        self.waveform = waveform
        self.volume = volume # from 0 to 1
        self.notes = notes # list of note objects
        self.position = position
        self.length = length # in bars

    def create_array(self, bpm, sample_rate, time_signature):
        samples_length = bars_to_samples_length(self.length, bpm, time_signature, sample_rate) #total length of track
        track_array = np.zeros(samples_length)
        length_of_bar = bars_to_samples_length(1, bpm, time_signature, sample_rate)
        beats_per_bar = int(time_signature.split("/")[0])
        for note_n in self.notes:
            position_n = note_n.position
            bars_n, beats_n = position_n.split(":")
            bars_n, beats_n = float(bars_n), float(beats_n)
            position_samples = int(length_of_bar * (bars_n + beats_n / beats_per_bar))
            note_waveform = note_n.create_array(bpm, self.waveform, sample_rate)
            track_array[position_samples:position_samples+len(note_waveform)] += note_waveform
        return waveforms.normalize(track_array) * self.volume
    
    def __repr__(self):
        return f"Track({self.name}, {self.waveform}, {len(self.notes)} notes)"


class Song:
    def __init__ (self, name, bpm, length, tracks, sample_rate = 44100, time_signature = "4/4"):
        self.name = name
        self.bpm = bpm
        self.time_signature = time_signature # default of 4/4
        self.length = length # in bars
        self.sample_rate = sample_rate
        self.tracks = tracks # array of tracks

    def create_array(self):
        song_length = bars_to_samples_length(self.length, self.bpm, self.time_signature, self.sample_rate)
        song_array = np.zeros(song_length)
        length_of_bar = bars_to_samples_length(1, self.bpm, self.time_signature, self.sample_rate)
        for track_n in self.tracks:
            position_n = track_n.position
            position_samples = int(length_of_bar * position_n)
            track_waveform_n = track_n.create_array(self.bpm, self.sample_rate, self.time_signature)
            song_array[position_samples:position_samples+len(track_waveform_n)] += track_waveform_n
        return waveforms.normalize(song_array)
    
    def __repr__(self):
        return f"Song({self.name}, {self.bpm}, {self.time_signature}, {self.tracks})"