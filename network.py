import socket
import pickle


class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = "192.168.0.123"
        self._port = 5556
        self._address = (self._server, self._port)
        self._football_pitch = None

    def connect_to_server(self):
        self._football_pitch = self.connect()

    @property
    def football_pitch(self):
        return self._football_pitch

    def connect(self):
        try:
            self._client.connect(self._address)
            return pickle.loads(self._client.recv(2048))
        except Exception as err:
            print(err)

    def send(self, data):
        try:
            self._client.send(pickle.dumps(data))
            return pickle.loads(self._client.recv(512))
        except socket.error as err:
            print(err)