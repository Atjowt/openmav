from socket import socket, AF_INET, SOCK_DGRAM

from .data import FGData

class Reader:

    def __init__(self, host='localhost', port=5500) -> None:
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))

    def read(self) -> FGData:
        raw, _ = self.socket.recvfrom(FGData.size)
        data = FGData.from_bytes(raw)
        return data

    def close(self) -> None:
        self.socket.close()
