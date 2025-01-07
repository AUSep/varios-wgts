import wave
import sys
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

def play_audio(file_dir : str) -> None:
    with wave.open(sys.argv[1], 'rb') as wf:
        p = pyaudio.PyAudio()

        o_stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        i_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        while len(data := wf.readframes(CHUNK)):
            o_stream.write(data)

        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(i_stream.read(CHUNK))

        o_stream.close()
        i_stream.close()
        p.terminate()


def record_audio() -> None:
    with wave.open('output.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')

        stream.close()
        p.terminate()