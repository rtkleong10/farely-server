# class RouteQuery:
# 	ADULT = 1
# 	CHILD = 2
# 	FARE_TYPES = [
# 		(ADULT, 'Adult'),
# 		(CHILD, 'Child'),
# 	]

from enum import Enum

class FareType(Enum):
	WORKFARE = 0
	STUDENT = 1
	SINGLE_TRIP = 2
	SENIOR_CITIZEN = 3
	PERSONS_WITH_DISABILITIES = 4
	ADULT = 5

class RouteQuery():
	pass

class Route():
	pass

class DirectionStep():
	pass

class Location():
	pass