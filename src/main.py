import tkinter as tk
from tkinter import ttk
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from synthesizer import Synthesizer
from utils import set_distortion_amount
from utils import set_reverb_amount
from utils import set_attack
from utils import set_decay
from utils import set_sustain
from utils import set_release

# PyAudio setup
p = pyaudio.PyAudio()
synth = Synthesizer()

# GUI setup
root = tk.Tk()
root.title("Synthesizer with Piano Keyboard")

# Visualization setup
fig, ax = plt.subplots()
ax.set_title("Waveform Visualization")
ax.set_xlabel("Time (samples)")
ax.set_ylabel("Amplitude")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def update_visualization(wave):
    ax.clear()
    ax.plot(wave[:synth.num_samples])
    ax.set_ylim(-1.0, 1.0)
    canvas.draw()

# Play Wave Function
def play_wave(freq):
    global waveform
    wave = synth.generate_and_process_wave(freq, waveform.get())
    wave = wave * synth.volume * synth.amplifier_gain
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=synth.sample_rate, output=True)
        stream.write(wave.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error playing sound: {e}")
    update_visualization(wave)

# Controls for Synthesizer Parameters
def create_controls(frame):
    # Volume Slider
    vol_label = ttk.Label(frame, text="Volume:")
    vol_label.pack(side=tk.LEFT, padx=5)
    vol_slider = ttk.Scale(
        frame,
        from_=0.1,
        to=1.0,
        orient=tk.HORIZONTAL,
        command=lambda value: setattr(synth, 'volume', float(value))
    )
    vol_slider.set(synth.volume)
    vol_slider.pack(side=tk.LEFT, padx=5)

    # Amplifier Gain Slider
    amp_label = ttk.Label(frame, text="Amplifier Gain:")
    amp_label.pack(side=tk.LEFT, padx=5)
    amp_slider = ttk.Scale(
        frame,
        from_=0.1,
        to=5.0,
        orient=tk.HORIZONTAL,
        command=lambda value: setattr(synth, 'amplifier_gain', float(value))
    )
    amp_slider.set(synth.amplifier_gain)
    amp_slider.pack(side=tk.LEFT, padx=5)

    # Distortion Slider (uses utility function)
    distortion_label = ttk.Label(frame, text="Distortion:")
    distortion_label.pack(side=tk.LEFT, padx=5)
    distortion_slider = ttk.Scale(
        frame,
        from_=1.2,
        to=0.1,
        orient=tk.HORIZONTAL,
        command=lambda value: set_distortion_amount(value, synth)
    )
    distortion_slider.set(synth.distortion_amount)
    distortion_slider.pack(side=tk.LEFT, padx=5)

    # Reverb Slider (uses utility function)
    reverb_label = ttk.Label(frame, text="Reverb:")
    reverb_label.pack(side=tk.LEFT, padx=5)
    reverb_slider = ttk.Scale(
        frame,
        from_=0.0,
        to=1.0,
        orient=tk.HORIZONTAL,
        command=lambda value: set_reverb_amount(value, synth)
    )
    reverb_slider.set(synth.reverb_amount)
    reverb_slider.pack(side=tk.LEFT, padx=5)

    # Attack Slider (uses utility function)
    attack_label = ttk.Label(frame, text="Attack:")
    attack_label.pack(side=tk.LEFT, padx=5)
    attack_slider = ttk.Scale(
        frame,
        from_=0.0,
        to=1.0,
        orient=tk.HORIZONTAL,
        command=lambda value: set_attack(value, synth)
    )
    attack_slider.set(synth.attack_amount)
    attack_slider.pack(side=tk.LEFT, padx=5)

    # Decay Slider (uses utility function)
    decay_label = ttk.Label(frame, text="Decay:")
    decay_label.pack(side=tk.LEFT, padx=5)
    decay_slider = ttk.Scale(
        frame,
        from_=0.0,
        to=1.0,
        orient=tk.HORIZONTAL,
        command=lambda value: set_decay(value, synth)
    )
    decay_slider.set(synth.decay_amount)
    decay_slider.pack(side=tk.LEFT, padx=5)

    # Release Slider (uses utility function)
    release_label = ttk.Label(frame, text="Release:")
    release_label.pack(side=tk.LEFT, padx=5)
    release_slider = ttk.Scale(
        frame,
        from_=0.0,
        to=2.0,
        orient=tk.HORIZONTAL,
        command=lambda value: set_release(value, synth)
    )
    release_slider.set(synth.release_amount)
    release_slider.pack(side=tk.LEFT, padx=5)

    # Sustain Slider (uses utility function)
    sustain_label = ttk.Label(frame, text="Sustain:")
    sustain_label.pack(side=tk.LEFT, padx=5)
    sustain_slider = ttk.Scale(
        frame,
        from_=0.0,
        to=1.0,
        orient=tk.HORIZONTAL,
        command=lambda value: set_sustain(value, synth)
    )
    sustain_slider.set(synth.sustain_amount)
    sustain_slider.pack(side=tk.LEFT, padx=5)

    # Samples Slider
    samples_label = ttk.Label(frame, text="Samples:")
    samples_label.pack(side=tk.LEFT, padx=5)
    samples_slider = ttk.Scale(
        frame,
        from_=100,
        to=44100,
        orient=tk.HORIZONTAL,
        command=lambda value: setattr(synth, 'num_samples', int(float(value)))
    )
    samples_slider.set(synth.num_samples)
    samples_slider.pack(side=tk.LEFT, padx=5)

    # Filter Cutoff Slider
    filter_label = ttk.Label(frame, text="Filter Cutoff:")
    filter_label.pack(side=tk.LEFT, padx=5)
    filter_slider = ttk.Scale(
        frame,
        from_=10,  # Minimum cutoff frequency
        to=500,  # Maximum cutoff frequency
        orient=tk.HORIZONTAL,
        command=lambda value: setattr(synth, 'filter_cutoff', float(value))
    )
    filter_slider.set(synth.filter_cutoff)
    filter_slider.pack(side=tk.LEFT, padx=5)

    # Filter Type Dropdown
    filter_type_label = ttk.Label(frame, text="Filter Type:")
    filter_type_label.pack(side=tk.LEFT, padx=5)
    filter_type_var = tk.StringVar(value="lowpass")
    filter_type_dropdown = ttk.OptionMenu(
        frame,
        filter_type_var,
        "lowpass",
        "highpass",
        command=lambda value: setattr(synth, 'filter_type', value)
    )
    filter_type_dropdown.pack(side=tk.LEFT, padx=5)



# Waveform Selection
def create_waveform_selection(left_frame):
    global waveform
    waveform = tk.StringVar(left_frame, "sine")
    wave_label = ttk.Label(left_frame, text="Waveform:")
    wave_label.pack(side=tk.LEFT, padx=5)
    for wf in ["sine", "square", "saw", "triangle"]:
        wave_button = ttk.Radiobutton(
            left_frame, text=wf.capitalize(), value=wf, variable=waveform
        )
        wave_button.pack(side=tk.LEFT, padx=5)

# Piano Keys
def create_piano_keys(keyboard_frame):
    white_notes = [("C", 261.63), ("D", 293.66), ("E", 329.63), ("F", 349.23),
                   ("G", 392.00), ("A", 440.00), ("B", 493.88)]
    black_notes = [("C#", 277.18), ("D#", 311.13), None, ("F#", 369.99), ("G#", 415.30), ("A#", 466.16)]

    white_keys = []
    black_keys = []

    for i, (note, freq) in enumerate(white_notes):
        key = tk.Button(keyboard_frame, text=note, width=5, height=15, bg="white", relief="raised",
                        command=lambda f=freq: play_wave(f))
        key.grid(row=0, column=i, padx=1, pady=10)
        white_keys.append(key)

    for i, note_data in enumerate(black_notes):
        if note_data:
            note, freq = note_data
            key = tk.Button(keyboard_frame, text=note, width=3, height=8, bg="black", fg="white", relief="raised",
                            command=lambda f=freq: play_wave(f))
            key.place(x=30 + (i * 50), y=10)
            black_keys.append(key)

# Layout
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
create_controls(control_frame)

keyboard_frame = tk.Frame(root)
keyboard_frame.pack(side=tk.BOTTOM, pady=10)
create_piano_keys(keyboard_frame)

top_frame = ttk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)
create_waveform_selection(top_frame)

# Run Application
root.mainloop()
p.terminate()
