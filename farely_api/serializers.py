"""
This module contains the serializers for the Farely API. They are used to format the inputs and outputs of the API.
"""

from rest_framework import serializers
from .entity import RouteQuery
from .enum import FareType
from .boundary import GoogleMapsService

class RouteQuerySerializer(serializers.Serializer):
	"""
	This class serializes route queries into `RouteQuery` objects.
	"""
	fare_type = serializers.ChoiceField(choices=FareType.choices())
	origin = serializers.CharField()
	destination = serializers.CharField()

	def to_internal_value(self, data):
		"""
		This method converts a route query into a `RouteQuery` object

		## Parameters
		- `data`: A dictionary representing the route query

		## Returns
		A `RouteQuery` object representing the route query
		"""
		data = super().to_internal_value(data)
		return RouteQuery(**data)

	def validate(self, route_query):
		validation_errors = {}

		if GoogleMapsService.getCountry(route_query.origin) != 'SG':
			validation_errors['origin'] = "Origin must be within Singapore"

		if GoogleMapsService.getCountry(route_query.destination) != 'SG':
			validation_errors['destination'] = "Destination must be within Singapore"

		if validation_errors:
			raise serializers.ValidationError(validation_errors)

		return route_query