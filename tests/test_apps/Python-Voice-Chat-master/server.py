#!/usr/bin/python3

import socket
import threading


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        while True:
            try:
                self.port = 9000

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))

                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        self.accept_connections()

    def accept_connections(self):
        self.s.listen(10)

        print("Running on IP: " + self.ip)
        print("Running on port: " + str(self.port))

        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        while True:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)

            except socket.error:
                c.close()


server = Server()
