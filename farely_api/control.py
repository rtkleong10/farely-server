from .boundary import GoogleMapsService
from .enum import FareType
from .entity import Location, RouteQuery

class FindRoutesController():
	def __init__(self, sort_mode, fare_type_int, departure_time, departure_location_str, arrival_location_str):
		fare_type = FareType(fare_type_int)

		departure_location_arr = departure_location_str.split('|')
		departure_location = Location(**departure_location_arr)

		arrival_location_arr = arrival_location_str.split('|')
		arrival_location = Location(**arrival_location_arr)

		self.route_query = RouteQuery(fare_type, departure_time, departure_location, arrival_location)

	def findRoutes(self):
		return []

class FareController():
	# Refer to https://www.smrt.com.sg/Portals/0/Journey%20with%20Us/PTC0339_19%20PTC%20Conclusion%20Fare%20Table%20Brochure%20FA.pdf
	def __init__(self):
		self.calculateFare()

	def calculateFare(self, directions_steps):
		pass

class LocationController():
	@staticmethod
	def getLocations(plaintext):
		# data = GoogleMapsService().getLocations(plaintext)
		#
		# if 'results' not in data:
		# 	return []
		#
		# results = data['results']
		# location_list = []
		#
		# for result in results:
		# 	name = result['name']
		# 	location = result['geometry']['location']
		# 	latitude = location['lat']
		# 	longitude = location['lng']
		# 	location_list.append(Location(name, latitude, longitude))
		#
		# return location_list
		return [Location('NTU', -1, 2), Location('NIE', -3, 1)]