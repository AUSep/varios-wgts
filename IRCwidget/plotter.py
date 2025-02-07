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
            wave_array, samp_rate, n_frames = data
        max_len = n_frames if max_len<n_frames else max_len
        f_array, spect_array = get_spect_data(wave_array, samp_rate)
        w_arrays.append(wave_array)
        s_arrays.append(spect_array)
    t_array = np.linspace(0, max_len/samp_rate, max_len)
    w_arrays = [resize_array(array, max_len) for array in w_arrays]
    fig ,(ax0,ax1) = plt.subplots(2,1)
    ax1.set_xscale('log')
    i=0
    for wave_array in w_arrays:
        i=+1
        ax0.plot(t_array, wave_array, label = f"audio {i}")
        ax0.legend(shadow = True, fancybox=True)
    i=0
    for spect_array in s_arrays:
        i=+1
        ax1.plot(f_array, spect_array, label = f"audio {i}")
        ax1.legend(shadow = True, fancybox=True)
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
    spect_array = np.abs(np.fft.fft(wave_array, 22000))
    return f_array, spect_array

t1 = np.linspace(0,1,44100)
x1 = 3*np.sin(2*np.pi*50*t1)
x2 = 1.5*np.sin(2*np.pi*20*t1) 
audio_data1=(x1,44100,44100)
audio_data2=(x2,44100,44100)
plot_audio_data(audio_data1,audio_data2)