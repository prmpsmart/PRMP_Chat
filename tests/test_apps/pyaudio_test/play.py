""" Play a WAVE file """
from tests.libs.pyaudio import PyAudio
import wave, os

filename = "path_of_file1.wav"
# filename = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\PRMP_Chat\tests\test_apps\qt_audio\data.wav'
# filename = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\PRMP_Chat\tests\test_apps\qt_audio\datah.m4a'

# Set chunk size of 1024 samples per data frame
chunk = 1024

# Open the soaudio/sound file
af = wave.open(filename, "rb")

# Create an interface to PortAudio
pa = PyAudio()

# Open a .Stream object to write the WAV file
# 'output = True' indicates that the
# sound will be played rather than
# recorded and opposite can be used for recording
stream = pa.open(
    format=pa.get_format_from_width(af.getsampwidth()),
    channels=af.getnchannels(),
    rate=af.getframerate(),
    output=True,
)

# Read data in chunks
rd_data = af.readframes(chunk)

# Play the sound by writing the audio
# data to the Stream using while loop
while rd_data != b"":
    stream.write(rd_data)
    rd_data = af.readframes(chunk)

# Close and terminate the stream
stream.stop_stream()
stream.close()
pa.terminate()
