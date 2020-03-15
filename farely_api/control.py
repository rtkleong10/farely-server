"""
This module contains the control classes for the Farely API.
"""

from .boundary import GoogleMapsService, DataGovService, LTADataMallService
from .enum import FareType, TravelMode, FareCategory
from .entity import DirectionStep, Location

class FindRoutesController():
	"""
	This class processes a route query and returns the best routes from an origin to a destination location.

	## Example
	```
	from farely_api.entity import RouteQuery
	from farely_api.enum import FareType
	from farely_api.control import FindRoutesController

	route_query = RouteQuery(
	fare_type=FareType.ADULT,
	origin="NTU",
	destination="Changi Airport"
	)
	routes = FindRoutesController(route_query).findRoutes()
	print(routes)
	```

	### Output
	> {'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJY0QBmQoP2jERGYItxQAIu7g', 'types': ['establishment', 'point_of_interest', 'university']}, {'geocoder_status': 'OK', 'place_id': 'ChIJ483Qk9YX2jERA0VOQV7d1tY', 'types': ['airport', 'establishment', 'point_of_interest']}], 'routes': [...], 'status': 'OK'}
	"""

	def __init__(self, route_query):
		self.__route_query = route_query
		self.__fare_controller = FareController()

	def getWalkingStep(self, step):
		"""
		This method instantiates `DirectionStep` from a walking step of a route.

		## Parameters
		- `step`: A dictionary representing a walking step in the Google Maps Direction API Format

		## Returns
		A `DirectionStep` object with attributes of the walking step
		"""
		departure_stop = GoogleMapsService.getLocation(**step["start_location"])
		arrival_stop = GoogleMapsService.getLocation(**step["end_location"])
		distance = step["distance"]["value"] / 1000

		return DirectionStep(
			travel_mode=TravelMode.WALK,
			arrival_stop=arrival_stop,
			departure_stop=departure_stop,
			distance=distance,
		)

	def getTransitStep(self, step):
		"""
		This method instantiate a `DirectionStep` object from a transit step of a route.

		## Parameters
		- `step`: A dictionary representing a transit direction step in the Google Maps Direction API Format

		## Returns
		A `DirectionStep` object with attributes of the transit step
		"""
		line = step["transit_details"]["line"]["name"]
		departure_stop = Location(
			**step["transit_details"]["departure_stop"]["location"],
			name=step["transit_details"]["departure_stop"]["name"],
		)
		arrival_stop = Location(
			**step["transit_details"]["arrival_stop"]["location"],
			name=step["transit_details"]["arrival_stop"]["name"],
		)
		distance = step["distance"]["value"] / 1000

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
			distance=distance,
		)

	def getDirectionSteps(self, steps):
		"""
		This method obtains a list of direction steps from a dictionary representing the steps.

		## Parameters
		- `steps`: An list of direction steps of a route in the Google Maps Direction API Format

		## Returns
		A list of `DirectionStep` objects representing the steps of a route
		"""
		direction_steps = []

		for step in steps:
			travel_mode = step["travel_mode"]
			if travel_mode == "TRANSIT":
				direction_steps.append(self.getTransitStep(step))

			elif travel_mode == "WALKING":
				direction_steps.append(self.getWalkingStep(step))

		return direction_steps

	def addRouteDetails(self, route):
		"""
		This method adds fare and checkpoint information to a route.

		## Parameters
		- `route`: A route in the Google Maps Direction API Format

		## Returns
		A route in the Google Maps Direction API Format with fare and checkpoint information embedded
		"""
		legs = route['legs']

		# Each route will always have one leg
		for leg in legs:
			steps = leg['steps']
			direction_steps = self.getDirectionSteps(steps)

			# Add fare
			leg['fare'] = self.__fare_controller.calculateFare(self.__route_query.fare_type, direction_steps)

			# Add checkpoint information
			checkpoints = []

			for direction_step in direction_steps:
				departure_stop = direction_step.departure_stop

				checkpoint = {
					"lat": departure_stop.lat,
					"lng": departure_stop.lng,
					"name": departure_stop.name,
					"travel_mode": direction_step.travel_mode,
				}

				checkpoints.append(checkpoint)

			leg['checkpoints'] = checkpoints

	def findRoutes(self):
		"""
		This method processes a route query to find the best routes. It uses the Google Maps Direction API to find the routes. Then, it adds fare and checkpoint information to the routes.

		## Returns
		A list of routes in the Google Maps Direction API Format with fare and checkpoint information embedded
		"""
		data = GoogleMapsService.getDirections(
			origin=self.__route_query.origin,
			destination=self.__route_query.destination
		)

		routes = data['routes']

		for route in routes:
			self.addRouteDetails(route)

		return data

