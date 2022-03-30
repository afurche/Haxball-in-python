import socket
from _thread import *
from main import FootballPitch
import pickle
import sys


class Server:
    def __init__(self):
        self._server = "192.168.0.123"
        self._port = 5556
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.bind((self._server, self._port))
        except socket.error as err:
            print(err)
        self._football_pitch = FootballPitch()

    def client_thread(self, conn):
        conn.send(pickle.dumps(self._football_pitch))
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self._football_pitch = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    reply = self._football_pitch
                    print("Received: ", reply)
                    print("Sending: ", reply)

                conn.sendall(pickle.dumps(self._football_pitch))
            except Exception as e:
                print(e)
                break

        print("Connection closed")
        conn.close()

    def server_run(self):
        self._sock.listen(2)
        print("Waiting for connection, Server Started")
        while True:
            conn, addr = self._sock.accept()
            print("Connected to:", addr)

            start_new_thread(self.client_thread, (conn,))


if __name__ == '__main__':
    Server().server_run()
