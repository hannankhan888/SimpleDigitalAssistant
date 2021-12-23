import pyaudio
 
p = pyaudio.PyAudio()
stream = p.open(
    frames_per_buffer=3200,
    rate=16000,
    format=pyaudio.paInt16,
    channels=1,
    input=True,
)