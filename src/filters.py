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
num_samples = 44100
distortion_amount = 1.2
reverb_amount = 0.0

attack_amount = 0.0
decay_amount = 0.0
sustain_amount = 0.0
release_amount = 0.5
total_duration = 0.5


# Function to generate waveforms
def generate_wave(freq, duration = total_duration, waveform="sine"):
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












# Apply attack effect

def apply_ADSR(wave, attack_amount, decay_amount, sustain_amount, release_amount):
    global total_duration

    total_samples = len(wave)
    attack_samples = int((attack_amount / total_duration) * total_samples)
    decay_samples = int((decay_amount / total_duration) * total_samples)
    sustain_samples = int(((total_duration - attack_amount - decay_amount - release_amount) / total_duration) * total_samples)
    release_samples = int((release_amount / total_duration) * total_samples)

    envelope = np.zeros(total_samples)

    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    if decay_samples > 0:
        decay_start = attack_samples
        decay_end = decay_start + decay_samples
        envelope[decay_start:decay_end] = np.linspace(1, sustain_amount, decay_samples)

    if sustain_samples > 0:
        sustain_start = attack_samples + decay_samples
        sustain_end = sustain_start + sustain_samples
        envelope[sustain_start:sustain_end] = sustain_amount

    if release_samples > 0:
        release_start = attack_samples + decay_samples + sustain_samples
        release_end = release_start + release_samples
        envelope[release_start:release_end] = np.linspace(sustain_amount, 0, release_samples)

    wave = wave[:total_samples] * envelope
    return wave


# Apply distortion effect
def apply_distortion(wave, distortion_amount):
    wave = np.clip(wave, -distortion_amount, distortion_amount)
    return wave

# Apply reverb effect
def apply_reverb(wave, reverb_amount):
    reverb_signal = np.zeros_like(wave)
    decay = int(0.01 * sample_rate)
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
    global distortion_amount, reverb_amount, attack_amount, decay_amount, release_amount, sustain_amount
    
    wave = apply_ADSR(wave, attack_amount,decay_amount,release_amount,sustain_amount)
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
    ax.plot(wave[:num_samples])
    ax.set_ylim(-1.0, 1.0)
    canvas.draw()




# GUI Controls
def set_volume(value):
    global volume
    volume = float(value)

def set_amplifier_gain(value):
    global amplifier_gain
    amplifier_gain = float(value)

def set_distortion_amount(value):
    global distortion_amount
    distortion_amount = float(value)

def set_reverb_amount(value):
    global reverb_amount
    reverb_amount = float(value)

def set_num_samples(value):
    global num_samples
    num_samples = value

def set_attack(value):
    global attack_amount, total_duration
    attack_amount = float(value)
    total_duration = attack_amount + decay_amount + sustain_amount + release_amount

def set_decay(value):
    global decay_amount, total_duration
    decay_amount = float(value)
    total_duration = attack_amount + decay_amount + sustain_amount + release_amount

def set_sustain(value):
    global sustain_amount, total_duration
    sustain_amount = float(value)
    total_duration = attack_amount + decay_amount + sustain_amount + release_amount

def set_release(value):
    global release_amount, total_duration
    release_amount = float(value)
    total_duration = attack_amount + decay_amount + sustain_amount + release_amount



# Tkinter GUI
root = tk.Tk()
root.title("Synthesizer with Piano Keyboard")

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

# Volume Slider
vol_label = ttk.Label(top_frame, text="Volume:")
vol_label.pack(side=tk.LEFT, padx=5)
vol_slider = ttk.Scale(top_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=set_volume)
vol_slider.set(volume)
vol_slider.pack(side=tk.LEFT, padx=5)

# Amplifier Gain Slider
amp_label = ttk.Label(top_frame, text="Amplifier Gain:")
amp_label.pack(side=tk.LEFT, padx=5)
amp_slider = ttk.Scale(top_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, command=set_amplifier_gain)
amp_slider.set(amplifier_gain)
amp_slider.pack(side=tk.LEFT, padx=5)

