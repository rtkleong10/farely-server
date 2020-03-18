"""Contains the entity classes for the Farely API.
"""

from .enum import FareType, TravelMode

__all__ = [
	'RouteQuery',
	'DirectionStep',
	'Location'
]

class RouteQuery():
	"""Creates route query objects.

	A route query is the query sent to the system when a user requests for best routes from an origin to a destination location.

	Example:
		>>> from farely_api.entity import RouteQuery
		>>> from farely_api.enum import FareType
		>>> route_query = RouteQuery(
		... 	fare_type=FareType.ADULT,
		... 	origin="NTU",
		... 	destination="Changi Airport"
		... )
		>>> print(route_query)
		NTU to Changi Airport
	"""

	def __init__(self, fare_type=FareType.ADULT, origin="", destination=""):
		self.__fare_type = fare_type
		self.__origin = origin
		self.__destination = destination

	def __repr__(self):
		return "{} to {}".format(self.__origin, self.__destination)

	@property
	def fare_type(self):
		"""Fare type of the route query.

		It contains a value of the `farely_api.enum.FareType` enum.
		"""
		return self.__fare_type

	@property
	def origin(self):
		"""Departure location of a route query.

		The departure location is the location from which the user wants the route to start. It contains a string representing the starting point (e.g. `"NTU"`).
		"""
		return self.__origin

	@property
	def destination(self):
		"""Arrival location of the route query.

		The arrival location is the location to which the user wants the route to end at. It contains a string representing the end point (e.g. `"NTU"`).
		"""
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
	"""Creates direction step objects.

	A direction step refers to a step in the directions of a route. A step consists of either taking a bus, taking a train or walking from one location to another.

	Example:
		>>> from farely_api.entity import DirectionStep, Location
		>>> from farely_api.enum import TravelMode
		>>> direction_step = DirectionStep(
		... 	line="East-West Line",
		... 	travel_mode=TravelMode.MRT_LRT,
		... 	departure_stop=Location(lat=1.0, lng=100.0, name="Start"),
		... 	arrival_stop=Location(lat=1.0, lng=101.0, name="End"),
		... 	distance=2.45,
		... )
		>>> print(direction_step)
		Start (1.0, 100.0) to End (1.0, 101.0)
	"""

	def __init__(self, line="", travel_mode=TravelMode.BUS, departure_stop=None, arrival_stop=None, distance=0.0):
		self.__travel_mode = travel_mode
		self.__line = line
		self.__arrival_stop = arrival_stop
		self.__departure_stop = departure_stop
		self.__distance = distance

	def __repr__(self):
		return '{} to {}'.format(self.__departure_stop, self.__arrival_stop)

	@property
	def travel_mode(self):
		"""Travel mode of the route query.

		It contains a value of the `farely_api.enum.TravelMode` enum.
		"""
		return self.__travel_mode

	@property
	def line(self):
		"""Line of the direction step.

		The line refers to the name of the bus, MRT or LRT taken. It contains a string.
		"""
		return self.__line

	@property
	def departure_stop(self):
		"""Location of the departure stop of the direction step.

		It contains a `farely_api.entity.Location` object.
		"""
		return self.__departure_stop

	@property
	def arrival_stop(self):
		"""Location of the arrival stop of the direction step.

		It contains a `farely_api.entity.Location` object.
		"""
		return self.__arrival_stop

	@property
	def distance(self):
		"""Distance of the direction step in kilometres.

		It contains a number.
		"""
		return self.__distance

	@travel_mode.setter
	def travel_mode(self, travel_mode):
		self.__travel_mode = travel_mode

	@line.setter
	def line(self, line):
		self.__line = line

	@departure_stop.setter
	def departure_stop(self, departure_stop):
		self.__departure_stop = departure_stop

	@arrival_stop.setter
	def arrival_stop(self, arrival_stop):
		self.__arrival_stop = arrival_stop

	@distance.setter
	def distance(self, distance):
		self.__distance = distance

class Location():
	"""Creates location objects.

	A location refers the latitude and longitude of a location.

	Example:
		>>> from farely_api.entity import Location
		>>> location = Location(
		... 	lat=1.0,
		... 	lng=100.0,
		... 	name="Somewhere"
		... )
		>>> print(location)
		Somewhere (1.0, 100.0)
	"""

	def __init__(self, lat=0.0, lng=0.0, name=""):
		self.__lat = lat
		self.__lng = lng
		self.__name = name

	def __repr__(self):
		return '{} ({}, {})'.format(self.__name, self.__lat, self.__lng)

	@property
	def lat(self):
		"""Latitude of the location.

		It contains a number.
		"""
		return self.__lat

	@property
	def lng(self):
		"""Longitude of the location.

		It contains a number.
		"""
		return self.__lng

	@property
	def name(self):
		"""Name of the location.

		It contains a string.
		"""
		return self.__name

	@lat.setter
	def lat(self, lat):
		self.__lat = lat

	@lng.setter
	def lng(self, lng):
		self.__lng = lng

	@name.setter
	def name(self, name):
		self.__name = name