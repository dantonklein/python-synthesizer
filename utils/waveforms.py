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

def apply_adsr(wave, attack, decay, sustain_level, release, sample_rate=44100):
    #calculate the amount of samples for each part
    attack_samples = sample_rate * attack
    decay_samples = sample_rate * decay
    release_samples = sample_rate * release
    sustain_samples = len(wave) - (attack_samples + decay_samples + release_samples)

    if(sustain_samples < 0) :
        raise ValueError(f"ADSR times exceed note duration. Attack + decay + release = {attack + decay + release:.2f}s but note is only {len(wave) / sample_rate:.2f}s")
    
    #build adsr segments
    attack_wave = np.linspace(0, 1, int(attack_samples))
    decay_wave = np.linspace(1, sustain_level, int(decay_samples))
    sustain_wave = np.ones(int(sustain_samples)) * sustain_level
    release_wave = np.linspace(sustain_level, 0, int(release_samples))

    #create adsr wave
    adsr_wave = np.concatenate([attack_wave, decay_wave, sustain_wave, release_wave])
    adsr_wave = adsr_wave[:len(wave)]
    return wave * adsr_wave
    
