from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RouteQuerySerializer, FareQuerySerializer, FareResponseSerializer
from .control import FindRoutesController, FareController, DummyFindRoutesController

class FindRoutesApi(APIView):
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

class DummyFindRoutesApi(APIView):
	"""
	Accepts a route query and returns a list of the best routes

	## Sample Query
	`/api/dummy-find-routes/?fare_type=1&origin=1.3495031,103.7103219&destination=1.3143176,103.6835991`

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
		- fare: In SGD (will return a dummy value of $2.00)
		- checkpoints: List of departure stops of each leg except the first leg
			- lat: Latitude of departure stop
			- lng: Longitude of departure stop
			- travel_mode: Travel mode of leg
				- 1: Bus
				- 2: MRT/LRT
				- 3: Walk

	"""

	def get_view_name(self):
		return "Dummy Find Routes API"

	def get(self, request):
		# Serialize input
		route_query_serializer = RouteQuerySerializer(data=request.query_params)

		# Raise exception if invalid
		route_query_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		data = route_query_serializer.validated_data
		route_response = DummyFindRoutesController(**data).findRoutes()

		return Response(route_response)