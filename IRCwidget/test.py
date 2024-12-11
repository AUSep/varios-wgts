import wave
import numpy as np
import matplotlib.pyplot as plt
import random

def get_dtype(wf : wave.Wave_read) -> np.signedinteger:
    samp_width = wf.getsampwidth()
    if samp_width == 1:
        dtype = np.int8
    elif samp_width == 2:
        dtype = np.int16
    elif samp_width == 4:
        dtype = np.int32
    return dtype

def signal_plot_data(file_dir : str) -> dict[np.ndarray]:
    with wave.open(file_dir, 'rb') as wf:
        channels = wf.getnchannels()
        samp_rate = wf.getframerate()
        samples = wf.getnframes()
        dtype = get_dtype(wf)
        time: np.ndarray = np.arange(samples)/samp_rate
        freqs=np.fft.fftfreq(n=samples, d=1/samp_rate)
        if channels == 1:
            audio_data : bytes = wf.readframes(samples)
            wf_array : np.ndarray = np.frombuffer(audio_data, dtype)
            fft_data=np.fft.fft(wf_array)
            spectrum=np.abs(fft_data)
            freqs=np.fft.fftfreq(n=samples, d=1/samp_rate)
            audio_data_dict : dict = {'wave_form' : wf_array, 
                                      'seconds' : time, 
                                      'spectrum' : spectrum,
                                      'frequence' : freqs}
            return audio_data_dict
        else:
            raise Exception('The audio file should be mono')

def mult_plot_data(*plot_data: dict[str : np.ndarray]) -> dict[np.ndarray]:
    w_arrays: list[np.ndarray] = []
    t_arrays: list[np.ndarray] = []
    s_arrays: list[np.ndarray] = []
    f_arrays: list[np.ndarray] = []
    for data in plot_data:
        for k in data:
            if k == 'wave_form':
                w_arrays.append(data[k])
            elif k == 'seconds':
                t_arrays.append(data[k])
            elif k == 'spectrum':
                s_arrays.append(data[k])
            elif k == 'frequence':
                f_arrays.append(data[k])
    mult_plot_d = {'wave_form' : tuple(w_arrays),
                    'seconds' : tuple(t_arrays),
                    'spectrum' : tuple(s_arrays),
                    'frequence' : tuple(f_arrays)}
    mult_plot_d = format_data_d(mult_plot_d)
    return mult_plot_data

def format_data_d(data_d: dict[str : np.ndarray]) -> dict:
    for k in data_d:
        if data_d[k] == 'seconds' or data_d[k] == 'frequence':
            arr = max(data_d[k])
            data_d[k] = arr
    t_size = len(data_d['seconds'])
    f_size = len(data_d['frequence'])
    data_d['wave_form'] = resize_arrays(data_d['wave_form'], size = t_size)
    data_d['spectrum'] = resize_arrays(data_d['spectrum'], size = f_size)
    return data_d

def resize_arrays(array: np.ndarray, size : int) -> tuple:
    _array = array[0]
    dif = size - len(_array)
    z_arr = np.array([0]*dif)
    _array = np.concatenate([_array,z_arr])
    return array

def get_random_colour() -> tuple:
    cmap = plt.cm.get_cmap('viridis', 20)
    colour=cmap(random.randint(0, 19))
    return colour
    
def print_comp_graph(arr_dict: dict) -> None:
    t_array = arr_dict['seconds']
    f_array = arr_dict['frequence']
    for arr in arr_dict['wave_form']:
        plt.plot(t_array, arr, get_random_colour())
    for arr in arr_dict['spectrum']:
        plt.plot(f_array, arr, get_random_colour())
    plt.show()
        
audio_data = signal_plot_data('IRCwidget/100.wav')
audio_data_2 = signal_plot_data('IRCwidget/100.wav')
comp_data = mult_plot_data(audio_data, audio_data_2)
print_comp_graph(comp_data)

