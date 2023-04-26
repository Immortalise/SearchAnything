import pyaudio
import wave
import whisper

class SpeechRecog(object):
    def __init__(self, asr_model='base'):
        self.asr_model = asr_model
        self.asr = whisper.Whisper(self.asr_model)


    def record_audio(self, filename):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print("* recording")

        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # record complete
        stream.stop_stream()
        stream.close()
        p.terminate()

        print("* done recording")

        # save as wav file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames)) # join frames
        wf.close()

    def recognize(self, filename):
        return self.asr.recognize(filename)

    



