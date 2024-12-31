import numpy as np
from utils import generate_wave, normalize_wave

class Synthesizer:
    def __init__(self, sample_rate = 44100, num_samples = 44100):
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.volume = 0.5
        self.amplifier_gain = 1.0
        self.distortion_amount = 1.2  # No distortion by default
        self.reverb_amount = 0.0  # No reverb by default
        self.attack_amount = 0.0  # No attack by default
        self.decay_amount = 0.0  # No decay by default
        self.sustain_amount = 1.0  # Full sustain (no volume change)
        self.release_amount = 0.0  # No release by default
        self.total_duration = 1.0  # Default duration of the sound

    def set_adsr(self, attack, decay, sustain, release):
        self.attack_amount = attack
        self.decay_amount = decay
        self.sustain_amount = sustain
        self.release_amount = release
        self.total_duration = attack + decay + sustain + release

    def apply_adsr(self, wave):
        total_samples = len(wave)
        attack_samples = int((self.attack_amount / self.total_duration) * total_samples)
        decay_samples = int((self.decay_amount / self.total_duration) * total_samples)
        sustain_samples = int(((self.total_duration - self.attack_amount - self.decay_amount - self.release_amount) / self.total_duration) * total_samples)
        release_samples = int((self.release_amount / self.total_duration) * total_samples)

        envelope = np.zeros(total_samples)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if decay_samples > 0:
            decay_start = attack_samples
            decay_end = decay_start + decay_samples
            envelope[decay_start:decay_end] = np.linspace(1, self.sustain_amount, decay_samples)
        if sustain_samples > 0:
            sustain_start = attack_samples + decay_samples
            sustain_end = sustain_start + sustain_samples
            envelope[sustain_start:sustain_end] = self.sustain_amount
        if release_samples > 0:
            release_start = attack_samples + decay_samples + sustain_samples
            release_end = release_start + release_samples
            envelope[release_start:release_end] = np.linspace(self.sustain_amount, 0, release_samples)

        wave = wave[:total_samples] * envelope
        return wave

    def apply_distortion(self, wave):
        return np.clip(wave, -self.distortion_amount, self.distortion_amount)

    def apply_reverb(self, wave):
        reverb_signal = np.zeros_like(wave)
        decay = int(0.01 * self.sample_rate)
        for i in range(len(wave)):
            reverb_signal[i] = wave[i]
            if i >= decay:
                reverb_signal[i] += self.reverb_amount * reverb_signal[i - decay]
        return reverb_signal

    def process_wave(self, wave):
        wave = self.apply_adsr(wave)
        wave = self.apply_distortion(wave)
        wave = self.apply_reverb(wave)
        return normalize_wave(wave)

    def generate_and_process_wave(self, freq, waveform="sine"):
        wave = generate_wave(freq, self.total_duration, self.sample_rate, waveform)
        return self.process_wave(wave)
    
    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
