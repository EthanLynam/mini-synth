import tkinter as tk
from tkinter import ttk
import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
DURATION = 0.1  # Duration per buffer in seconds

# Global state
frequency = 440.0
cutoff_frequency = 2000.0
filter_type = "lowpass"
wavetable_length = 64
wavetable = np.sin(2 * np.pi * np.arange(wavetable_length) / wavetable_length)


def generate_waveform(frequency, duration=0.1):
    """Generate a sine wave buffer."""
    global wavetable
    num_samples = int(SAMPLE_RATE * duration)
    output = np.zeros(num_samples)
    index = 0
    index_increment = frequency * wavetable_length / SAMPLE_RATE

    for i in range(num_samples):
        output[i] = wavetable[int(index) % wavetable_length]
        index += index_increment

    return output


def apply_filter(data, cutoff, filter_type):
    """Apply low-pass or high-pass filter to data."""
    nyquist = 0.5 * SAMPLE_RATE
    normal_cutoff = cutoff / nyquist
    b, a = butter(4, normal_cutoff, btype=filter_type, analog=False)
    return lfilter(b, a, data)


def audio_callback(outdata, frames, time, status):
    """Callback for real-time audio output."""
    global frequency, cutoff_frequency, filter_type
    buffer = generate_waveform(frequency, DURATION)
    if filter_type != "none":
        buffer = apply_filter(buffer, cutoff_frequency, filter_type)
    outdata[:] = np.expand_dims(buffer, axis=1)


def update_visualization():
    """Update the waveform visualization in the Tkinter canvas."""
    global frequency, cutoff_frequency, filter_type
    buffer = generate_waveform(frequency, DURATION)
    if filter_type != "none":
        buffer = apply_filter(buffer, cutoff_frequency, filter_type)

    # Update the plot
    line.set_ydata(buffer)
    canvas.draw_idle()

    # Schedule the next update
    root.after(50, update_visualization)


def on_frequency_change(value):
    """Update frequency from slider."""
    global frequency
    frequency = float(value)


def on_cutoff_change(value):
    """Update cutoff frequency from slider."""
    global cutoff_frequency
    cutoff_frequency = float(value)


def on_filter_change(value):
    """Update filter type from dropdown."""
    global filter_type
    filter_type = value.lower()


# Tkinter Setup
root = tk.Tk()
root.title("Real-Time Synthesizer")

# Frequency Control
tk.Label(root, text="Frequency (Hz)").grid(row=0, column=0, padx=5, pady=5)
frequency_slider = tk.Scale(root, from_=20, to=2000, orient="horizontal", resolution=1, command=on_frequency_change)
frequency_slider.set(frequency)
frequency_slider.grid(row=0, column=1, padx=5, pady=5)

# Cutoff Frequency Control
tk.Label(root, text="Cutoff Frequency (Hz)").grid(row=1, column=0, padx=5, pady=5)
cutoff_slider = tk.Scale(root, from_=20, to=20000, orient="horizontal", resolution=1, command=on_cutoff_change)
cutoff_slider.set(cutoff_frequency)
cutoff_slider.grid(row=1, column=1, padx=5, pady=5)

# Filter Type Selection
tk.Label(root, text="Filter Type").grid(row=2, column=0, padx=5, pady=5)

filter_var = tk.StringVar(value="Lowpass")  # Create a StringVar to track the combobox value
filter_menu = ttk.Combobox(root, textvariable=filter_var, values=["None", "Lowpass", "Highpass"], state="readonly")
filter_menu.grid(row=2, column=1, padx=5, pady=5)

# Trace changes in the combobox value
filter_var.trace_add("write", lambda *args: on_filter_change(filter_var.get()))


# Matplotlib Figure for Waveform
fig, ax = plt.subplots(figsize=(5, 2))
x = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION))
line, = ax.plot(x, generate_waveform(frequency, DURATION))
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, DURATION)
ax.set_title("Waveform")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

# Start Audio Stream
stream = sd.OutputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1, blocksize=BUFFER_SIZE)
stream.start()

# Start Visualization Update Loop
update_visualization()

# Run Tkinter Main Loop
root.mainloop()

# Stop the audio stream when the application is closed
stream.stop()
stream.close()
