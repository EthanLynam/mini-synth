import numpy as np
from scipy.signal import butter, lfilter

# synthesizer class
class Synthesizer:
    def __init__(self, sample_rate = 44100, num_samples = 10000):
        # initialize parameters for the class
        self.sample_rate = sample_rate # audio sample rate
        self.num_samples = num_samples # number of samples to be displayed
        self.volume = 0.5
        self.amplifier_gain = 1.0
        self.distortion_amount = 1.2
        self.reverb_amount = 0.0
        self.attack_amount = 0.0
        self.decay_amount = 0.0
        self.sustain_amount = 1.0
        self.release_amount = 0.0
        self.total_duration = 2
        self.filter_cutoff = 1000
        self.filter_type = "lowpass"
        self.filter_enabled = False
        self.waveform = "sine"

    def set_adsr(self, attack, decay, sustain, release):
        self.attack_amount = attack
        self.decay_amount = decay
        self.sustain_amount = sustain
        self.release_amount = release
        self.total_duration = attack + decay + sustain + release

    # applies ADSR to waveform
    def apply_adsr(self, wave):
        total_samples = len(wave)

        # check how many samples in each adsr phase
        attack_samples = int((self.attack_amount / self.total_duration) * total_samples)
        decay_samples = int((self.decay_amount / self.total_duration) * total_samples)
        sustain_samples = int(((self.total_duration - self.attack_amount - self.decay_amount - self.release_amount) / self.total_duration) * total_samples)
        release_samples = int((self.release_amount / self.total_duration) * total_samples)

        envelope = np.zeros(total_samples)

        # apply attack, which is a linear rise from beginning of sound
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # apply decay, which decays sound from 1 to sustain level
        if decay_samples > 0:
            decay_start = attack_samples
            decay_end = decay_start + decay_samples
            envelope[decay_start:decay_end] = np.linspace(1, self.sustain_amount, decay_samples)

        # apply sustain, which leaves sound at cnstant level
        if sustain_samples > 0:
            sustain_start = attack_samples + decay_samples
            sustain_end = sustain_start + sustain_samples
            envelope[sustain_start:sustain_end] = self.sustain_amount

        # apply release, which goes from sustain to 0
        if release_samples > 0:
            release_start = attack_samples + decay_samples + sustain_samples
            release_end = release_start + release_samples
            envelope[release_start:release_end] = np.linspace(self.sustain_amount, 0, release_samples)

        # applies changes to waveform
        wave = wave[:total_samples] * envelope
        return wave

    # function to apply distortion, an effect, to waveform
    def apply_distortion(self, wave):
        return np.clip(wave, -self.distortion_amount, self.distortion_amount)

    def apply_reverb(self, wave):
        reverb_signal = np.zeros_like(wave)# setup reverb signal
        decay = int(0.01 * self.sample_rate)

        for i in range(len(wave)):
            reverb_signal[i] = wave[i]

            if i >= decay:
                reverb_signal[i] += self.reverb_amount * wave[i - decay]

        return reverb_signal

    def apply_filtering(self, wave, sample_rate, filter_type, cutoff=1000):
        # returns unfiltered wave if filter is not toggled on
        if not self.filter_enabled:
            return wave

        freq = sample_rate / 2 # nyquist freq
        normalized_cutoff = cutoff / freq  #0 to 1

        # creates the filter coefficients with butterworth
        b, a = butter(N=4, Wn=normalized_cutoff, btype=filter_type)

        # apply the filter
        filtered_wave = lfilter(b, a, wave)
        return filtered_wave

    # normalize wave in range -1.0 - 1.0
    def normalize_wave(self, wave):
        return np.clip(wave, -1.0, 1.0)

    def generate_and_process_wave(self, freq):
        # time array
        t = np.linspace(0, self.total_duration, int(self.sample_rate * self.total_duration), endpoint=False)

        # checks which waveform the user has selected. default is sine
        if self.waveform == "sine":
            wave = np.sin(2 * np.pi * freq * t)
        elif self.waveform == "square":
            wave = np.sign(np.sin(2 * np.pi * freq * t))
        elif self.waveform == "saw":
            wave = 2 * (t * freq - np.floor(t * freq + 0.5)) - 1
        elif self.waveform == "triangle":
            wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        else:
            return

        # chain the changes to the wave
        wave = self.apply_adsr(wave)
        wave = self.apply_distortion(wave)
        wave = self.apply_reverb(wave)
        wave = self.apply_filtering(wave, self.sample_rate, self.filter_type, self.filter_cutoff)

        # normalize the wave in a range
        wave = self.normalize_wave(wave)

        return wave
