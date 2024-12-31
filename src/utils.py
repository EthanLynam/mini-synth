import numpy as np

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

def set_volume(value, synth):
    """Updates the volume of the synthesizer."""
    synth.volume = float(value)

def set_amplifier_gain(value, synth):
    """Updates the amplifier gain of the synthesizer."""
    synth.amplifier_gain = float(value)

def set_distortion_amount(value, synth):
    """Updates the distortion amount of the synthesizer."""
    synth.distortion_amount = float(value)

def set_reverb_amount(value, synth):
    """Updates the reverb amount of the synthesizer."""
    synth.reverb_amount = float(value)

def set_attack(value, synth):
    """Updates the attack amount of the synthesizer."""
    synth.attack_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_decay(value, synth):
    """Updates the decay amount of the synthesizer."""
    synth.decay_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_sustain(value, synth):
    """Updates the sustain amount of the synthesizer."""
    synth.sustain_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_release(value, synth):
    """Updates the release amount of the synthesizer."""
    synth.release_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_num_samples(value, synth):
    """Updates the number of samples to generate for the wave."""
    synth.num_samples = value
