import sys
import pyaudio as pa
import numpy as np
import matplotlib.pyplot as plt

class Catchr():
    def __init__(self):
        self.__chunk = 64
        self.__format = pa.paFloat32
        self.__channels = 1 if sys.platform == 'darwin' else 2
        self.__rate = 96000
        self.__output = pa.PyAudio()
        self.__input = pa.PyAudio()
    
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
    
    @property
    def output(self) -> pa.PyAudio:
        return self.__output
    
    @property
    def input(self) -> pa.PyAudio:
        return self.__input

    def play(self, signal : np.ndarray) -> None:
        o_stream = self.open_port(self.output)
        o_stream.write(signal.tobytes())
        o_stream.close()
        self.output.terminate()
    
    def calibrate(self) -> None:
        o_stream = self.open_port(self.output)
        i=0
        tone = self.tone()
        while o_stream.is_active():
            data = tone[i:i+self.chunk]
            if i<len(tone):
                i+=self.chunk
            else:
                i=0
            o_stream.write(data)

    def open_port(self, port : pa.PyAudio) -> pa.Stream:
        stream = port.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        output=True if port == self.output else False,
                        input=True if port == self.input else False)
        return stream
            
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
    
    def tone(self) -> np.ndarray:
        t=np.linspace(start=0, num=self.rate, stop=1, dtype=np.float32)
        tone =0.25*np.sin(2*np.pi*500*t)
        return tone

a = Catchr()
a.play(a.tone())
