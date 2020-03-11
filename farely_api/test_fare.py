from .control import FareController
from .enum import FareType, TravelMode
from .entity import DirectionStep

fare_type = FareType.SINGLE_TRIP

direction_steps = [
	DirectionStep(distance=6.4, travel_mode=TravelMode.BUS, line='179A'),
	DirectionStep(distance=20, travel_mode=TravelMode.MRT_LRT),
	DirectionStep(distance=17.1, travel_mode=TravelMode.BUS, line='161'),
]
f = FareController()
print(f.calculateFare( fare_type, direction_steps))