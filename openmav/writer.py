from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

from .data import OutData

class Writer:

    def __init__(self, host='localhost', port=5400, kind='udp') -> None:
        match kind:
            case 'udp': socket_kind = SOCK_DGRAM
            case 'tcp': socket_kind = SOCK_STREAM
            case _: raise ValueError('Invalid socket kind!')
        self._socket = socket(AF_INET, socket_kind)
        self._socket.connect((host, port))

    def write(self, data: OutData) -> None:
        raw = data.to_bytes()
        self._socket.sendall(raw)

    def close(self) -> None:
        self._socket.close()
