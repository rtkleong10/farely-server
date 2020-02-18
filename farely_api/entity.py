# class RouteQuery:
# 	ADULT = 1
# 	CHILD = 2
# 	FARE_TYPES = [
# 		(ADULT, 'Adult'),
# 		(CHILD, 'Child'),
# 	]

from enum import Enum
from datetime import datetime


class FareType(Enum):
	WORKFARE = 0
	STUDENT = 1
	SINGLE_TRIP = 2
	SENIOR_CITIZEN = 3
	PERSONS_WITH_DISABILITIES = 4
	ADULT = 5


class TravelMode(Enum):
	WALK = 0
	BUS = 1
	MRT = 2


class RouteQuery():
	def __init__(self, startLoc="", endLoc="", route=[]):
		self.__startLoc = startLoc
		self.__endLoc = endLoc
		self.__route = route

	def __str__(self):
		return "{} to {}".format(self.__startLoc, self.__endLoc)

	@property
	def startLoc(self):
		return self.__startLoc
	@property
	def endLoc(self):
		return self.__endLoc
	@property
	def route(self):
		return self.__route
	@startLoc.setter
	def startLoc(self, startLoc):
		self.__startLoc = startLoc
	@endLoc.setter
	def endLoc(self, endLoc):
		self.__endLoc = endLoc
	@route.setter
	def route(self, route):
		self.__route = route

class Route():
	"""
	e = Route()
	d = DirectionStep(FareType.STUDENT, TravelMode.MRT, "Somerset", "BoonLay", 15, datetime.now().time())
	f = DirectionStep(FareType.STUDENT, TravelMode.MRT, "Orchard", "Jurong East", 15, datetime.now().time())
	e.directionSteps = [d,f]
	print(e)

	output:
	BoonLay to Somerset | FareType: STUDENT
	Jurong East to Orchard | FareType: STUDENT
	Total Fare: 0
	Total Travel Time: 0

	"""
	def __init__(self, directionSteps =[], totalFare=0, totalTravelTime=0):
		self.__directionSteps = directionSteps
		self.__totalFare = totalFare
		self.__totalTravelTime = totalTravelTime

	def __str__(self):
		for i in range(len(self.__directionSteps)):
			print(self.__directionSteps[i])
		return 'Total Fare: {}\nTotal Travel Time: {}'.format(self.__totalFare, self.__totalTravelTime)

	@property
	def directionSteps(self):
		return self.__directionSteps
	@property
	def totalFare(self):
		return self.__totalFare
	@property
	def totalTravelTime(self):
		return self.__totalTravelTime
	@directionSteps.setter
	def directionSteps(self, directionSteps):
		self.__directionSteps = directionSteps
	@totalFare.setter
	def totalFare(self, totalFare):
		self.__totalFare = totalFare
	@totalTravelTime.setter
	def totalTravelTime(self, totalTravelTime):
		self.__totalTravelTime = totalTravelTime



class DirectionStep():
	"""
		e = DirectionStep(FareType.STUDENT, TravelMode.MRT ,"Orchard", "Boon Lay", 2.45, datetime.now().time())
		print(e)
		d = DirectionStep(FareType.STUDENT)
		d.arrivalStop = "Somerset"
		d.departureStop = "JurongEast"
		d.FareType = TravelMode.MRT
		print(d)

		output:
		Boon Lay to Orchard | FareType: STUDENT
		JurongEast to Somerset | FareType: STUDENT
	"""

	def __init__(self, fareType="", travelMode="", arrivalStop="", departureStop="", distance=0, time=0):
		self.__travelMode = travelMode
		self.__fareType = fareType
		self.__arrivalStop = arrivalStop
		self.__departureStop = departureStop
		self.__distance = distance
		self.__time = time

	def __str__(self):
		return '{} to {} | FareType: {}'.format(self.__departureStop, self.__arrivalStop, self.__fareType.name)

	@property
	def travelMode(self):
		return self.__travelMode

	@property
	def fareType(self):
		return self.__fareType

	@property
	def arrivalStop(self):
		return self.__arrivalStop

	@property
	def departureStop(self):
		return self.__departureStop

	@property
	def distance(self):
		return self.__distance

	@property
	def time(self):
		return self.__time

	@travelMode.setter
	def travelMode(self, travelMode):
		self.__travelMode = travelMode

	@fareType.setter
	def fareType(self, fareType):
		self.__fareType = fareType

	@arrivalStop.setter
	def arrivalStop(self, arrivalStop):
		self.__arrivalStop = arrivalStop

	@departureStop.setter
	def departureStop(self, departureStop):
		self.__departureStop = departureStop

	@distance.setter
	def distance(self, distance):
		self.__distance = distance

	@time.setter
	def time(self, time):
		self.__time = time


class Location():
	"""
	e = Location("ntu", 1.0, 2.5)
	print(e)
	e.name = "nus"
	print(e)

	output:
	(ntu,1.0,2.5)
	(nus,1.0,2.5)
	"""

	def __init__(self, name="", lat=0, long=0):
		self.__name = name
		self.__lat = lat
		self.__long = long

	def __str__(self):
		return '({},{},{})'.format(self.__name, self.__lat, self.__long)

	@property
	def name(self):
		return self.__name

	@property
	def lat(self):
		return self.__lat

	@property
	def long(self):
		return self.__long

	@name.setter
	def name(self, name):
		self.__name = name

	@lat.setter
	def lat(self, lat):
		self.__lat = lat

	@long.setter
	def long(self, long):
		self.__long = long
