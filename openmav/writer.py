from socket import socket, AF_INET, SOCK_DGRAM

from .data import FGData

class Writer:

    def __init__(self, host='localhost', port=5400) -> None:
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.connect((host, port))

    def write(self, data: FGData) -> None:
        raw = data.to_bytes()
        self._socket.sendall(raw)

    def close(self) -> None:
        self._socket.close()