# Distortion Slider
distortion_label = ttk.Label(top_frame, text="Distortion:")
distortion_label.pack(side=tk.LEFT, padx=5)
distortion_slider = ttk.Scale(top_frame, from_=1.2, to=0.1, orient=tk.HORIZONTAL, command=set_distortion_amount)
distortion_slider.set(distortion_amount)
distortion_slider.pack(side=tk.LEFT, padx=5)

# Reverb Slider
reverb_label = ttk.Label(top_frame, text="Reverb:")
reverb_label.pack(side=tk.LEFT, padx=5)
reverb_slider = ttk.Scale(top_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=set_reverb_amount)
reverb_slider.set(reverb_amount)
reverb_slider.pack(side=tk.LEFT, padx=5)

# Attack Slider

ttk.Label(top_frame, text="Attack").pack(side=tk.LEFT, padx=5)
attack_slider = ttk.Scale(top_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=set_attack)
attack_slider.set(attack_amount)
attack_slider.pack(side=tk.LEFT, padx=5)

# Decay Slider

ttk.Label(top_frame, text="Decay").pack(side=tk.LEFT, padx=5)
decay_slider = ttk.Scale(top_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=set_decay)
decay_slider.set(decay_amount)
decay_slider.pack(side=tk.LEFT, padx=5)

# Release Slider

ttk.Label(top_frame, text="Release").pack(side=tk.LEFT, padx=5)
release_slider = ttk.Scale(top_frame, from_=0.0, to=2.0, orient=tk.HORIZONTAL, command=set_release)
release_slider.set(release_amount)
release_slider.pack(side=tk.LEFT, padx=5)

# Sustain Slider

ttk.Label(top_frame, text="Sustain").pack(side=tk.LEFT, padx=5)
sustain_slider = ttk.Scale(top_frame, from_=0., to=1.0, orient=tk.HORIZONTAL, command=set_sustain)
sustain_slider.set(sustain_amount)
sustain_slider.pack(side=tk.LEFT, padx=5)



# Samples Slisdr
ttk.Label(top_frame, text="Samples").pack(side=tk.LEFT, padx=5)
samples_slider = ttk.Scale(top_frame, from_=100, to=44100, orient=tk.HORIZONTAL, command=lambda v: set_num_samples(int(float(v))))
samples_slider.set(num_samples)
samples_slider.pack(side=tk.LEFT, padx=5)





# Piano Keys with a Piano-Like Appearance
def create_piano_keys(frame):
    white_notes = [("C", 261.63), ("D", 293.66), ("E", 329.63), ("F", 349.23),
                   ("G", 392.00), ("A", 440.00), ("B", 493.88)]
    black_notes = [("C#", 277.18), ("D#", 311.13), None, ("F#", 369.99), ("G#", 415.30), ("A#", 466.16)]

    white_keys = []
    black_keys = []

    for i, (note, freq) in enumerate(white_notes):
        key = tk.Button(frame, text=note, width=5, height=15, bg="white", relief="raised",
                        command=lambda f=freq: play_wave(f))
        key.grid(row=0, column=i, padx=1, pady=10)
        white_keys.append(key)

    for i, note_data in enumerate(black_notes):
        if note_data:
            note, freq = note_data
            key = tk.Button(frame, text=note, width=3, height=8, bg="black", fg="white", relief="raised",
                            command=lambda f=freq: play_wave(f))
            key.place(x=30 + (i * 50), y=10)
            black_keys.append(key)

keyboard_frame = tk.Frame(root)
keyboard_frame.pack(side=tk.BOTTOM, pady=10)

create_piano_keys(keyboard_frame)








# Play Wave Function
def play_wave(freq):
    global attack_amount, decay_amount, sustain_amount, release_amount, total_duration
    selected_waveform = waveform.get()
    wave = generate_wave(freq, duration=total_duration, waveform=selected_waveform)
    wave = wave / np.max(np.abs(wave))
    wave = process_wave(wave)
    wave = wave * volume * amplifier_gain
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(wave.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error playing sound: {e}")
    update_visualization(wave)

root.mainloop()

p.terminate()
