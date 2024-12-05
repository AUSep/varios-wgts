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
    time: np.ndarray | int = 0
    freqs: np.ndarray | int = 0
    wf_arrays = [data['wave_form'] for data in plot_data]
    spectrum = [data['spectrum'] for data in plot_data]
    for data in plot data:
        if len(data['seconds']) > len(time):
            time = data['seconds']
        if let()
        
def largest_arrays(*dicts : dict[str : np.ndarrary]) -> dict:
    d_max={}
    for d in dicts:
        for k in d.keys():
            if k not in d_max or d_max[k] < d[k]:
                d_max[k] = d[k]
    return d_max


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
