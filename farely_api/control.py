from .boundary import GoogleMapsService, DataGovService, LTADataMallService
from .enum import FareType, TravelMode, FareCategory
from .entity import RouteQuery, DirectionStep
from .data import route_data

class FindRoutesController():
	def __init__(self, fare_type, origin, destination):
		fare_type = FareType(fare_type)
		self.__route_query = RouteQuery(fare_type, origin, destination)

	def getWalkingStep(self, step):
		departure_stop = step["start_location"]
		arrival_stop = step["end_location"]
		distance = step["distance"]["value"] / 1000
		duration = step["duration"]["value"]

		return DirectionStep(
			travel_mode=TravelMode.WALK,
			arrival_stop=arrival_stop,
			departure_stop=departure_stop,
			distance=distance,
			duration=duration
		)

	def getTransitStep(self, step):
		line = step["transit_details"]["line"]["name"]
		departure_stop = step["transit_details"]["departure_stop"]["location"]
		arrival_stop = step["transit_details"]["arrival_stop"]["location"]
		num_stops = step["transit_details"]["num_stops"]
		distance = step["distance"]["value"] / 1000
		duration = step["duration"]["value"]

		travel_mode = None
		mode = step["transit_details"]["line"]["vehicle"]["type"]

		if (mode == "SUBWAY"):
			travel_mode = TravelMode.MRT_LRT
		elif (mode == "BUS"):
			travel_mode = TravelMode.BUS

		return DirectionStep(
			line=line,
			travel_mode=travel_mode,
			arrival_stop=arrival_stop,
			departure_stop=departure_stop,
			num_stops=num_stops,
			distance=distance,
			duration=duration
		)

	def getDirectionSteps(self, legs):
		direction_steps = []

		for leg in legs:
			steps = leg['steps']

			for step in steps:
				travel_mode = step["travel_mode"]
				if travel_mode == "TRANSIT":
					direction_steps.append(self.getTransitStep(step))

				elif travel_mode == "WALKING":
					direction_steps.append(self.getWalkingStep(step))

		return direction_steps

	def addRouteDetails(self, route):
		legs = route['legs']
		direction_steps = self.getDirectionSteps(legs)

		# Add Fare
		fareController = FareController(self.__route_query.fare_type, direction_steps)
		route['fare'] = fareController.calculateFare()

		# Add checkpoint info
		checkpoints = []

		for direction_step in direction_steps[1:]:
			checkpoints.append(direction_step.departure_stop)

		route['checkpoints'] = checkpoints

	def findRoutes(self):
		data = GoogleMapsService.getDirections(
			origin=self.__route_query.origin,
			destination=self.__route_query.destination
		)

		routes = data['routes']

		for route in routes:
			self.addRouteDetails(route)

		return data

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
		distance_fare_table = self.__fare_table.get(fare_category)

		for distance_range in distance_fare_table.keys():
			if distance >= distance_range[0] and (distance_range[1] == None or distance < distance_range[1]):
				return distance_fare_table[distance_range].get(fare_type)

		print(distance)
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
			total_fare = self.calculateCashFare()

		else:
			total_fare = self.calculateCardFare()

		if total_fare == None:
			return None
		else:
			return total_fare / 100

# class LocationController():
# 	@staticmethod
# 	def getLocations(plaintext):
# 		data = GoogleMapsService.getLocations(plaintext)
#
# 		if 'candidates' not in data:
# 			return []
#
# 		results = data['candidates']
# 		location_list = []
#
# 		for result in results:
# 			name = result['name']
# 			location = result['geometry']['location']
# 			latitude = location['lat']
# 			longitude = location['lng']
# 			location_list.append(Location(name, latitude, longitude))
#
# 		return location_list