# Fare set to $2
class DummyFindRoutesController():
	"""
	This class processes a route query and returns the best routes from an origin to a destination location.

	## Example
	```
	from farely_api.entity import RouteQuery
	from farely_api.enum import FareType
	from farely_api.control import FindRoutesController

	route_query = RouteQuery(
	fare_type=FareType.ADULT,
	origin="NTU",
	destination="Changi Airport"
	)
	routes = FindRoutesController(route_query).findRoutes()
	print(routes)
	```

	### Output
	> {'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJY0QBmQoP2jERGYItxQAIu7g', 'types': ['establishment', 'point_of_interest', 'university']}, {'geocoder_status': 'OK', 'place_id': 'ChIJ483Qk9YX2jERA0VOQV7d1tY', 'types': ['airport', 'establishment', 'point_of_interest']}], 'routes': [...], 'status': 'OK'}
	"""

	def __init__(self, route_query):
		self.__route_query = route_query

	def getWalkingStep(self, step):
		"""
		This method instantiates `DirectionStep` from a walking step of a route.

		## Parameters
		- `step`: A dictionary representing a walking step in the Google Maps Direction API Format

		## Returns
		A `DirectionStep` object with attributes of the walking step
		"""
		departure_stop = GoogleMapsService.getLocation(**step["start_location"])
		arrival_stop = GoogleMapsService.getLocation(**step["end_location"])
		distance = step["distance"]["value"] / 1000

		return DirectionStep(
			travel_mode=TravelMode.WALK,
			arrival_stop=arrival_stop,
			departure_stop=departure_stop,
			distance=distance,
		)

	def getTransitStep(self, step):
		"""
		This method instantiate a `DirectionStep` object from a transit step of a route.

		## Parameters
		- `step`: A dictionary representing a transit direction step in the Google Maps Direction API Format

		## Returns
		A `DirectionStep` object with attributes of the transit step
		"""
		line = step["transit_details"]["line"]["name"]
		departure_stop = Location(
			**step["transit_details"]["departure_stop"]["location"],
			name=step["transit_details"]["departure_stop"]["name"],
		)
		arrival_stop = Location(
			**step["transit_details"]["arrival_stop"]["location"],
			name=step["transit_details"]["arrival_stop"]["name"],
		)
		distance = step["distance"]["value"] / 1000

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
			distance=distance,
		)

	def getDirectionSteps(self, steps):
		"""
		This method obtains a list of direction steps from a dictionary representing the steps.

		## Parameters
		- `steps`: An list of direction steps of a route in the Google Maps Direction API Format

		## Returns
		A list of `DirectionStep` objects representing the steps of a route
		"""
		direction_steps = []

		for step in steps:
			travel_mode = step["travel_mode"]
			if travel_mode == "TRANSIT":
				direction_steps.append(self.getTransitStep(step))

			elif travel_mode == "WALKING":
				direction_steps.append(self.getWalkingStep(step))

		return direction_steps

	def addRouteDetails(self, route):
		"""
		This method adds fare and checkpoint information to a route.

		## Parameters
		- `route`: A route in the Google Maps Direction API Format

		## Returns
		A route in the Google Maps Direction API Format with fare and checkpoint information embedded
		"""
		legs = route['legs']

		# Each route will always have one leg
		for leg in legs:
			steps = leg['steps']
			direction_steps = self.getDirectionSteps(steps)

			# Add fare
			leg['fare'] = 2

			# Add checkpoint information
			checkpoints = []

			for direction_step in direction_steps:
				departure_stop = direction_step.departure_stop

				checkpoint = {
					"lat": departure_stop.lat,
					"lng": departure_stop.lng,
					"name": departure_stop.name,
					"travel_mode": direction_step.travel_mode,
				}

				checkpoints.append(checkpoint)

			leg['checkpoints'] = checkpoints

	def findRoutes(self):
		"""
		This method processes a route query to find the best routes. It uses the Google Maps Direction API to find the routes. Then, it adds fare and checkpoint information to the routes.

		## Returns
		A list of routes in the Google Maps Direction API Format with fare and checkpoint information embedded
		"""
		data = GoogleMapsService.getDirections(
			origin=self.__route_query.origin,
			destination=self.__route_query.destination
		)

		routes = data['routes']

		for route in routes:
			self.addRouteDetails(route)

		return data

