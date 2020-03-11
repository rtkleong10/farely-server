from enum import Enum, IntEnum

class FareCategory(IntEnum):
	MRT_LRT_EARLY = 1
	MRT_LRT = 2
	WALK = 3
	FEEDER_BUS = 4
	EXPRESS_BUS = 5
	TRUNK_BUS = 6
	NIGHT_BUS = 7
	FLAT_FARE_2_BUS = 8

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
