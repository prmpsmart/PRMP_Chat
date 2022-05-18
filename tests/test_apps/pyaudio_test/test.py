from tests.test_apps.mimi_wave.mimi_wave_ui.mimi_wave._mimi_wave import *

# file = 'data.mp3'
# data = open(file, 'rb').read()


def callback(frames=None, frame=None, **kwargs):
    # if frames:
    #     print(len(frames))
    ...


# file = 'op'+file

player = WavePlayer(callback=callback)
# frames = WaveFrames([data])
# player.save_frames(frames, file)

# player.play(file=file)
# player.load_file(r'path_of_file.wav')
player.play(file="path_of_file.wav", resume=1)


exit()
o = 0
# file = 'oop'+file

if o:
    player = WaveRecorder(callback=callback)
    player.resume()
    u = player.record(file=file, seconds=5)
else:
    player = WavePlayer()
    player.resume()
    player.play(file=file)
