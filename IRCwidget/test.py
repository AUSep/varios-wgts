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

def signal_plot_data(file_dir : str) -> dict[str, list]:
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
            audio_data_dict : dict = {'wave_form' : wf_array.tolist(),
                                      'seconds' : time.tolist(),
                                      'spectrum' : spectrum.tolist(),
                                      'frequence' : freqs.tolist()}
            return audio_data_dict
        else:
            raise Exception('The audio file should be mono')


def mult_plot_data(*plot_data: dict[str, list]) -> dict[str:list]:
    w_arrays: list[list] = []
    t_arrays: list[list] = []
    s_arrays: list[list] = []
    f_arrays: list[list] = []
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
    mult_plot_d = {
        'wave_form': w_arrays,
        'seconds': t_arrays,
        'spectrum': s_arrays,
        'frequence': f_arrays
    }
    mult_plot_d = format_data_d(mult_plot_d)
    return mult_plot_d

def format_data_d(data_d: dict[str, list]) -> dict[str, list]:
    for k in data_d:
        if k == 'seconds':
            arr = max(data_d[k])
            data_d[k] = arr
        elif k == 'frequence':
            arr = max(data_d[k])
            data_d[k] = arr
    t_size = len(data_d['seconds'])
    f_size = len(data_d['frequence'])
    print(f_size)
    w_arrays = [resize_arrays(arr,t_size) for arr in data_d['wave_form']]
    s_arrays = [resize_arrays(arr,f_size) for arr in data_d['spectrum']]
    print(len(s_arrays[0]))
    data_d['wave_form'] = w_arrays
    data_d['spectrum'] = s_arrays
    return data_d


def resize_arrays(array: list, size : int) -> list:
    dif = size - len(array)
    z_arr = [0]*dif
    array.extend(z_arr)
    return array

def get_random_colour() -> tuple:
    cmap = plt.colormaps.get_cmap('viridis')
    colour=cmap(random.randint(0, 19))
    return colour

def print_comp_graph(arr_dict: dict) -> None:
    t_array = arr_dict['seconds']
    f_array = arr_dict['frequence']
    w_array = arr_dict['wave_form']
    s_array = arr_dict['spectrum']
    for arr in w_array:
        plt.plot(t_array, arr, get_random_colour())
    for arr in s_array:
        plt.plot(f_array, arr, get_random_colour())
    plt.show()

audio_data = signal_plot_data('varios_widgets/IRCwidget/100.wav')
audio_data_2 = signal_plot_data('varios_widgets/IRCwidget/test.wav')
comp_data = mult_plot_data(audio_data, audio_data_2)
print_comp_graph(comp_data)