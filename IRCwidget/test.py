import wave
import numpy as np
import matplotlib.pyplot as plt

def signal_data(file_dir : str, label: str) -> dict:
    with wave.open(file_dir, 'rb') as wf:
        channels = wf.getnchannels()
        if channels == 1:
            samp_rate = wf.getframerate()
            samples = wf.getnframes()
            dtype = get_dtype(wf)
            time = np.arange(samples)/samp_rate
            freqs = np.fft.fftfreq(n=samples, d=1/samp_rate)
            audio_data = wf.readframes(samples)
            wf_array  = np.frombuffer(audio_data, dtype)
            fft_data=np.fft.fft(wf_array)
            spectrum=np.abs(fft_data)
            audio_data_dict : dict = {'wave_form' : (wf_array.tolist(),label),
                                      'spectrum' : (spectrum.tolist(),label),
                                      'time' : time.tolist(),
                                      'frequence' : freqs.tolist()}
            return audio_data_dict
        else:
            raise Exception('The audio file should be mono')
        
def plot_data(*data_d : dict) -> None:
    w_arr = [data['wave_form'] for data in data_d]
    s_arr = [data['spectrum'] for data in data_d]
    t_arr = max([data['time'] for data in data_d])
    f_arr = max([data['frequence'] for data in data_d])
    for w in w_arr:
        arr = resize_arrays(w[0], len(t_arr))
        label = w[1]
        plt.plot(t_arr, arr, label = label)
    plt.legend()
    plt.show()
    for s in s_arr:
        arr = resize_arrays(s[0], len(f_arr))
        label = s[1]
        plt.plot(f_arr, arr, label = label)
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
    elif len(array) > size:
        array = array[:size]
    return array

def binary_to_db(array: np.ndarray, dtype:np.signedinteger) -> list:
    if dtype == np.int16:
        n=16
    elif dtype == np.int32:
        n=32
    db_array=[]
    for v in array:
        v = 20*np.log10(np.abs(v)/2**(n-1))
        db_array.append(v)
    return db_array
audio_data = signal_data('varios_widgets/IRCwidget/gtr_test.wav', 'guitarra')
audio_data_2 = signal_data('varios_widgets/IRCwidget/Bajo_test.wav', 'bajo')
plot_data(audio_data, audio_data_2)