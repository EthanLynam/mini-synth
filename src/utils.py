import numpy as np
from scipy.signal import butter, lfilter

# takes the frequency, sample rate. duration and waveform type, returns 
# one of 4 different types
def generate_wave(freq, duration, sample_rate, waveform="sine"):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if waveform == "sine":
        wave = np.sin(2 * np.pi * freq * t)
    elif waveform == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif waveform == "saw":
        wave = 2 * (t * freq - np.floor(t * freq + 0.5)) - 1
    elif waveform == "triangle":
        wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    else:
        wave = np.zeros_like(t)
    return wave

def normalize_wave(wave):
    return np.clip(wave, -1.0, 1.0)

def apply_filter(wave, sample_rate, filter_type, cutoff=1000):
    freq = sample_rate / 2
    normalized_cutoff = cutoff / freq  #0 to 1
    
    # creates the filter
    b, a = butter(N=4, Wn=normalized_cutoff, btype=filter_type)
    
    # apply the filter
    filtered_wave = lfilter(b, a, wave)
    return filtered_wave

def set_distortion_amount(value, synth):
    synth.distortion_amount = float(value)

def set_reverb_amount(value, synth):
    synth.reverb_amount = float(value)

def set_attack(value, synth):
    synth.attack_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_decay(value, synth):
    synth.decay_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_sustain(value, synth):
    synth.sustain_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_release(value, synth):
    synth.release_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount
    synth.num_samples = value
