import wave
import numpy as np
import matplotlib.pyplot as plt

def get_audio_data(file_dir : str) -> tuple:
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
            print(samples)
            print(samp_rate)
            print(len(freqs))
            return (wf_array, time, spectrum, freqs)

def get_dtype(wf : wave.Wave_read) -> np.signedinteger:
    samp_width = wf.getsampwidth()
    if samp_width == 1:
        dtype = np.int8
    elif samp_width == 2:
        dtype = np.int16
    elif samp_width == 4:
        dtype = np.int32
    return dtype
        
def plot_wf(wf : np.ndarray, time : np.ndarray) -> None: 
    plt.plot(time, wf)
    plt.xlabel('tiempo')
    plt.ylabel('amplitud')
    plt.title('Waveform')
    plt.show()

def plot_spectrum(spectrum : np.ndarray, freqs:np.ndarray) -> None:
    plt.plot(freqs, spectrum)
    plt.xlabel('frecuencias')
    plt.ylabel('amplitud')
    plt.title('Espectro de frecuencias')
    plt.show()

audio_data = get_audio_data('varios_widgets/IRCwidget/100.wav')
plot_wf(audio_data[0],audio_data[1])
plot_spectrum(audio_data[2],audio_data[3])