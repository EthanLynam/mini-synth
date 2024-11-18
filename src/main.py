from visual_waveform import visualise_waveform
import numpy as np
import scipy.io.wavfile as wav

def main():
    # sine wave generator for testing
    sample_rate = 44100 # 44100 Hz
    frequency = 440
    time = 3 # 3 seconds
    waveform = np.sin
    
    wavetable_length = 64
    wavetable = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wavetable[n] = waveform((2 * np.pi) * n / wavetable_length)

    output = np.zeros((time * sample_rate,))

    index = 0
    indexIncrement = frequency * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        output[n] = wavetable[int(np.floor(index))]
        index += indexIncrement
        index %= wavetable_length

    visualise_waveform(output, frequency, sample_rate)
        
if __name__ == '__main__':
    main()