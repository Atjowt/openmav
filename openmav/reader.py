from socket import socket, AF_INET, SOCK_DGRAM

from .data import InData

class Reader:

    def __init__(self, host='localhost', port=5500) -> None:
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))

    def read(self) -> InData:
        raw, _ = self.socket.recvfrom(InData.size)
        data = InData.from_bytes(raw)
        return data

    def close(self) -> None:
        self.socket.close()
