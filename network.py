import socket
import pickle


class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = "172.16.128.171"
        self._port = 5556
        self._address = (self._server, self._port)
        self._football_pitch = None

    def connect_to_server(self):
        self._football_pitch = self.connect()

    @property
    def football_pitch(self):
        return self._football_pitch

    def connect(self):
        """
        Handles connecting to server by client, at start client receives FootballPitch object with inital state of the game.
        :return:
        """
        try:
            self._client.connect(self._address)
            return pickle.loads(self._client.recv(2048))
        except Exception as err:
            print(err)

    def send(self, data):
        """
        Function handling sending and receiving data on the client side
        :param data:
        :return:
        """
        try:
            self._client.send(pickle.dumps(data))
            return pickle.loads(self._client.recv(512))
        except socket.error as err:
            print(err)
