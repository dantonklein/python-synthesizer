import numpy as np

def sine(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * t * freq)

def square(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sign(np.sin(2 * np.pi * t * freq))

def sawtooth(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.mod(t, (1/freq)) * freq * 2 - 1

def triangle(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.abs(np.mod(t, (1/freq)) * freq - 0.5) * 4 - 1

def normalize(wave):
    return wave / np.max(np.abs(wave))

def wave_to_int16(wave):
    return (wave * 32767).astype(np.int16)