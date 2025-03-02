import struct

class FGData:

    format = '@fff'
    size = struct.calcsize(format)

    def __init__ (
        self,
        altitude: float,
        latitude: float,
        longitude: float,
    ) -> None:
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude

    def to_bytes(self) -> bytes:
        return struct.pack (
            FGData.format,
            self.altitude,
            self.latitude,
            self.longitude
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'FGData':
        return FGData(*struct.unpack(FGData.format, raw))
