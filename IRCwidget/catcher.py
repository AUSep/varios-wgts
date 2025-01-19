import sys
import pyaudio as pa
import numpy as np
import gevent as gv
import matplotlib.pyplot as plt

from scipy.signal import chirp, butter, sosfilt


class Catchr():
    def __init__(self):
        self.__chunk = 1024
        self.__format = pa.paFloat32
        self.__channels = 1 if sys.platform == 'darwin' else 2
        self.__rate = 44100
        self.__output = pa.PyAudio()
        self.__input = pa.PyAudio()
        self.__delay = None
        
    @property
    def chunk(self) -> int:
        return self.__chunk
    
    @property
    def format(self) -> int:
        return self.__format
    
    @format.setter
    def format(bits : int, float : bool = True):
        pass

    @property
    def channels(self) -> int:
        return self.__channels
    
    @property
    def rate(self) -> int:
        return self.__rate
    
    @property
    def output(self) -> pa.PyAudio:
        return self.__output
    
    @property
    def input(self) -> pa.PyAudio:
        return self.__input
    
    @property
    def delay(self) -> int:
        return self.__delay
    
    def sweep(self, amp = float) -> np.ndarray: 
        t = np.linspace(start=0, num=self.rate*45, stop=30)
        sweep = amp*chirp(t,10,45,22050,'quadratic')
        sos = butter(10, (22000/self.rate), output='sos')
        sweep = sosfilt(sos, sweep)
        sweep = np.array(sweep, dtype=np.float32)
        plt.plot(t, sweep)
        plt.show()
        return sweep
    
    def pulse(self) -> np.ndarray:
        n = 250
        zeros = np.zeros(n)
        ones = np.ones(n)
        pulse = np.concatenate([zeros, ones, zeros])
        pulse.astype(np.float32)
        return pulse
    
    def tone(self, amp = float) -> np.ndarray:
        t=np.linspace(start=0, num=self.rate, stop=1, dtype=np.float32)
        tone =amp*np.sin(2*np.pi*1000*t)
        return tone
    
    def open_port(self, port : pa.PyAudio) -> pa.Stream:
        stream = port.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        output=True if port == self.output else False,
                        input=True if port == self.input else False)
        return stream
            
    def play(self, signal : np.ndarray) -> None:
        o_stream = self.open_port(self.output)
        o_stream.write(signal.tobytes())
        o_stream.close()
        self.output.terminate()
        gv.sleep(1)
    
    def rec(self, len : int) -> np.ndarray:
        i_stream = self.open_port(self.input)
        audio_data = i_stream.read(len)
        audio_data = np.array(audio_data, dtype = np.float32)
        i_stream.close()
        self.input.terminate()
        gv.sleep(1)
        return audio_data
    
    def rms(self, audio_data : np.ndarray) -> float:
        sq_sum = np.square(audio_data)
        rms = np.sqrt(np.mean(sq_sum))
        print(type(rms))
        return rms

    def vol_in(self, stream : pa.Stream) -> float:
        audio_chunk = stream.read(self.chunk)
        audio_data = np.frombuffer(audio_chunk)
        rms = self.rms(audio_data)
        return rms
    
    def get_return_lvl(self, signal : np.ndarray) -> float:
        signal_return = self.get_return(signal)
        return_level =self.rms(signal_return)
        return return_level
    
    def get_return(self, signal : np.ndarray) -> np.ndarray:
        play_routine = gv.spawn(self.play(signal))
        rec_routine = gv.spawn_later(self.delay, self.rec(len(signal)))
        gv.joinall([play_routine,rec_routine])
        signal_return = rec_routine.get()
        return signal_return
    
    def max_gain_test(self) -> tuple[float,float]:
        noise_lvl = self.get_return_lvl(self.rate*5)
        max_amp=0
        lvl = 0
        while lvl <0.9:
            max_amp+=0.01
            tone = self.tone(max_amp)
            lvl = self.get_return_lvl(tone)
        return max_amp, noise_lvl

    def sweep_test(self, max_amp : float) -> dict:
        amp = 0
        sweep_returns={}
        while amp < max_amp:
            amp+=0.01
            sweep = self.sweep(amp)
            self.play(sweep)
            audio_array = self.comunicate(sweep)
            sweep_returns[amp] = audio_array
        return sweep_returns

a = Catchr()
a.play(a.sweep(0.25)) 


