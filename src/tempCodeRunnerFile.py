
plt.plot(time, sine_wave, color='blue', linewidth=1.5, label="Sine Wave")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Add a zero line
plt.title(f"Sine Wave Oscillator - Frequency: {frequency} Hz", fontsize=14)