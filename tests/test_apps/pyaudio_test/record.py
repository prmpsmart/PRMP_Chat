from tests.libs.pyaudio import paInt16, PyAudio
import wave

# Record in chunks of 1024 samples
chunk = 1024

# 16 bits per sample
sample_format = paInt16
chanels = 2

# Record at 44400 samples per second
smpl_rt = 44400
seconds = 3
filename = "path_of_file1.wav"

# Create an interface to PortAudio
pa = PyAudio()

stream = pa.open(
    format=sample_format,
    channels=chanels,
    rate=smpl_rt,
    input=True,
    frames_per_buffer=chunk,
)

print("Recording...")

# Initialize array that be used for storing frames
frames = []

# Store data in chunks for 8 seconds
for i in range(int(smpl_rt / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)
    print(i, end=", ")

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate - PortAudio interface
pa.terminate()

print("Done !!! ")

# Save the recorded data in a .wav format
sf = wave.open(filename, "wb")
sf.setnchannels(chanels)
sf.setsampwidth(pa.get_sample_size(sample_format))
sf.setframerate(smpl_rt)
sf.writeframes(b"".join(frames))
sf.close()
