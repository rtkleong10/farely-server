from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlaintextLocationSerializer, LocationListSerializer, RouteQuerySerializer, RouteListSerializer
from .control import LocationController, FindRoutesController

class InterpretLocationAPI(APIView):
	"""
	Interprets the plaintext location of the user and returns a list of candidate locations.

	## Sample Query
	`/api/interpret-location/?plaintext=ntu`

	## Parameters
	- plaintext: Plaintext location to find the candidate locations of

	## Return Format
		{
			locations: [
				{
					'name': ...,
					'latitude': ...,
					'longitude': ...
				},
				...
			]
		}
	"""

	def get_view_name(self):
		return "Interpret Location API"

	def get(self, request):
		# Serialize input
		plaintext_location_serializer = PlaintextLocationSerializer(data=request.query_params)

		# Raise exception if invalid
		plaintext_location_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		data = plaintext_location_serializer.data
		location_list = LocationController.getLocations(data["plaintext"])

		# Serialize output
		location_list_serializer = LocationListSerializer({
			'locations': location_list
		})

		return Response(location_list_serializer.data)

class FindRoutesAPI(APIView):
	"""
	Accepts a route query and returns a list of the best routes

	## Sample Query
	`/api/find-routes/?sort_mode=1&fare_type=1&departure_time=2020-02-02T12:00&departure_location=ntu|1|2&arrival_location=nie|2|3`

	## Parameters
	- sort_mode: The sorting mode (as an integer)
		- 1: Sort by price
		- 2: Sort by travel time
	- fare_type: The fare type (as an integer)
		- 1: Workfare transport concession card fare
		- 2: Student card fare
		- 3: Single trip
		- 4: Senior citizen card fare
		- 5: Persons with disabilities card fare
		- 6: Adult card fare
	- departure_time: The starting time of the route
	- departure_location: The starting point of the route
		- Format: name|latitude|longitude
	- arrival_location: The end location of the route
		- Format: name|latitude|longitude

	## Return Format
		{
			routes: [
				{
					'travel_time': ..., // In hh:mm (e.g. 12:00)
					'price': ..., // In SGD
					'distance': ..., // In km
					'directions': [
						{
							'transport_type': ...,
							'line': ...,
							'travel_time': ...,
							'departure_stop': {
								'name': ...,
								'latitude': ...,
								'longitude': ...
							},
							'arrival_stop': {
								'name': ...,
								'latitude': ...,
								'longitude': ...
							}
						}
					]
				},
				...
			]
		}
	"""

	def get_view_name(self):
		return "Find Routes API"

	def get(self, request):
		# Serialize input
		route_query_serializer = RouteQuerySerializer(data=request.query_params)

		# Raise exception if invalid
		route_query_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		data = route_query_serializer.data
		route_list = FindRoutesController(**data).findRoutes()

		routes_serializer = RouteListSerializer({
			'routes': route_list
		})

		return Response(routes_serializer.data)