class FareController():
	"""
	This class is used to calculate the fare of a route. It calculates the fare based on the information from Data.gov.sg and LTA DataMall. It also refers to this pdf for more information: https://www.smrt.com.sg/Portals/0/Journey%20with%20Us/PTC0339_19%20PTC%20Conclusion%20Fare%20Table%20Brochure%20FA.pdf.
	"""

	def __init__(self):
		self.__fare_table = DataGovService.getFareTable()
		self.__bus_services = LTADataMallService.getBusServices()

	def getBusType(self, line):
		"""
		This method gets the `FareCategory` object corresponding to the line of the bus

		## Parameters
		- `line`: The line of the bus

		## Returns
		A `FareCategory` object corresponding to the line of the bus
		"""
		return self.__bus_services.get(line)

	def parseSteps(self, direction_steps):
		"""
		This method converts a list of `DirectionStep` objects into a list of tuples containing the fare category and distance of the directions steps.

		## Parameters
		- `direction_steps`: A list of `DirectionStep` objects

		## Returns
		A list of direction steps, where direction steps are represented as a tuple `(fare_category, distance)`
		"""
		steps = []

		for step in direction_steps:
			# Get distance
			distance = step.distance

			# Get fare category
			fare_category = None

			if step.travel_mode == TravelMode.MRT_LRT:
				fare_category = FareCategory.MRT_LRT

			elif step.travel_mode == TravelMode.BUS:
				fare_category = self.getBusType(step.line)

			elif step.travel_mode == TravelMode.WALK:
				fare_category = FareCategory.WALK

			steps.append((fare_category, distance))


		return steps

	def getStepFare(self, fare_type, fare_category, distance):
		"""
		This method gets the fare for a step of the route. This step may correspond to multiple direction steps that share the same or a similar fare category.

		## Parameters
		- `fare_type`: A `FareType` object representing the fare type to calculate the fare for
		- `fare_category: A `FareCategory` object representing the fare category of the step
		- `distance`: The distance of the step in kilometres

		## Returns
		The fare for the step in Singapore dollars
		"""
		if fare_category == FareCategory.WALK or distance == 0:
			return 0

		if fare_category == None:
			return None

		distance_fare_table = self.__fare_table.get(fare_category)

		if distance_fare_table == None:
			return None

		for distance_range in distance_fare_table.keys():
			if distance >= distance_range[0] and (distance_range[1] == None or distance < distance_range[1]):
				return distance_fare_table[distance_range].get(fare_type) / 100

		return None

	def calculateCashFare(self, steps):
		"""
		This method calculates the fare for a list of direction steps. This method is only for the Single Trip fare type.

		## Parameters
		- `steps`: A list of tuples representing the direction steps

		## Returns
		The calculated fare in Singapore dollars
		"""
		total_fare = 0

		for step in steps:
			fare_category = step[0]
			distance = step[1]
			current_fare = self.getStepFare(FareType.SINGLE_TRIP,fare_category, distance)

			if current_fare == None:
				return None

			total_fare += current_fare

		return total_fare

	def calculateCardFare(self, fare_type, steps):
		"""
		This method calculates the fare for a list of direction steps. This method is for fare types other than Single Trip.

		## Parameters
		- `fare_type`: A `FareType` object representing the fare type to calculate the fare for
		- `steps`: A list of tuples representing the direction steps

		## Returns
		The calculated fare in Singapore dollars
		"""
		total_fare = 0

		current_fare_category = None
		current_distance = 0
		MRT_LRT_GROUP_CATEGORY = [FareCategory.MRT_LRT, FareCategory.TRUNK_BUS]

		for step in steps:
			fare_category = step[0]
			distance = step[1]

			if (fare_category == current_fare_category) or (current_fare_category in MRT_LRT_GROUP_CATEGORY and fare_category in MRT_LRT_GROUP_CATEGORY):
				current_distance += distance

			else:
				current_fare = self.getStepFare(fare_type, current_fare_category, current_distance)

				if current_fare == None:
					return None

				total_fare += current_fare

				current_fare_category = fare_category
				current_distance = distance

		current_fare = self.getStepFare(fare_type, current_fare_category, current_distance)

		if current_fare == None:
			return None

		total_fare += current_fare

		return total_fare

	def calculateFare(self, fare_type, direction_steps):
		"""
		This method calculates the fare for a list of direction steps.

		## Parameters
		- `fare_type`: A `FareType` object representing the fare type to calculate the fare for
		- `steps`: A list of tuples representing the direction steps

		## Returns
		The calculated fare in Singapore dollars
		"""
		steps = self.parseSteps(direction_steps)

		if fare_type == FareType.SINGLE_TRIP:
			total_fare = self.calculateCashFare(steps)

		else:
			total_fare = self.calculateCardFare(fare_type, steps)

		return total_fare
