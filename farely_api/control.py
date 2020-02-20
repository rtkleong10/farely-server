from .boundary import GoogleMapsService, DataGovService, LTADataMallService
from .enum import FareType, TravelMode, FareCategory
from .entity import Location, RouteQuery, Route, DirectionStep

class FindRoutesController():
	def __init__(self, sort_mode, fare_type, departure_time, departure_location, arrival_location):
		fare_type = FareType(fare_type)

		departure_location_arr = departure_location.split('|')
		departure_location = Location(*departure_location_arr)

		arrival_location_arr = arrival_location.split('|')
		arrival_location = Location(*arrival_location_arr)

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
	def __init__(self, fare_type, direction_steps):
		self.__fare_table = DataGovService.getFareTable()
		self.__bus_services = LTADataMallService.getBusServices()
		self.__fare_type = fare_type
		self.__steps = self.parseSteps(direction_steps)

	def parseSteps(self, direction_steps):
		steps = []

		for step in direction_steps:
			distance = step.distance

			fare_category = None

			if step.travel_mode == TravelMode.MRT_LRT:
				fare_category = FareCategory.MRT_LRT

			elif step.travel_mode == TravelMode.BUS:
				fare_category = self.getBusType(step.line)

			elif step.travel_mode == TravelMode.WALK:
				fare_category = FareCategory.WALK

			steps.append((fare_category, distance))

		return steps

	def getBusType(self, serviceNo):
		return self.__bus_services.get(serviceNo)

	def getStepFare(self, fare_category, distance):
		if fare_category == FareCategory.WALK or distance == 0:
			return 0

		if fare_category == None:
			return None

		fare_type = self.__fare_type
		distance_fare_table = self.__fare_table[fare_category]

		for distance_range in distance_fare_table.keys():
			if distance >= distance_range[0] and (distance_range[1] == None or distance < distance_range[1]):
				return distance_fare_table[distance_range][fare_type]

		return None

	def calculateCashFare(self):
		total_fare = 0

		for step in self.__steps:
			fare_category = step[0]
			distance = step[1]
			current_fare = self.getStepFare(fare_category, distance)

			if current_fare == None:
				return None

			total_fare += current_fare

		return total_fare

	def calculateCardFare(self):
		total_fare = 0

		current_fare_category = None
		current_distance = 0
		MRT_LRT_GROUP_CATEGORY = [FareCategory.MRT_LRT, FareCategory.TRUNK_BUS]

		for step in self.__steps:
			fare_category = step[0]
			distance = step[1]

			if (fare_category == current_fare_category) or (current_fare_category in MRT_LRT_GROUP_CATEGORY and fare_category in MRT_LRT_GROUP_CATEGORY):
				current_distance += distance

			else:
				current_fare = self.getStepFare(current_fare_category, current_distance)

				if current_fare == None:
					return None

				total_fare += current_fare

				current_fare_category = fare_category
				current_distance = distance

		current_fare = self.getStepFare(current_fare_category, current_distance)

		if current_fare == None:
			return None

		total_fare += current_fare

		return total_fare

	def calculateFare(self):
		fare_type = self.__fare_type

		if fare_type == FareType.SINGLE_TRIP:
			return self.calculateCashFare() / 100

		else:
			return self.calculateCardFare() / 100

class LocationController():
	@staticmethod
	def getLocations(plaintext):
		data = GoogleMapsService.getLocations(plaintext)

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