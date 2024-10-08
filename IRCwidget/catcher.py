import wave
import sys
import pyaudio

CHUNK = 1024

def play_audio_file(filename):
    with wave.open(filename, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        while len(data := wf.readframes(CHUNK)):
            stream.write(data)

        stream.close()
        p.terminate()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Plays a wave file. Usage: {sys.argv[0]} <audio_file>')
        sys.exit(-1)

    filename = sys.argv[1]
    play_audio_file(filename)
