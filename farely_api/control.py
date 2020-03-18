"""Contains the control classes for the Farely API.

Handles the application logic for the FarelyAPI
"""

from .boundary import GoogleMapsService, DataGovService, LTADataMallService
from .enum import FareType, TravelMode, FareCategory
from .entity import DirectionStep, Location

__all__ = [
	'FindRoutesController',
	'FareController',
]

class FindRoutesController():
	"""Processes a route query and returns the best routes from an origin to a destination location.

	Example:
		>>> from farely_api.entity import RouteQuery
		>>> from farely_api.enum import FareType
		>>> from farely_api.control import FindRoutesController

		>>> route_query = RouteQuery(
		... 	fare_type=FareType.ADULT,
		... 	origin="NTU",
		... 	destination="Changi Airport"
		... )
		>>> routes = FindRoutesController(route_query).find_routes()
		>>> print(routes)
		{'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJY0QBmQoP2jERGYItxQAIu7g', 'types': ['establishment', 'point_of_interest', 'university']}, {'geocoder_status': 'OK', 'place_id': 'ChIJ483Qk9YX2jERA0VOQV7d1tY', 'types': ['airport', 'establishment', 'point_of_interest']}], 'routes': [...], 'status': 'OK'}
	"""

	def __init__(self, route_query):
		self.__route_query = route_query
		self.__fare_controller = FareController()

	def get_walking_step(self, step):
		"""Instantiates `farely_api.entity.DirectionStep` from a walking step of a route.

		Args:
			step (dict): Dictionary representing a walking step in the Google Maps Direction API Format.

		Returns:
			direction_step (farely_api.entity.DirectionStep): A `farely_api.entity.DirectionStep` object with attributes of the walking step.
		"""
		departure_stop = GoogleMapsService.get_location(**step["start_location"])
		arrival_stop = GoogleMapsService.get_location(**step["end_location"])
		distance = step["distance"]["value"] / 1000

		return DirectionStep(
			travel_mode=TravelMode.WALK,
			arrival_stop=arrival_stop,
			departure_stop=departure_stop,
			distance=distance,
		)

	def get_transit_step(self, step):
		"""Instantiates `farely_api.entity.DirectionStep` from a walking step of a route.

		Args:
			step (dict): Dictionary representing a walking step in the Google Maps Direction API Format.

		Returns:
			direction_step (farely_api.entity.DirectionStep): A `farely_api.entity.DirectionStep` object with attributes of the walking step.
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

	def get_direction_steps(self, steps):
		"""Obtains a list of direction steps from a dictionary representing the steps.

		Args:
			steps (list): List of direction steps of a route in the Google Maps Direction API Format.

		## Returns
			direction_steps (list): List of `farely_api.entity.DirectionStep` objects representing the steps of a route.
		"""
		direction_steps = []

		for step in steps:
			travel_mode = step["travel_mode"]
			if travel_mode == "TRANSIT":
				direction_steps.append(self.get_transit_step(step))

			elif travel_mode == "WALKING":
				direction_steps.append(self.get_walking_step(step))

		return direction_steps

	def add_route_details(self, route):
		"""Adds fare and checkpoint information to a route.

		Checkpoints are created for the departure stop of every step, as well as the endpoint of the last direction step (destination of the route). Checkpoints include the latitude, longitude and name of the checkpoint. For every checkpoint except the last one, the travel_mode is also included using a `farely_api.enum.TravelMode` object.

		Args:
			route (dict): Route in the Google Maps Direction API Format.
		"""
		legs = route['legs']

		# Each route will always have one leg
		for leg in legs:
			steps = leg['steps']
			direction_steps = self.get_direction_steps(steps)

			# Add fare
			leg['fare'] = self.__fare_controller.calculate_fare(self.__route_query.fare_type, direction_steps)

			# Add checkpoint information
			checkpoints = []

			# Add checkpoint for departure location of each direction step
			for direction_step in direction_steps:
				departure_stop = direction_step.departure_stop

				checkpoint = {
					"lat": departure_stop.lat,
					"lng": departure_stop.lng,
					"name": departure_stop.name,
					"travel_mode": direction_step.travel_mode,
					"line": direction_step.line,
				}

				checkpoints.append(checkpoint)

			# Add checkpoint for end of route
			if len(direction_steps) != 0:
				last_direction_step = direction_steps[-1]
				endpoint = last_direction_step.arrival_stop

				checkpoint = {
					"lat": endpoint.lat,
					"lng": endpoint.lng,
					"name": endpoint.name,
					"travel_mode": None,
					"line": "",
				}

				checkpoints.append(checkpoint)

			leg['checkpoints'] = checkpoints

	def find_routes(self):
		"""Processes a route query to find the best routes.

		Uses the Google Maps Direction API to find the routes. Then, it adds fare and checkpoint information to the routes.

		Returns:
			routes (dict): Dictionary of routes in the Google Maps Direction API Format with fare and checkpoint information embedded.
		"""
		data = GoogleMapsService.get_directions(
			origin=self.__route_query.origin,
			destination=self.__route_query.destination
		)

		routes = data['routes']

		for route in routes:
			self.add_route_details(route)

		return data

class FareController():
	"""Calculates the fare of a route.

	It calculates the fare based on the information from Data.gov.sg and LTA DataMall. It also refers to this [pdf](https://www.smrt.com.sg/Portals/0/Journey%20with%20Us/PTC0339_19%20PTC%20Conclusion%20Fare%20Table%20Brochure%20FA.pdf) for more information.
	"""

	def __init__(self):
		self.__fare_table = DataGovService.get_fare_table()
		self.__bus_services = LTADataMallService.get_bus_services()

	def get_bus_type(self, line):
		"""Obtains the `farely_api.enum.FareCategory` object corresponding to the line of the bus.

		Args:
			line (str): Line of the bus (bus number).

		Returns:
			bus_type (farely_api.enum.FareCategory): `farely_api.enum.FareCategory` object corresponding to the line of the bus.
		"""
		return self.__bus_services.get(line)

	def parse_steps(self, direction_steps):
		"""Converts a list of `farely_api.entity.DirectionStep` objects into a list of tuples containing the fare category and distance of the directions steps.

		Args:
			direction_steps (list): List of `farely_api.entity.DirectionStep` objects.

		Returns:
			direction_steps (list): List of direction steps, where direction steps are represented as a tuple `(fare_category, distance)`.
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
				fare_category = self.get_bus_type(step.line)

			elif step.travel_mode == TravelMode.WALK:
				fare_category = FareCategory.WALK

			steps.append((fare_category, distance))


		return steps

	def get_step_fare(self, fare_type, fare_category, distance):
		"""Gets the fare for a step of the route.

		This step may correspond to multiple direction steps that share the same or a similar fare category.

		Args:
			fare_type (farely_api.enum.FareType): Fare type to calculate the fare for.
			fare_category (farely_api.enum.FareCategory): Fare category of the step.
			distance (float): Distance of the step in kilometres.

		Returns:
			fare (float): Fare for the step in Singapore dollars
		"""
		if fare_category == FareCategory.WALK or distance == 0:
			return 0

		if fare_category == None:
			return None

		distance_fare_table = self.__fare_table.get(fare_category)

		if distance_fare_table == None:
			return None

		# Find the matching distance range for the distance of the step
		for distance_range in distance_fare_table.keys():
			if distance >= distance_range[0] and (distance_range[1] == None or distance < distance_range[1]):
				step_fare = distance_fare_table[distance_range].get(fare_type)

				if step_fare != None:
					return step_fare / 100 # Convert cents to dollars
				else:
					return None

		return None

	def calculate_cash_fare(self, steps):
		"""Calculates the fare for a list of direction steps.

		This method is only for the Single Trip fare type.

		Args:
			steps (list): List of tuples representing the direction steps.

		Returns:
			fare (float): Calculated fare in Singapore dollars.
		"""
		total_fare = 0

		for step in steps:
			fare_category = step[0]
			distance = step[1]
			current_fare = self.get_step_fare(FareType.SINGLE_TRIP,fare_category, distance)

			# Return None if one step's fare can't be calculated
			if current_fare == None:
				return None

			total_fare += current_fare

		return total_fare

	def calculate_card_fare(self, fare_type, steps):
		"""Calculates the fare for a list of direction steps.

		This method is for fare types other than Single Trip.

		Args:
			fare_type (farely_api.enum.FareType): Fare type to calculate the fare for.
			steps (list): List of tuples representing the direction steps.

		Returns:
			fare (float): Calculated fare in Singapore dollars.
		"""
		total_fare = 0

		current_fare_category = None
		current_distance = 0

		# Consecutive MRTs, LRTs & trunk bus fares are counted together as one step in distance fare calculation
		MRT_LRT_GROUP_CATEGORY = [FareCategory.MRT_LRT, FareCategory.TRUNK_BUS]

		for step in steps:
			fare_category = step[0]
			distance = step[1]

			# Check if falls under same category
			if (fare_category == current_fare_category) or (current_fare_category in MRT_LRT_GROUP_CATEGORY and fare_category in MRT_LRT_GROUP_CATEGORY):
				current_distance += distance

			else:
				current_fare = self.get_step_fare(fare_type, current_fare_category, current_distance)

				# Return None if one step's fare can't be calculated
				if current_fare == None:
					return None

				total_fare += current_fare

				current_fare_category = fare_category
				current_distance = distance

		current_fare = self.get_step_fare(fare_type, current_fare_category, current_distance)

		if current_fare == None:
			return None

		total_fare += current_fare

		return total_fare

	def calculate_fare(self, fare_type, direction_steps):
		"""Calculates the fare for a list of direction steps.

		Args:
			fare_type (farely_api.enum.FareType): Fare type to calculate the fare for.
			steps (list): List of `farely_api.entity.DirectionStep` objects representing the direction steps.

		Returns:
			fare (float): Calculated fare in Singapore dollars.
		"""
		steps = self.parse_steps(direction_steps)

		if fare_type == FareType.SINGLE_TRIP:
			total_fare = self.calculate_cash_fare(steps)

		else:
			total_fare = self.calculate_card_fare(fare_type, steps)

		return total_fare

# Fare set to $2
# class DummyFindRoutesController():
# 	"""
# 	This class processes a route query and returns the best routes from an origin to a destination location.
#
# 	## Example
# 	```
# 	from farely_api.entity import RouteQuery
# 	from farely_api.enum import FareType
# 	from farely_api.control import FindRoutesController
#
# 	route_query = RouteQuery(
# 	fare_type=FareType.ADULT,
# 	origin="NTU",
# 	destination="Changi Airport"
# 	)
# 	routes = FindRoutesController(route_query).find_routes()
# 	print(routes)
# 	```
#
# 	### Output
# 	> {'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJY0QBmQoP2jERGYItxQAIu7g', 'types': ['establishment', 'point_of_interest', 'university']}, {'geocoder_status': 'OK', 'place_id': 'ChIJ483Qk9YX2jERA0VOQV7d1tY', 'types': ['airport', 'establishment', 'point_of_interest']}], 'routes': [...], 'status': 'OK'}
# 	"""
#
# 	def __init__(self, route_query):
# 		self.__route_query = route_query
# 		self.__fare_controller = FareController()
#
# 	def get_walking_step(self, step):
# 		"""
# 		This method instantiates `farely_api.entity.DirectionStep` from a walking step of a route.
#
# 		## Parameters
# 		`step`: A dictionary representing a walking step in the Google Maps Direction API Format
#
# 		## Returns
# 		A `farely_api.entity.DirectionStep` object with attributes of the walking step
# 		"""
# 		departure_stop = GoogleMapsService.get_location(**step["start_location"])
# 		arrival_stop = GoogleMapsService.get_location(**step["end_location"])
# 		distance = step["distance"]["value"] / 1000
#
# 		return DirectionStep(
# 			travel_mode=TravelMode.WALK,
# 			arrival_stop=arrival_stop,
# 			departure_stop=departure_stop,
# 			distance=distance,
# 		)
#
# 	def get_transit_step(self, step):
# 		"""
# 		This method instantiate a `farely_api.entity.DirectionStep` object from a transit step of a route.
#
# 		## Parameters
# 		`step`: A dictionary representing a transit direction step in the Google Maps Direction API Format
#
# 		## Returns
# 		A `farely_api.entity.DirectionStep` object with attributes of the transit step
# 		"""
# 		line = step["transit_details"]["line"]["name"]
# 		departure_stop = Location(
# 			**step["transit_details"]["departure_stop"]["location"],
# 			name=step["transit_details"]["departure_stop"]["name"],
# 		)
# 		arrival_stop = Location(
# 			**step["transit_details"]["arrival_stop"]["location"],
# 			name=step["transit_details"]["arrival_stop"]["name"],
# 		)
# 		distance = step["distance"]["value"] / 1000
#
# 		travel_mode = None
# 		mode = step["transit_details"]["line"]["vehicle"]["type"]
#
# 		if (mode == "SUBWAY"):
# 			travel_mode = TravelMode.MRT_LRT
# 		elif (mode == "BUS"):
# 			travel_mode = TravelMode.BUS
#
# 		return DirectionStep(
# 			line=line,
# 			travel_mode=travel_mode,
# 			arrival_stop=arrival_stop,
# 			departure_stop=departure_stop,
# 			distance=distance,
# 		)
#
# 	def get_direction_steps(self, steps):
# 		"""
# 		This method obtains a list of direction steps from a dictionary representing the steps.
#
# 		## Parameters
# 		`steps`: An list of direction steps of a route in the Google Maps Direction API Format
#
# 		## Returns
# 		A list of `farely_api.entity.DirectionStep` objects representing the steps of a route
# 		"""
# 		direction_steps = []
#
# 		for step in steps:
# 			travel_mode = step["travel_mode"]
# 			if travel_mode == "TRANSIT":
# 				direction_steps.append(self.get_transit_step(step))
#
# 			elif travel_mode == "WALKING":
# 				direction_steps.append(self.get_walking_step(step))
#
# 		return direction_steps
#
# 	def add_route_details(self, route):
# 		"""
# 		This method adds fare and checkpoint information to a route. Checkpoints are created for the departure stop of every step, as well as the endpoint of the last direction step (destination of the route). Checkpoints include the latitude, longitude and name of the checkpoint. For every checkpoint except the last one, the travel_mode is also included using a `farely_api.enum.TravelMode` object
#
# 		## Parameters
# 		`route`: A route in the Google Maps Direction API Format
#
# 		## Returns
# 		A route in the Google Maps Direction API Format with fare and checkpoint information embedded
# 		"""
# 		legs = route['legs']
#
# 		# Each route will always have one leg
# 		for leg in legs:
# 			steps = leg['steps']
# 			direction_steps = self.get_direction_steps(steps)
#
# 			# Add fare
# 			leg['fare'] = self.__fare_controller.calculate_fare(self.__route_query.fare_type, direction_steps)
#
# 			# Add checkpoint information
# 			checkpoints = []
#
# 			for direction_step in direction_steps:
# 				departure_stop = direction_step.departure_stop
#
# 				checkpoint = {
# 					"lat": departure_stop.lat,
# 					"lng": departure_stop.lng,
# 					"name": departure_stop.name,
# 					"travel_mode": direction_step.travel_mode,
# 					"line": direction_step.line,
# 				}
#
# 				checkpoints.append(checkpoint)
#
# 			if len(direction_steps) != 0:
# 				last_direction_step = direction_steps[-1]
# 				endpoint = last_direction_step.arrival_stop
#
# 				checkpoint = {
# 					"lat": endpoint.lat,
# 					"lng": endpoint.lng,
# 					"name": endpoint.name,
# 					"travel_mode": None,
# 					"line": "",
# 				}
#
# 				checkpoints.append(checkpoint)
#
# 			leg['checkpoints'] = checkpoints
#
# 	def find_routes(self):
# 		"""
# 		This method processes a route query to find the best routes. It uses the Google Maps Direction API to find the routes. Then, it adds fare and checkpoint information to the routes.
#
# 		## Returns
# 		A list of routes in the Google Maps Direction API Format with fare and checkpoint information embedded
# 		"""
# 		data = GoogleMapsService.get_directions(
# 			origin=self.__route_query.origin,
# 			destination=self.__route_query.destination
# 		)
#
# 		routes = data['routes']
#
# 		for route in routes:
# 			self.add_route_details(route)
#
# 		return data