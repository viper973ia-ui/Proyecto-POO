import numpy as np, matplotlib.pyplot as plt
from scipy import signal

fs = 1000
t = np.arange(0, 6, 1/fs)
chirp = signal.chirp(t, f0=5, f1=200, t1=6, method="quadratic")
f, tt, Sxx = signal.spectrogram(chirp, fs=fs, nperseg=256, noverlap=224)

fig, ax = plt.subplots(figsize=(8, 4.5))
m = ax.pcolormesh(tt, f, 10*np.log10(Sxx + 1e-12), shading="gouraud", cmap="magma")
ax.set(xlabel="Tiempo (s)", ylabel="Frecuencia (Hz)", ylim=(0, 300))
fig.colorbar(m, label="dB"); plt.show()