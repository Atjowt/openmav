import struct

# https://docs.python.org/3/library/struct.html#format-strings

# This data should match the procotol defined in [protocol/openmav.xml].

class InData:

    format = '@ffffffffffi?'
    size = struct.calcsize(format)

    def __init__ (self,
        altitude: float,
        latitude: float,
        longitude: float,
        heading: float,
        speed: float,
        throttle: float,
        aileron: float,
        elevator: float,
        rudder: float,
        roll: float,
        engine_rpm: int,
        engine_running: bool,
    ) -> None:
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.speed = speed
        self.throttle = throttle
        self.aileron = aileron
        self.elevator = elevator
        self.rudder = rudder
        self.roll = roll
        self.engine_rpm = engine_rpm
        self.engine_running = engine_running

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'InData':
        return InData(*struct.unpack(InData.format, raw))

class OutData:

    format = '@ffff'
    size = struct.calcsize(format)

    def __init__ (self,
        throttle: float,
        aileron: float,
        elevator: float,
        rudder: float,
    ) -> None:
        self.throttle = throttle
        self.aileron = aileron
        self.elevator = elevator
        self.rudder = rudder

    def to_bytes(self) -> bytes:
        return struct.pack (
            OutData.format,
            self.throttle,
            self.aileron,
            self.elevator,
            self.rudder,
        )
