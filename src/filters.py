import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from scipy.signal import butter, lfilter


# Function to generate waveforms
def generate_waveform(wave_type, freq, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    if wave_type == "sine":
        return np.sin(2 * np.pi * freq * t), t
    elif wave_type == "square":
        return np.sign(np.sin(2 * np.pi * freq * t)), t
    elif wave_type == "sawtooth":
        return 2 * (t * freq - np.floor(t * freq + 0.5)), t
    else:
        raise ValueError("Unsupported wave type!")


# Function to apply a low-pass filter
def low_pass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return lfilter(b, a, data)


# Function to play audio using PyAudio
def play_audio(data, fs=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(data.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


# Main script
if __name__ == "__main__":
    # Parameters
    fs = 44100  # Sampling frequency
    duration = 65.0  # Duration in seconds
    freq = 440.0  # Frequency of the waveform (e.g., A4 note)
    wave_type = "sine"  # Change to "square" or "sawtooth" for other waveforms
    cutoff_freq = 1000  # Low-pass filter cutoff frequency in Hz

    # Step 1: Generate waveform
    waveform, t = generate_waveform(wave_type, freq, duration, fs)

    # Step 2: Apply low-pass filter
    filtered_waveform = low_pass_filter(waveform, cutoff=cutoff_freq, fs=fs)

    # Step 3: Play the filtered waveform
    print("Playing the sound...")
    play_audio(filtered_waveform, fs=fs)
    print("Done!")

    # Step 4: Plot the original and filtered waveforms
    plt.figure(figsize=(10, 5))
    plt.plot(t[:1000], waveform[:1000], label="Original", alpha=0.7)
    plt.plot(t[:1000], filtered_waveform[:1000], label="Filtered", alpha=0.7)
    plt.title(f"{wave_type.capitalize()} Wave - Original vs Filtered")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

