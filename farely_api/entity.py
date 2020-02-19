from datetime import datetime, timedelta
from .enum import SortMode, FareType, TravelMode

class RouteQuery():
	def __init__(self, sort_mode=SortMode.PRICE, fare_type=FareType.ADULT, departure_time=datetime.now(), departure_location=None, arrival_location=None):
		self.__sort_mode = sort_mode
		self.__fare_type = fare_type
		self.__departure_time = departure_time
		self.__departure_location = departure_location
		self.__arrival_location = arrival_location


	def __repr__(self):
		return "{} to {}".format(self.__departure_location, self.__arrival_location)

	@property
	def sort_mode(self):
		return self.__sort_mode

	@property
	def fare_type(self):
		return self.__fare_type

	@property
	def departure_time(self):
		return self.__departure_time

	@property
	def departure_location(self):
		return self.__departure_location

	@property
	def arrival_location(self):
		return self.__arrival_location

	@sort_mode.setter
	def sort_mode(self, sort_mode):
		self.__sort_mode = sort_mode

	@fare_type.setter
	def fare_type(self, fare_type):
		self.__fare_type = fare_type

	@departure_time.setter
	def departure_time(self, departure_time):
		self.__departure_time = departure_time

	@departure_location.setter
	def departure_location(self, departure_location):
		self.__departure_location = departure_location

	@arrival_location.setter
	def arrival_location(self, arrival_location):
		self.__arrival_location = arrival_location


class Route():
	"""
	e = Route()
	d = DirectionStep("East west", TravelMode.MRT, "Somerset", "BoonLay", 15, timedelta(hours=1))
	f = DirectionStep("East west", TravelMode.MRT, "Orchard", "Jurong East", 15, timedelta(hours=1))
	e.directionSteps = [d,f]
	print(e)

	output:
	BoonLay to Somerset
	Jurong East to Orchard
	Total Fare: 0
	Total Travel Time: 0
	Total Distance: 0

	"""

	def __init__(self, price=0, travel_time=0, distance=0, direction_steps =[]):
		self.__price = price
		self.__travel_time = travel_time
		self.__distance = distance
		self.__direction_steps = direction_steps

	def __repr__(self):
		for i in range(len(self.__direction_steps)):
			print(self.__direction_steps[i])

		return 'Total Fare: {}\nTotal Travel Time: {}\nTotal Distance: {}'.format(self.__price, self.__travel_time, self.__distance)

	@property
	def price(self):
		return self.__price

	@property
	def travel_time(self):
		return self.__travel_time

	@property
	def distance(self):
		return self.__distance

	@property
	def direction_steps(self):
		return self.__direction_steps

	@direction_steps.setter
	def direction_steps(self, direction_steps):
		self.__direction_steps = direction_steps

	@price.setter
	def price(self, price):
		self.__price = price

	@travel_time.setter
	def travel_time(self, travel_time):
		self.__travel_time = travel_time

	@distance.setter
	def distance(self, distance):
		self.__distance = distance


class DirectionStep():
	"""
		Example:
		e = DirectionStep("East-West Line", TravelMode.MRT ,"Orchard", "Boon Lay", 2.45, timedelta(hours=1))
		print(e)
		d.arrival_stop = "Somerset"
		d.departure_stop = "JurongEast"
		print(d)

		Output:
		Boon Lay to Orchard
		JurongEast to Somerset
	"""

	def __init__(self, line="", travel_mode=TravelMode.BUS, arrival_stop=None, departure_stop=None, distance=0, travel_time=timedelta(hours=1)):
		self.__travel_mode = travel_mode
		self.__line = line
		self.__arrival_stop = arrival_stop
		self.__departure_stop = departure_stop
		self.__distance = distance
		self.__travel_time = travel_time

	def __repr__(self):
		return '{} to {}'.format(self.__departure_stop, self.__arrival_stop)

	@property
	def travel_mode(self):
		return self.__travel_mode

	@property
	def line(self):
		return self.__line

	@property
	def arrival_stop(self):
		return self.__arrival_stop

	@property
	def departure_stop(self):
		return self.__departure_stop

	@property
	def distance(self):
		return self.__distance

	@property
	def travel_time(self):
		return self.__travel_time

	@travel_mode.setter
	def travel_mode(self, travel_mode):
		self.__travel_mode = travel_mode

	@line.setter
	def line(self, line):
		self.__line = line

	@arrival_stop.setter
	def arrival_stop(self, arrival_stop):
		self.__arrival_stop = arrival_stop

	@departure_stop.setter
	def departure_stop(self, departure_stop):
		self.__departure_stop = departure_stop

	@distance.setter
	def distance(self, distance):
		self.__distance = distance

	@travel_time.setter
	def travel_time(self, travel_time):
		self.__travel_time = travel_time


class Location():
	"""
	e = Location("ntu", 1.0, 2.5)
	print(e)
	e.name = "nus"
	print(e)

	output:
	ntu: (1.0, 2.5)
	nus: (1.0, 2.5)
	"""

	def __init__(self, name="", lat=0, lng=0):
		self.__name = name
		self.__lat = lat
		self.__lng = lng

	def __repr__(self):
		return '{}: ({}, {})'.format(self.__name, self.__lat, self.__lng)

	@property
	def name(self):
		return self.__name

	@property
	def lat(self):
		return self.__lat

	@property
	def lng(self):
		return self.__lng

	@name.setter
	def name(self, name):
		self.__name = name

	@lat.setter
	def lat(self, lat):
		self.__lat = lat

	@lng.setter
	def lng(self, lng):
		self.__lng = lng
