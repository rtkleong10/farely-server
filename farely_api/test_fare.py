from .control import FareController
from .enum import FareType, TravelMode
from .entity import DirectionStep

fare_type = FareType.ADULT

direction_steps = [
	DirectionStep(distance=1.0, travel_mode=TravelMode.WALK),
	DirectionStep(distance=1.8, travel_mode=TravelMode.BUS, line='102'),
	DirectionStep(distance=4.6, travel_mode=TravelMode.MRT_LRT, line='North-East Line'),
]

print(FareController(fare_type, direction_steps).calculateFare())