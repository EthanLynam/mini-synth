import tkinter as tk
from tkinter import ttk
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# PyAudio setup
p = pyaudio.PyAudio()
volume = 0.5
amplifier_gain = 1.0
sample_rate = 44100
distortion_amount = 1
reverb_amount = 0.0

# ADSR parameters
attack = 0.1  # Attack time in seconds
decay = 0.1   # Decay time in seconds
sustain = 0.7  # Sustain level (0 to 1)
release = 0.5  # Release time in seconds

# Function to generate waveforms
def generate_wave(freq, duration=0.5, waveform="sine"):
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

# Apply ADSR envelope
def apply_adsr(wave, key_press_duration, attack, decay, sustain, release):
    total_samples = len(wave)
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    sustain_samples = int(key_press_duration * sample_rate)
    release_samples = int(release * sample_rate)

    envelope = np.zeros(total_samples)

    # Attack phase
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Decay phase
    if decay_samples > 0:
        decay_start = attack_samples
        decay_end = decay_start + decay_samples
        envelope[decay_start:decay_end] = np.linspace(1, sustain, decay_samples)

    # Sustain phase
    sustain_start = attack_samples + decay_samples
    sustain_end = sustain_start + sustain_samples
    envelope[sustain_start:sustain_end] = sustain

    # Release phase
    release_start = sustain_end
    release_end = release_start + release_samples
    if release_samples > 0:
        envelope[release_start:release_end] = np.linspace(sustain, 0, release_samples)

    # Clip to ensure envelope length matches wave
    envelope = envelope[:total_samples]
    return wave * envelope

# Apply distortion effect
def apply_distortion(wave, distortion_amount):
    wave = np.clip(wave, -distortion_amount, distortion_amount)
    return wave

# Apply reverb effect
def apply_reverb(wave, reverb_amount):
    reverb_signal = np.zeros_like(wave)
    decay = int(0.01 * sample_rate)  # 10ms decay
    for i in range(len(wave)):
        reverb_signal[i] = wave[i]
        if i >= decay:
            reverb_signal[i] += reverb_amount * reverb_signal[i - decay]
    return reverb_signal

# Normalize waveform
def normalize_wave(wave):
    return np.clip(wave, -1.0, 1.0)

# Process wave
def process_wave(wave):
    global distortion_amount, reverb_amount
    wave = apply_distortion(wave, distortion_amount)
    wave = apply_reverb(wave, reverb_amount)
    wave = normalize_wave(wave)
    return wave

# Visualization
fig, ax = plt.subplots()
ax.set_title("Waveform Visualization")
ax.set_xlabel("Time (samples)")
ax.set_ylabel("Amplitude")

def update_visualization(wave):
    ax.clear()
    ax.plot(wave[:1000])  # Show first 1000 samples
    ax.set_ylim(-1.0, 1.0)
    canvas.draw()

# GUI Controls for ADSR
def set_attack(value):
    global attack
    attack = float(value)

def set_decay(value):
    global decay
    decay = float(value)

def set_sustain(value):
    global sustain
    sustain = float(value)

def set_release(value):
    global release
    release = float(value)

# Tkinter GUI
root = tk.Tk()
root.title("Synthesizer with Piano Keyboard and ADSR")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

top_frame = ttk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

# Waveform Selection
waveform = tk.StringVar(top_frame, "sine")
wave_label = ttk.Label(top_frame, text="Waveform:")
wave_label.pack(side=tk.LEFT, padx=5)
for wf in ["sine", "square", "saw", "triangle"]:
    wave_button = ttk.Radiobutton(
        top_frame, text=wf.capitalize(), value=wf, variable=waveform
    )
    wave_button.pack(side=tk.LEFT, padx=5)

# ADSR sliders
ttk.Label(top_frame, text="Attack").pack(side=tk.LEFT, padx=5)
attack_slider = ttk.Scale(top_frame, from_=0.01, to=1.0, orient=tk.HORIZONTAL, command=set_attack)
attack_slider.set(attack)
attack_slider.pack(side=tk.LEFT, padx=5)

ttk.Label(top_frame, text="Decay").pack(side=tk.LEFT, padx=5)
decay_slider = ttk.Scale(top_frame, from_=0.01, to=1.0, orient=tk.HORIZONTAL, command=set_decay)
decay_slider.set(decay)
decay_slider.pack(side=tk.LEFT, padx=5)

ttk.Label(top_frame, text="Sustain").pack(side=tk.LEFT, padx=5)
sustain_slider = ttk.Scale(top_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=set_sustain)
sustain_slider.set(sustain)
sustain_slider.pack(side=tk.LEFT, padx=5)

ttk.Label(top_frame, text="Release").pack(side=tk.LEFT, padx=5)
release_slider = ttk.Scale(top_frame, from_=0.01, to=1.0, orient=tk.HORIZONTAL, command=set_release)
release_slider.set(release)
release_slider.pack(side=tk.LEFT, padx=5)

# Piano Keys with ADSR
keyboard_frame = tk.Frame(root)
keyboard_frame.pack(side=tk.BOTTOM, pady=10)

def play_wave(freq, key_press_duration=0.5):
    selected_waveform = waveform.get()
    print(f"Playing wave: {selected_waveform}, Frequency: {freq}")
    wave = generate_wave(freq, duration=(key_press_duration + release), waveform=selected_waveform)
    wave = apply_adsr(wave, key_press_duration, attack, decay, sustain, release)
    wave = volume * amplifier_gain * process_wave(wave)
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(wave.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error playing sound: {e}")
    update_visualization(wave)

# Create white and black keys
def create_piano_keys(frame):
    white_notes = [("C", 261.63), ("D", 293.66), ("E", 329.63), ("F", 349.23),
                   ("G", 392.00), ("A", 440.00), ("B", 493.88)]
    black_notes = [("C#", 277.18), ("D#", 311.13), None, ("F#", 369.99), ("G#", 415.30), ("A#", 466.16)]

    for i, (note, freq) in enumerate(white_notes):
        key = tk.Button(frame, text=note, width=5, height=15, bg="white", relief="raised",
                        command=lambda f=freq: play_wave(f))
        key.grid(row=0, column=i, padx=1, pady=10)

    for i, note_data in enumerate(black_notes):
        if note_data:
            note, freq = note_data
            key = tk.Button(frame, text=note, width=3, height=8, bg="black", fg="white", relief="raised",
                            command=lambda f=freq: play_wave(f))
            key.place(x=30 + (i * 50), y=10)

create_piano_keys(keyboard_frame)

root.mainloop()

p.terminate()
