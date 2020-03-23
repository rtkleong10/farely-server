"""Contains the API views of the Farely API.

Defines the entry points of the APIs.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RouteQuerySerializer
from .control import FindRoutesController

__all__ = [
	'FindRoutesApi',
]

class FindRoutesApi(APIView):
	"""
	This API View accepts a route query and returns a list of the best routes

	## Sample Query
	[/api/find-routes/?fare_type=1&origin=boon+lay&destination=changi+airport](/api/find-routes/?fare_type=1&origin=boon+lay&destination=changi+airport)

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
		- checkpoints: List of departure stops of each direction step and the destination of the route
			- lat: Latitude of departure stop
			- lng: Longitude of departure stop
			- travel_mode: Travel mode of direction step
				- 1: Bus
				- 2: MRT/LRT
				- 3: Walk
			- name: Name of departure step
			- line: Name of the bus, mrt or lrt, if applicable (otherwise "")

	### Example
		{'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJY0QBmQoP2jERGYItxQAIu7g', 'types': ['establishment', 'point_of_interest', 'university']}, {'geocoder_status': 'OK', 'place_id': 'ChIJ483Qk9YX2jERA0VOQV7d1tY', 'types': ['airport', 'establishment', 'point_of_interest']}], 'routes': [...], 'status': 'OK'}
	"""

	def get_view_name(self):
		"""Returns the name of the view.

		Returns:
			view_name (str): Name of the view (i.e. Find Routes API).
		"""
		return "Find Routes API"

	def get(self, request):
		"""Handles the get request for this API view.

		Args:
			request (rest_framework.request.Request): GET request made including the query parameters.

		Returns:
			response (rest_framework.response.Response): API response containing the routes.

		Raises:
			 `rest_framework.serializers.ValidationError`: If the request query parameters are invalid.
		"""
		# Serialize input
		route_query_serializer = RouteQuerySerializer(data=request.query_params)

		# Raise exception if invalid
		route_query_serializer.is_valid(raise_exception=True)

		# Find candidate locations
		route_query = route_query_serializer.validated_data
		route_response = FindRoutesController(route_query).find_routes()

		return Response(route_response)
