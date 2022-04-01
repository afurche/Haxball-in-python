import socket
from _thread import *
from main import FootballPitch
import pickle


class Server:
    def __init__(self):
        self._server = "192.168.76.132"
        self._port = 5556
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._current_client_id = 0
        try:
            self._sock.bind((self._server, self._port))
        except socket.error as err:
            print(err)
        self._football_pitch = FootballPitch()

    def client_thread(self, conn, client_id):
        conn.send(pickle.dumps(self._football_pitch))
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self._football_pitch = data

                if not data:
                    print(f"Client{client_id} disconnected with server")
                    break
                else:
                    reply = self._football_pitch
                    print(f"Received from client{client_id}: {reply}")
                    print(f"Sending to client{client_id}: {reply}")

                conn.sendall(pickle.dumps(self._football_pitch))
            except Exception as e:
                print(e)
                break

        print(f"Connection with client{client_id} ended")
        self._current_client_id -= 1
        conn.close()

    def server_run(self):
        self._sock.listen(2)
        print("Server Started")
        while True:
            conn, addr = self._sock.accept()
            print("Connected to:", addr)
            start_new_thread(self.client_thread, (conn, self._current_client_id))
            self._current_client_id += 1


if __name__ == '__main__':
    Server().server_run()
