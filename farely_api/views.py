from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RouteQuerySerializer, FareQuerySerializer, FareResponseSerializer
from .control import FindRoutesController, FareController

# class InterpretLocationAPI(APIView):
# 	"""
# 	Interprets the plaintext location of the user and returns a list of candidate locations.
#
# 	## Sample Query
# 	`/api/interpret-location/?plaintext=ntu`
#
# 	## Parameters
# 	- plaintext: Plaintext location to find the candidate locations of
#
# 	## Return Format
# 		{
# 			locations: [
# 				{
# 					'name': ...,
# 					'latitude': ...,
# 					'longitude': ...
# 				},
# 				...
# 			]
# 		}
# 	"""
#
# 	def get_view_name(self):
# 		return "Interpret Location API"
#
# 	def get(self, request):
# 		# Serialize input
# 		plaintext_location_serializer = PlaintextLocationSerializer(data=request.query_params)
#
# 		# Raise exception if invalid
# 		plaintext_location_serializer.is_valid(raise_exception=True)
#
# 		# Find candidate locations
# 		data = plaintext_location_serializer.validated_data
# 		location_list = LocationController.getLocations(data["plaintext"])
#
# 		# Serialize output
# 		location_list_serializer = LocationListSerializer({
# 			'locations': location_list
# 		})
#
# 		return Response(location_list_serializer.data)

class FindRoutesAPI(APIView):
	"""
	Accepts a route query and returns a list of the best routes

	## Sample Query
	`/api/find-routes/?fare_type=1&origin=1.3495031,103.7103219&destination=1.3143176,103.6835991`

	## Parameters
	- origin: Starting point of route
	- destination: End point of route
	- fare_type: Fare type for fare calculation
		- 1: Workfare transport concession card fare
		- 2: Student card fare
		- 3: Single trip
		- 4: Senior citizen card fare
		- 5: Persons with disabilities card fare
		- 6: Adult card fare

	## Return Format
	- Google Maps API Format
	- Routes include
		- fare: In SGD
		- checkpoints: List of departure stops of each leg except the first leg
			- lat: Latitude of departure stop
			- lng: Longitude of departure stop
			- travel_mode: Travel mode of leg
				- 1: Bus
				- 2: MRT/LRT
				- 3: Walk

	"""

	def get_view_name(self):
		return "Find Routes API"

	def get(self, request):
		# Serialize input
		route_query_serializer = RouteQuerySerializer(data=request.query_params)

		# Raise exception if invalid
		route_query_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		data = route_query_serializer.validated_data
		route_response = FindRoutesController(**data).findRoutes()

		return Response(route_response)

class CalculateFareAPI(APIView):
	"""
	Takes the fare type and directions steps of a route and returns the calculated fare.

	## Input
	### Format
	- fare_type: 1 to 6
		- 1: Workfare transport concession card fare
		- 2: Student card fare
		- 3: Single trip
		- 4: Senior citizen card fare
		- 5: Persons with disabilities card fare
		- 6: Adult card fare
	- direction_steps
		- distance: In kilometres
		- travel_mode: 1 to 3
			- 1: Bus
			- 2: MRT or LRT
			- 3: Walking
		- line: Bus number (only for buses)

	### Example
		{
			"fare_type": 2,
			"direction_steps": [
				{
					"distance": 2.3,
					"travel_mode": 1,
					"line": "161"
				},
				{
					"distance": 2.3,
					"travel_mode": 2
				}
			]
		}

	## Output
	### Format
	- fare: In SGD

	### Example
		{
			"fare": 0.52
		}
	"""

	def get_view_name(self):
		return "Calculate Fare API"

	def post(self, request):
		# Serialize input
		fare_query_serializer = FareQuerySerializer(data=request.data)

		# Raise exception if invalid
		fare_query_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		data = fare_query_serializer.validated_data
		fare = FareController().calculateFare(**data)

		fare_response_serializer = FareResponseSerializer({
			'fare': fare
		})

		return Response(fare_response_serializer.data)