import numpy as np
from scipy.signal import find_peaks
from plotter import plot_audio_data, get_spect_data

sample_rate = 44100

t = np.linspace(0,5,sample_rate, dtype=np.float32)
x1 = 0.9*np.sin(2*np.pi*20*t)
x2 = 0.2*np.sin(2*np.pi*100*t)
x3 = 0.5*np.sin(2*np.pi*50*t)
g = x1 + x2 + x3
audio_data = (g,sample_rate,sample_rate)

def track_harmonics(signal : np.ndarray, s_rate: int, n = int) -> np.ndarray:
    f_array, spect_array = get_spect_data(signal, s_rate)
    print(f_array)
    peak_indxs, prop = find_peaks(spect_array, height=0.1)
    peak_hght = prop['peak_heights']
    peak_dict = dict(zip(peak_hght, peak_indxs))
    i = 0
    indxs = []
    while i<n:
        max_peak = max(peak_dict)
        max_indx = int(peak_dict.pop(max_peak))
        indxs.append(max_indx)
        i+=1
    print(indxs)
    peak_freqs = [f_array[i] for i in indxs]
    return peak_freqs

print(track_harmonics(g, sample_rate, 3))
