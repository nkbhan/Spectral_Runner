import pyaudio
import wave
import time

p = pyaudio.PyAudio()

wf = wave.open('Music/CutAndRun.wav', 'rb')
print(wf.getsampwidth())

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate=wf.getframerate(),
                input=True,
                input_device_index=1)

stream.start_stream()

while stream.is_active():
    print
    time.sleep(.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()

print(p.get_format_from_width(2))
