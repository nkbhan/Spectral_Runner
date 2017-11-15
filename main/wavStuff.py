import wave
import numpy as np
import scipy.io.wavfile as sciwave
import struct
import array

f = 'Music/Luna.wav'
CHUNK = 1024
S16LE = np.dtype("<h") # signed 16 bit little endian bit type

# downsample must be power of 2
def sciOpen(f, downSample=1):
    chunk = int(CHUNK/downSample)
    rate, data = sciwave.read(f)
    mono = np.mean(data, axis=1)
    mono = mono.astype(S16LE, copy=False)

    numOfChunks = int(np.ceil(mono.size/chunk))
    shape = (numOfChunks, chunk)
    mono.resize(shape)

    # take log(audio + 1)
    # The +1 handles the log(0) case
    # maniuplate signs to avoid logs of negatve numbers
    signs = np.sign(mono)
    mono = np.fabs(mono)
    mono = np.log1p(mono)/np.log(1.5)
    mono *= signs
    return rate, mono

    # oneChunk = np.rint(mono[:CHUNK])
    # oneChunk = oneChunk.astype(int)
    # byteBuffer = bytearray(oneChunk.size)
    # print(len(byteBuffer))
    # for i, num in enumerate(oneChunk):
    #     try:
    #         struct.pack_into('q', byteBuffer, i, num)
    #     except:
    #         print(i, num)
    #         break
    # return data
    # # print(byteBuffer)

def waveOpen(f):
    with wave.open(f, mode='rb') as song:
        rate = song.getframerate()
        channels = song.getnchannels()
        frames = song.getnframes()
        width = song.getsampwidth()
        print(rate, channels, frames, frames/rate, width, frames/CHUNK)

        # read in samples as a bytes object
        samples = song.readframes(frames)

        # need to unpack the bytes into a list of ints,
        # specifically signed 16 bit integers
        # also, in wave files the data is encoded in little-endian
        # '<' specifies little-endian, 'h' for 16 bit
        unpackFormat = '<%dh'%(frames*channels)
        data = struct.unpack(unpackFormat, samples)
        seperatedChannels = []
        # left = []
        # right = []
        # for i in range(len(data)):
        #     if i%2 == 0:
        #         left.append(data[i])
        #     else:
        #         right.append(data[i])
        # npData = np.array([left, right])
        print(npData)

def getByteData(f):
    with wave.open(f, mode='rb') as song:
        rate = song.getframerate()
        channels = song.getnchannels()
        frames = song.getnframes()
        width = song.getsampwidth()

        dataType = np.dtype('<h')
        np.ndarray(shape, dataType)

        framesToRead = 10
        numOfFrameBatches = int(np.ceil(frames/framesToRead))
        unpackFormat = '<%dh'%(framesToRead*channels)
        for i in range(numOfFrameBatches):
            samples = song.readframes(framesToRead)

        samples = song.readframes(framesToRead)
        data = struct.unpack(unpackFormat, samples)
        print(data)

#https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
def oneChannel(fname, chanIdx):
    """ list with specified channel's data from multichannel wave with 16-bit data """
    f = wave.open(fname, 'rb')
    chans = f.getnchannels()
    samps = f.getnframes()
    sampwidth = f.getsampwidth()
    assert sampwidth == 2
    s = f.readframes(samps) #read the all the samples from the file into a byte string
    f.close()
    unpstr = '<{0}h'.format(samps*chans) #little-endian 16-bit samples
    print(unpstr)
    x = list(struct.unpack(unpstr, s)) #convert the byte string into a list of ints
    return x[chanIdx::chans] #return the desired channel