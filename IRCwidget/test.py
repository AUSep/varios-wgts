import wave
import numpy as np
import matplotlib.pyplot as plt

def get_array_dict(file_dir : str) -> dict[np.ndarray]:
    with wave.open(file_dir, 'rb') as wf:
        channels = wf.getnchannels()
        samp_rate = wf.getframerate()
        samples = wf.getnframes()
        dtype = get_dtype(wf)
        if channels == 1:
            audio_data : bytes = wf.readframes(samples)
            wf_array : np.ndarray = np.frombuffer(audio_data, dtype)
            time: np.ndarray = np.arange(samples)/samp_rate
            fft_data=np.fft.fft(wf_array)
            spectrum=np.abs(fft_data)
            freqs=np.fft.fftfreq(n=samples, d=1/samp_rate)
            audio_data_dict : dict = {'wave_form' : wf_array, 
                                      'seconds' : time, 
                                      'spectrum' : spectrum,
                                      'frequence' : freqs}
            return audio_data_dict

def get_dtype(wf : wave.Wave_read) -> np.signedinteger:
    samp_width = wf.getsampwidth()
    if samp_width == 1:
        dtype = np.int8
    elif samp_width == 2:
        dtype = np.int16
    elif samp_width == 4:
        dtype = np.int32
    return dtype

def print_comp_graph(*arrays_dicts: dict[str : np.ndarray]) -> None:
    for array in arrays_dicts:
        fig, (wf_ax, spect_ax) = plt.subplots(2)
        wf_ax.plot(array['seconds'], array['wave_form'])
        wf_ax.set(xlabel='Tiempo', ylabel='Amplitud')
        spect_ax.plot(array['frequence'], array['spectrum'])
        spect_ax.set(xlabel='Frecuencias', ylabel='Amplitud')
        plt.show()
  
audio_data = get_array_dict('IRCwidget/100.wav')
print_comp_graph(audio_data)
