import wave
import numpy as np
import matplotlib.pyplot as plt
import random

def signal_data(file_dir : str, label: str) -> dict:
    with wave.open(file_dir, 'rb') as wf:
        channels = wf.getnchannels()
        if channels == 1:
            samp_rate = wf.getframerate()
            samples = wf.getnframes()
            dtype = get_dtype(wf)
            time = np.arange(samples)/samp_rate
            freqs = np.fft.fftfreq(n=samples, d=1/samp_rate)
            audio_data : bytes = wf.readframes(samples)
            wf_array : np.ndarray = np.frombuffer(audio_data, dtype)
            fft_data=np.fft.fft(wf_array)
            spectrum=np.abs(fft_data)
            colour = get_random_colour()
            audio_data_dict : dict = {'wave_form' : (wf_array.tolist(),label, colour),
                                      'spectrum' : (spectrum.tolist(),label, colour),
                                      'time' : time.tolist(),
                                      'frequence' : freqs.tolist()}
            return audio_data_dict
        else:
            raise Exception('The audio file should be mono')
        
def plot_data(*data_d : dict) -> None:
    w_arr = [data['wave_form'] for data in data_d]
    s_arr = [data['spectrum'] for data in data_d]
    t_arr = [data['time'] for data in data_d]
    t_arr = max(t_arr)
    f_arr = [data['frequence'] for data in data_d]
    f_arr = max(f_arr)
    for w in w_arr:
        arr = resize_arrays(w[0], len(t_arr))
        label = w[1]
        colour = w[2]
        plt.plot(t_arr, arr, colour, label = label)
        plt.legend()
    plt.show()
    for s in s_arr:
        arr = resize_arrays(s[0], len(f_arr))
        label = s[1]
        colour = s[2]
        plt.plot(f_arr, arr, colour, label = label)
        plt.legend()
    plt.show()
        
def get_dtype(wf : wave.Wave_read) -> np.signedinteger:
    samp_width = wf.getsampwidth()
    if samp_width == 1:
        dtype = np.int8
    elif samp_width == 2:
        dtype = np.int16
    elif samp_width == 4:
        dtype = np.int32
    return dtype

def resize_arrays(array: list, size: int) -> list:
    if len(array) < size:
        dif = size - len(array)
        z_arr = [0] * dif
        array.extend(z_arr)
    if len(array) > size:
        array = array[:size]
    return array

def get_random_colour() -> tuple:
    cmap = plt.colormaps.get_cmap('viridis')
    colour=cmap(random.randint(0, 19))
    return colour

audio_data = signal_data('IRCwidget/100.wav', 'pure 100')
audio_data_2 = signal_data('IRCwidget/test.wav', 'sweep')
plot_data(audio_data, audio_data_2)