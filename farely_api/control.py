from .boundary import GoogleMapsService
from .enum import FareType, TravelMode
from .entity import Location, RouteQuery, Route, DirectionStep

class FindRoutesController():
	def __init__(self, sort_mode, fare_type, departure_time, departure_location, arrival_location):
		fare_type = FareType(fare_type)

		departure_location_arr = departure_location.split('|')
		departure_location = Location(*departure_location_arr)

		arrival_location_arr = arrival_location.split('|')
		arrival_location = Location(*arrival_location_arr)
		print(type(departure_time))

		self.__route_query = RouteQuery(sort_mode, fare_type, departure_time, departure_location, arrival_location)

	def findRoutes(self):
		# data = GoogleMapsService.getDirections(
		# 	departure_time=self.__route_query.departure_time,
		# 	departure_location=self.__route_query.departure_location,
		# 	arrival_location=self.__route_query.arrival_location
		# )
		# print(data)

		return [
			Route(direction_steps=[
				DirectionStep('EW', TravelMode.BUS, Location('NTU', 1, 1), Location('NTU', 1, 1.00001), 1, 1)
			])
		]


class FareController():
	# Refer to https://www.smrt.com.sg/Portals/0/Journey%20with%20Us/PTC0339_19%20PTC%20Conclusion%20Fare%20Table%20Brochure%20FA.pdf
	def __init__(self):
		self.calculateFare()

	def calculateFare(self, directions_steps):
		pass


class LocationController():
	@staticmethod
	def getLocations(plaintext):
		data = GoogleMapsService.getLocations(plaintext)

		print(data)
		if 'candidates' not in data:
			return []

		results = data['candidates']
		location_list = []

		for result in results:
			name = result['name']
			location = result['geometry']['location']
			latitude = location['lat']
			longitude = location['lng']
			location_list.append(Location(name, latitude, longitude))

		return location_list