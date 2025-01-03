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

# visualization setup
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
    wave = synth.generate_and_process_wave(freq)
    wave = wave * synth.volume * synth.amplifier_gain

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=synth.sample_rate, output=True)
    stream.write(wave.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()

    update_visualization(wave)

def create_effects_UI(frame):
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

def create_volume_UI(frame):
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

def create_filters_UI(frame):
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

# Controls for Synthesizer Parameters
def create_ADSR_UI(frame):
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

def create_waveform_UI(frame):
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

# Waveform Selection
def create_waveform_selection_UI(frame):

    waveform = tk.StringVar(frame, synth.waveform)
    wave_label = ttk.Label(frame, text="Waveform:")
    wave_label.pack(side=tk.LEFT, padx=5)

    for wf in ["sine", "square", "saw", "triangle"]:
        wave_button = ttk.Radiobutton(
            frame, text=wf.capitalize(), value=wf, variable=waveform,
            command=lambda wf=wf: setattr(synth, 'waveform', wf)
        )
        wave_button.pack(side=tk.LEFT, padx=5)
    waveform.set(synth.waveform)


def create_piano_keys(frame):
    # White and black notes for 3 octaves starting from C1
    white_notes = [("C1", 130.81), ("D1", 146.83), ("E1", 164.81), ("F1", 174.61),
                   ("G1", 196.00), ("A1", 220.00), ("B1", 246.94),
                   ("C2", 261.63), ("D2", 293.66), ("E2", 329.63), ("F2", 349.23),
                   ("G2", 392.00), ("A2", 440.00), ("B2", 493.88),
                   ("C3", 523.25), ("D3", 587.33), ("E3", 659.26), ("F3", 698.46),
                   ("G3", 783.99), ("A3", 880.00), ("B3", 987.77)]
    black_notes = [("C#1", 138.59), ("D#1", 155.56), None, ("F#1", 185.00), ("G#1", 207.65), ("A#1", 233.08),
                   ("C#2", 554.37), ("D#2", 622.25), None, ("F#2", 739.99), ("G#2", 830.61), ("A#2", 932.33),
                   ("C#3", 554.37), ("D#3", 622.25), None, ("F#3", 740.00), ("G#3", 830.61), ("A#3", 932.33)]

    white_keys = []
    black_keys = []

    # Create white keys (buttons)
    for i, (note, freq) in enumerate(white_notes):
        key = tk.Button(frame, text=note, width=5, height=15, bg="white", relief="raised",
                        command=lambda f=freq: play_wave(f))
        key.grid(row=0, column=i, padx=1, pady=10)
        white_keys.append(key)

    # Create black keys (buttons)
    for i, note_data in enumerate(black_notes):
        if note_data:
            note, freq = note_data
            key = tk.Button(frame, text=note, width=3, height=8, bg="black", fg="white", relief="raised",
                            command=lambda f=freq: play_wave(f))
            key.place(x=30 + (i * 50), y=10)
            black_keys.append(key)

# Layout

# Central Controls
controls_frame = ttk.Frame(root)
controls_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)

# Waveform Selection at the Top
waveform_frame = ttk.LabelFrame(controls_frame, text="Waveforms")
waveform_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
create_waveform_selection_UI(waveform_frame)

# ADSR Controls
adsr_frame = ttk.LabelFrame(controls_frame, text="ADSR")
adsr_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
create_ADSR_UI(adsr_frame)

# Effects Controls
effects_frame = ttk.LabelFrame(controls_frame, text="Effects")
effects_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
create_effects_UI(effects_frame)

# Filters Controls
filters_frame = ttk.LabelFrame(controls_frame, text="Filters")
filters_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
create_filters_UI(filters_frame)

# Volume Control
volume_frame = ttk.LabelFrame(controls_frame, text="Volume")
volume_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
create_volume_UI(volume_frame)

# Keyboard at the Bottom
keyboard_frame = ttk.Frame(root)
keyboard_frame.pack(side=tk.BOTTOM, pady=10)
create_piano_keys(keyboard_frame)

# Run Application
root.mainloop()
p.terminate()
