import numpy as np
from synthesizer import Synthesizer

def test_adsr():
    synth = Synthesizer()
    wave = np.ones(1000)  # waveform of constant value
    synth.set_adsr(0.2, 0.2, 0.5, 0.1)
    processed_wave = synth.apply_adsr(wave)

    # max amplitude after processing is 1.0
    assert np.isclose(processed_wave.max(), 1.0)

    # Checkthe last part of the wave is 0
    assert np.isclose(processed_wave[-1], 0.0)

def test_waveform_generation():
    synth = Synthesizer()

    # test Sine wave generation (automatically a sine)
    sine_wave = synth.generate_and_process_wave(440)
    assert sine_wave is not None
    assert np.all(sine_wave <= 1.0) and np.all(sine_wave >= -1.0) # ensure normalization

    # Change waveform to square and test again
    synth.waveform = "square"
    square_wave = synth.generate_and_process_wave(440)
    assert square_wave is not None
    assert np.all(square_wave <= 1.0) and np.all(square_wave >= -1.0)

def test_distortion():
    synth = Synthesizer()
    synth.distortion_amount = 2.0
    wave = np.linspace(-1, 1, 1000)  # waveform from -1 to 1
    distorted_wave = synth.apply_distortion(wave)

    # distortion limits the values within the range
    assert np.all(distorted_wave <= synth.distortion_amount) and np.all(distorted_wave >= -synth.distortion_amount)

def test_reverb():
    synth = Synthesizer()
    synth.reverb_amount = 0.5
    wave = np.linspace(0, 1, 1000)
    reverb_wave = synth.apply_reverb(wave)

    # check reverb signal is not same as original wave
    assert not np.array_equal(reverb_wave, wave)

def test_filter():
    synth = Synthesizer()
    synth.filter_enabled = True
    synth.filter_cutoff = 500
    wave = synth.generate_and_process_wave(440)
    filtered_wave = synth.apply_filtering(wave, synth.sample_rate, synth.filter_type, synth.filter_cutoff)

    # check that the filtered wave is different from original
    assert not np.array_equal(filtered_wave, wave)

def test_wave_normalization():
    synth = Synthesizer()
    wave = np.linspace(2, 3, 1000)  # wave greater than 1
    normalized_wave = synth.normalize_wave(wave)

    # check the wave is normalized between -1 and 1
    assert np.all(normalized_wave <= 1.0) and np.all(normalized_wave >= -1.0)

def run_tests():
    test_adsr()
    test_waveform_generation()
    test_distortion()
    test_reverb()
    test_filter()
    test_wave_normalization()
    print("This message indicates all test have passed. Yippeeeee")

if __name__ == "__main__":
    run_tests()
