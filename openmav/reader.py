from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

from .data import InData

class Reader:

    def __init__(self, host='localhost', port=5500, kind='udp') -> None:
        match kind:
            case 'udp': socket_kind = SOCK_DGRAM
            case 'tcp': socket_kind = SOCK_STREAM
            case _: raise ValueError('Invalid socket kind!')
        self._socket = socket(AF_INET, socket_kind)
        self._socket.bind((host, port))

    def read(self) -> InData:
        raw, _ = self._socket.recvfrom(InData.size)
        data = InData.from_bytes(raw)
        return data

    def close(self) -> None:
        self._socket.close()
