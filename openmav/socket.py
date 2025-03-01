import socket
import ctypes
from .data import FlightData

class Connection:

    def __init__(self, host='127.0.0.1', port=5500) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((host, port))

    def receive(self) -> FlightData | None:
        buffer_size = ctypes.sizeof(FlightData)
        raw_data, _ = self._socket.recvfrom(buffer_size)
        if not raw_data: return None
        raw_ptr = ctypes.c_char_p(raw_data)
        data_ptr = ctypes.cast(raw_ptr, ctypes.POINTER(FlightData))
        data = data_ptr.contents
        return data

    def disconnect(self) -> None:
        self._socket.close()
