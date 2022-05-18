#!/usr/bin/python3

import socket
import threading
import sys

sys.path.append(
    r"C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\PRMP_Chat\tests\libs"
)
from pyaudio.pyaudio import pyaudio


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = "localhost"
                self.target_port = 9000

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024  # 512
        format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(
            format=format,
            channels=channels,
            rate=rate,
            output=True,
            frames_per_buffer=chunk_size,
        )
        self.recording_stream = self.p.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk_size,
        )

        print("Connected to Server")

        # start threads
        threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
                print(f"Listening to {len(data)} of audio", end="\r")
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
                print(f"Spoken {len(data)} of audio", end="\r")

            except:
                pass


client = Client()
