import wave
import numpy as np
import matplotlib.pyplot as plt

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
    x = []
    y = []
    for data in plot_data:
        d_x = {k:v for (k,v) in data if k == 'seconds' or k== 'frequence'}
        d_y = {k:v for (k,v) in data if k== 'wave_form' or k='spectrum'}
        x.append(d_X)
        y.append(d_y)
        
def largest_arrays(*dicts : dict[str : np.ndarrary]) -> dict:
    d_max={}
    for d in dicts:
        for k in d.keys():
            if k not in d_max or d_max[k] < d[k]:
                d_max[k] = d[k]
    return d_max

def normalize_arrays(*arr_d:dict[np.ndarray*]) -> dict[np.ndarray]:
    waves_list = []
    spect_list = []
    for arrays in arr_d:
        for arr in array:
            if arr == 'wave_form':
                wave_list.append(arr)
            elif arr == 'spectrum':
                spect_list.append(arr)
    waves_size= len(max(waves_list))
    waves_size= len(max(waves_list))

    lengths = [len(array) for array in arrays]
    len_arr = max(lengths)
    complete_arrays = []
    for array in arrays:
        dif = len_array - len(array)
        z_arr = np.array([0]*dif)
        new_arr = np.concatenate([array,z_array])
        complete_arrays.append(new_arr)
        
    return new_arr
    
def print_comp_graph(*arrays_dicts: dict[str : np.ndarray | list]) -> None:
    for array in arrays_dicts:
        fig, (wf_ax, spect_ax) = plt.subplots(2)
        wf_ax.plot(array['seconds'], array['wave_form'])
        wf_ax.set(xlabel='Tiempo', ylabel='Amplitud')
        spect_ax.plot(array['frequence'], array['spectrum'])
        spect_ax.set(xlabel='Frecuencias', ylabel='Amplitud')
        plt.show()
  
audio_data = get_array_dict('IRCwidget/100.wav')
print_comp_graph(audio_data)
