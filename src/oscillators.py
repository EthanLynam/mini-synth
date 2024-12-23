import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from scipy.fft import fft, fftfreq
import csv

# Initial parameters
initial_frequency = 5  # Initial frequency in Hz
initial_duration = 2    # Initial duration in seconds
initial_sampling_rate = 1000  # Initial sampling rate in samples/second
initial_custom_wave_expression = "np.sin(2 * np.pi * frequency * time) + 0.5 * np.sin(4 * np.pi * frequency * time)"

# Create the figure and axes for plotting
fig, ax = plt.subplots(5, 1, figsize=(12, 12))  # Add one more subplot for custom wave
plt.subplots_adjust(left=0.1, bottom=0.4)  # Leave space for sliders and buttons

# Initialize time array and waves
def generate_waves(frequency, duration, sampling_rate):
    time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * time)
    square_wave = np.sign(sine_wave)
    sawtooth_wave = 2 * (time * frequency - np.floor(time * frequency + 0.5))
    triangle_wave = 2 * np.abs(2 * (time * frequency % 1) - 1) - 1
    return time, sine_wave, square_wave, sawtooth_wave, triangle_wave

# Plot initial waves
time, sine_wave, square_wave, sawtooth_wave, triangle_wave = generate_waves(
    initial_frequency, initial_duration, initial_sampling_rate)

wave_axes = [
    (ax[0], sine_wave, "Sine Wave", "blue"),
    (ax[1], square_wave, "Square Wave", "green"),
    (ax[2], sawtooth_wave, "Sawtooth Wave", "orange"),
    (ax[3], triangle_wave, "Triangle Wave", "purple"),
    (ax[4], None, "Custom Wave", "red")  # Placeholder for custom wave
]

for axis, wave, title, color in wave_axes[:-1]:
    axis.plot(time, wave, color=color, lw=1.5)
    axis.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axis.set_title(title)
    axis.grid(True, linestyle='--', alpha=0.6)
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Amplitude")

# Add sliders
ax_freq = plt.axes([0.1, 0.3, 0.8, 0.03], facecolor="lightgray")
ax_duration = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgray")
ax_sampling = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor="lightgray")

slider_freq = Slider(ax_freq, "Frequency (Hz)", 1, 50, valinit=initial_frequency, valstep=1)
slider_duration = Slider(ax_duration, "Duration (s)", 0.5, 5, valinit=initial_duration, valstep=0.1)
slider_sampling = Slider(ax_sampling, "Sampling Rate (Hz)", 100, 5000, valinit=initial_sampling_rate, valstep=100)

# Add text box for custom wave
ax_text = plt.axes([0.1, 0.1, 0.8, 0.05])
textbox = TextBox(ax_text, "Custom Wave (expression):", initial=initial_custom_wave_expression)

# Function to evaluate custom wave
def evaluate_custom_wave(time, frequency, expression):
    try:
        custom_wave = eval(expression)
        return custom_wave
    except Exception as e:
        print(f"Error in custom wave expression: {e}")
        return np.zeros_like(time)

# Update function
def update(val):
    frequency = slider_freq.val
    duration = slider_duration.val
    sampling_rate = slider_sampling.val
    time, sine_wave, square_wave, sawtooth_wave, triangle_wave = generate_waves(
        frequency, duration, sampling_rate)
    custom_expression = textbox.text
    custom = evaluate_custom_wave(time, frequency, custom_expression)

    # Update waveform plots
    updated_waves = [
        sine_wave, square_wave, sawtooth_wave, triangle_wave, custom
    ]
    for (axis, _, title, color), updated_wave in zip(wave_axes, updated_waves):
        axis.clear()
        axis.plot(time, updated_wave, color=color, lw=1.5)
        axis.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        axis.set_title(title)
        axis.set_xlabel("Time (s)")
        axis.set_ylabel("Amplitude")
        axis.grid(True, linestyle='--', alpha=0.6)

    fig.canvas.draw_idle()

# Connect sliders and text box to update function
slider_freq.on_changed(update)
slider_duration.on_changed(update)
slider_sampling.on_changed(update)
textbox.on_submit(update)

# Save to CSV function
def save_csv(event):
    frequency = slider_freq.val
    duration = slider_duration.val
    sampling_rate = slider_sampling.val
    time, sine_wave, square_wave, sawtooth_wave, triangle_wave = generate_waves(
        frequency, duration, sampling_rate)
    custom_expression = textbox.text
    custom = evaluate_custom_wave(time, frequency, custom_expression)
    with open("waveforms.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Sine", "Square", "Sawtooth", "Triangle", "Custom"])
        for i in range(0, len(time), 10):  # Save every 10th sample
            writer.writerow([time[i], sine_wave[i], square_wave[i], sawtooth_wave[i], triangle_wave[i], custom[i]])
    print("Waveforms saved as 'waveforms.csv'.")

# Add Save button
ax_save = plt.axes([0.1, 0.02, 0.15, 0.04])
button_save = Button(ax_save, 'Save to CSV', color='lightgray', hovercolor='gray')
button_save.on_clicked(save_csv)

plt.show()
