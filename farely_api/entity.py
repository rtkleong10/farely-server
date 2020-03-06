from datetime import timedelta
from .enum import FareType, TravelMode

class RouteQuery():
	def __init__(self, fare_type=FareType.ADULT, origin="", destination=""):
		self.__fare_type = fare_type
		self.__origin = origin
		self.__destination = destination

	def __repr__(self):
		return "{} to {}".format(self.__origin, self.__destination)

	@property
	def fare_type(self):
		return self.__fare_type

	@property
	def origin(self):
		return self.__origin

	@property
	def destination(self):
		return self.__destination

	@fare_type.setter
	def fare_type(self, fare_type):
		self.__fare_type = fare_type

	@origin.setter
	def origin(self, origin):
		self.__origin = origin

	@destination.setter
	def destination(self, destination):
		self.__destination = destination

class DirectionStep():
	"""
		Example:
		e = DirectionStep("East-West Line", TravelMode.MRT ,"Orchard", "Boon Lay", 1, 2.45, timedelta(hours=1))
		print(e)
		d.arrival_stop = "Somerset"
		d.departure_stop = "JurongEast"
		print(d)

		Output:
		Boon Lay to Orchard
		JurongEast to Somerset
	"""

	def __init__(self, line="", travel_mode=TravelMode.BUS, arrival_stop=None, departure_stop=None, num_stops=0, distance=0, duration=timedelta(hours=1)):
		self.__travel_mode = travel_mode
		self.__line = line
		self.__arrival_stop = arrival_stop
		self.__departure_stop = departure_stop
		self.__num_stops = num_stops
		self.__distance = distance
		self.__duration = duration

	def __repr__(self):
		return '{} ({}) {} to {}'.format(self.__travel_mode, self.__line, self.__departure_stop, self.__arrival_stop)

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
	def num_stops(self):
		return self.__num_stops

	@property
	def distance(self):
		return self.__distance

	@property
	def duration(self):
		return self.__duration

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

	@num_stops.setter
	def num_stops(self, num_stops):
		self.__num_stops = num_stops

	@distance.setter
	def distance(self, distance):
		self.__distance = distance

	@duration.setter
	def duration(self , duration):
		self.__duration = duration

class Location():
	def __init__(self, lat=0, lng=0):
		self.__lat = lat
		self.__lng = lng

	def __init__(self, dict):
		self.__lat = dict["lat"]
		self.__lng = dict["lng"]

	def __repr__(self):
		return '({}, {})'.format(self.__lat, self.__lng)

	@property
	def lat(self):
		return self.__lat

	@property
	def lng(self):
		return self.__lng

	@lat.setter
	def lat(self, lat):
		self.__lat = lat

	@lng.setter
	def lng(self, lng):
		self.__lng = lng