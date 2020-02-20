from enum import Enum, IntEnum

class FareCategory(IntEnum):
	MRT_LRT_EARLY = 1
	MRT_LRT = 2
	FEEDER_BUS = 3
	EXPRESS_BUS = 4
	TRUNK_BUS = 5
	WALK = 6

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]

class FareType(IntEnum):
	WORKFARE = 1
	STUDENT = 2
	SINGLE_TRIP = 3
	SENIOR_CITIZEN = 4
	PERSONS_WITH_DISABILITIES = 5
	ADULT = 6

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]

class TravelMode(IntEnum):
	BUS = 1
	MRT_LRT = 2
	WALK = 3

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]

class SortMode(IntEnum):
	PRICE = 1
	TRAVEL_TIME = 2

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]