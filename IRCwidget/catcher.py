import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

class Catchr():
    def __init__(self):
        self.__chunk = 1024
        self.__format = pyaudio.paFloat32
        self.__channels = 1 if sys.platform == 'darwin' else 2
        self.__rate = 44100
    
    @property
    def chunk(self) -> int:
        return self.__chunk
    
    @property
    def format(self) -> int:
        return self.__format
    
    @property
    def channels(self) -> int:
        return self.__channels
    
    @property
    def rate(self) -> int:
        return self.__rate

    def play(self, signal : np.ndarray) -> None:
        p = pyaudio.PyAudio()
        o_stream = p.open(format=self.format,
                          channels=self.channels,
                          rate=self.rate,
                          output=True)
        o_stream.write(signal.tobytes())
        o_stream.close()
        p.terminate()

    def sweep(self) -> np.ndarray:
        t = np.linspace(start=0, num=(self.rate)*5, stop=5, dtype=np.float32)
        n=(self.rate/50)
        sweep = 0.25*np.sin(2*np.pi*n*(t**2))
        return sweep
    
    def pulse(self) -> np.ndarray:
        n = 250
        zeros = np.zeros(n)
        ones = np.ones(n)
        pulse = np.concatenate([zeros, ones, zeros])
        pulse.astype(np.float32)
        return pulse


