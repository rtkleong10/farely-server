from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlaintextLocationSerializer, LocationListSerializer, RouteQuerySerializer, RouteListSerializer
from farely_server.settings import GOOGLE_MAPS_API_KEY
import requests

class InterpretLocationAPI(APIView):
	"""
	Interprets the plaintext location of the user and returns a list of candidate locations.

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
		print(plaintext_location_serializer.data)

		# URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
		# r = requests.get(url = URL, params = {
		# 	'query': plaintext_location_serializer.data['plaintext'],
		# 	'key': GOOGLE_MAPS_API_KEY	
		# }) 
		
		# print(r.json())
		# data = r.json()
		# latitude = data['results'][0]['geometry']['location']['lat']
		# longitude = data['results'][0]['geometry']['location']['lng']
		# name = data['results'][0]['name']

		location_list_serializer = LocationListSerializer({
			'locations': [
				{
					'name': 'NTU',
					'latitude': 1.3,
					'longitude': 1.2,
				},
				{
					'name': 'NYJC',
					'latitude': 1.3,
					'longitude': 1.2,
				},
			]
		})

		return Response(location_list_serializer.data)

class FindRoutesAPI(APIView):
	"""
	Accepts a route query and returns a list of the best routes

	## Parameters
	- sort_mode: The sorting mode (as an integer)
		- 0: Sort by price
		- 1: Sort by travel time
	- fare_type: The fare type (as an integer)
		- 0: Workfare transport concession card fare
		- 1: Student card fare
		- 2: Single trip
		- 3: Senior citizen card fare
		- 4: Persons with disabilities card fare
		- 5: Adult card fare
	- departure_time: The starting time of the route
	- departure_location: The starting point of the route
		- latitude
		- longitude
	- arrival_location: The end location of the route
		- latitude
		- longitude

	## Return Format
		{
			routes: [
				{
					'time': ...,
					'price': ...,
					'directions': [
						{
							'transport_type': ...,
							'line': ...,
							'time': ...,
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

		print(route_query_serializer.data)

		routes_serializer = RouteListSerializer({
			'routes': []
		})

		return Response(routes_serializer.data)