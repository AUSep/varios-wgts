import numpy as np
from plotter import plot_audio_data, get_spect_data

sample_rate = 44100

t = np.linspace(0,5,sample_rate, dtype=np.float32)
x1 = 0.9*np.sin(2*np.pi*20*t)
x2 = 0.2*np.sin(2*np.pi*100*t)
x3 = 0.5*np.sin(2*np.pi*50*t)
g = x1 + x2 + x3
audio_data = (g,sample_rate,sample_rate)

def track_harmonics(signal : np.ndarray, s_rate: int, n = int) -> np.ndarray:
    f_array, spect_array = get_spect_data(signal, s_rate/2)
    h_min_val = np.sort(spect_array, kind='mergesort')[len(spect_array)-n]
    mx_val = [val for val in spect_array if val>h_min_val]
    print(mx_val)
    paired_data = np.column_stack((f_array, spect_array))
    f_h = [fila[1] for fila in paired_data if fila[0] > h_min_val]
    f_h = np.array(f_h)
    return f_h

print(track_harmonics(g, sample_rate, 3))





    

