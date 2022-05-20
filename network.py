import socket
import pickle


class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = "localhost"
        self._port = 5556
        self._address = (self._server, self._port)
        self._football_pitch = self.connect()

    @property
    def football_pitch(self):
        return self._football_pitch

    def connect(self):
        try:
            self._client.connect(self._address)
            return pickle.loads(self._client.recv(1024))
        except Exception as err:
            print(err)

    def send(self, data):
        try:
            self._client.send(pickle.dumps(data))
            return pickle.loads(self._client.recv(1024))
        except socket.error as err:
            print(err)


if __name__ == 'main':
    n = Network()
    print(n.send("hello"))
    print(n.send("working"))
