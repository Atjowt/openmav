from .data import FlightData
from typing import Callable

class Scenario:
    def __init__(self,
        initfn: Callable[[FlightData], FlightData],
        updatefn: Callable[[FlightData], FlightData]
    ) -> None:
        self.initfn = initfn
        self.updatefn = updatefn

# A bunch of actions you can perform (either as init, or update) ...

def position_over_stockholm(data: FlightData) -> FlightData:
    ...
