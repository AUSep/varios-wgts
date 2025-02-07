import pyaudio as pa
import matplotlib.pyplot as plt
import numpy as np
import wave

def plot_audio_data(*audio_data : str | tuple[np.ndarray, int, int]) -> None:
    max_len = 0
    w_arrays = []
    s_arrays = []
    for data in audio_data:
        if type(data) == str:
            wave_array, samp_rate, n_frames = get_wave_data(data)
        elif type(data) == tuple:
            wave_array, samp_rate = audio_data
        max_len = n_frames if max_len<n_frames else max_len
        f_array, spect_array = get_spect_data(wave_array, samp_rate)
        w_arrays.append(wave_array)
        s_arrays.append(spect_array)
    t_array = np.linspace(0, max_len/samp_rate, max_len)
    w_arrays = [resize_array(array, max_len) for array in w_arrays]
    plt.figure() 
    plt.subplot(211)
    i=0
    for wave_array in w_arrays:
        i=+1
        plt.plot(t_array, wave_array)
    i=0
    plt.subplot(212)
    for spect_array in s_arrays:
        i=+1
        plt.plot(f_array, spect_array)
    plt.show()

def get_wave_data(audio_data : str) -> tuple[np.ndarray, int, int]:
    with wave.open(audio_data,'rb') as wf:
        n_frames = wf.getnframes()
        samp_rate = wf.getframerate()
        bit_w = get_dtype(wf.getsampwidth())
        wave_array =np.frombuffer(wf.readframes(n_frames), bit_w)
    return wave_array, samp_rate, n_frames

def get_dtype(bit_w = int) -> np.signedinteger:
    if bit_w == 1:
        dtype = np.int16
    elif bit_w == 3:
        dtype == np.int32
    else:
        raise ValueError('Unsopported bit width')
    return dtype

def resize_array(array : np.ndarray, length : int) -> np.ndarray:
    if len(array)<length:
        array = np.pad(array, (0,length-len(array), 'constant'))
    elif len(array)>length:
        subarrays = np.array_split(array, length)
        array = subarrays[0]
    return array
        
def get_spect_data(wave_array : np.ndarray, samp_rate : int) -> tuple[np.ndarray, np.ndarray]:
    f_array = np.fft.fftfreq(22000, 1/samp_rate)
    spect_array = np.fft.fft(wave_array, 22000)
    return f_array, spect_array