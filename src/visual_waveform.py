import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualise_waveform(waveform, frequency, sample_rate, cycles=1):
    # Calculate the duration of one cycle
    cycle_samples = int(sample_rate / frequency)
    display_window_samples = 250  # Display this many samples
    
    # Time axis for the display window
    time_axis = np.linspace(0, cycles / frequency * 1000, num=display_window_samples)  # In milliseconds

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 4))
    line, = ax.plot([], [], color='cyan', linewidth=1.5)
    ax.set_xlim(0, time_axis[-1])  # Limit x-axis to the time of the displayed cycles
    ax.set_ylim(-1.1, 1.1)  # Normalized amplitude
    ax.set_title("Waveform Visualization")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude")
    ax.grid(True)

    # Animation update function
    def update(frame):
        start = (frame * (cycle_samples // 4)) % len(waveform)
        end = start + display_window_samples
        if end > len(waveform):
            visible_waveform = np.concatenate((waveform[start:], waveform[:end - len(waveform)]))
        else:
            visible_waveform = waveform[start:end]
        line.set_data(time_axis, visible_waveform)
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=range(len(waveform) // (cycle_samples // 4)),
        interval=50, blit=True, repeat=True
    )

    plt.tight_layout()
    plt.show()
