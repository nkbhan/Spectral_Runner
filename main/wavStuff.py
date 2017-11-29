import wave
import numpy as np
import scipy.io.wavfile as sciwave
import struct
import array

f = 'Music/The Seatbelts - Tank.wav'
CHUNK = 1024
S16LE = np.dtype("<h") # signed 16 bit little endian bit type

# downsample must be power of 2
def sciOpen(f, downSample=1, chunk=CHUNK):
    chunk = int(chunk/downSample)
    rate, data = sciwave.read(f)
    if data[0].shape == (2,):
        mono = np.mean(data, axis=1)
        mono = mono.astype(S16LE, copy=False)

        numOfChunks = int(np.ceil(mono.size/chunk))
        shape = (numOfChunks, chunk)
        mono.resize(shape)
        return rate, mono
    else:
        numOfChunks = int(np.ceil(data.size/chunk))
        shape = (numOfChunks, chunk)
        data.resize(shape)
        return rate, data
