"""Contains the serializers for the Farely API.

Serializers are used to format the inputs and outputs of the API.
"""

from rest_framework import serializers
from .entity import RouteQuery
from .enum import FareType
from .boundary import GoogleMapsService

__all__ = [
	'RouteQuerySerializer',
]

class RouteQuerySerializer(serializers.Serializer):
	"""Serializes route queries into `farely_api.entity.RouteQuery` objects.
	"""
	fare_type = serializers.ChoiceField(choices=FareType.choices())
	origin = serializers.CharField()
	destination = serializers.CharField()

	def to_internal_value(self, data):
		"""Converts a route query into a `farely_api.entity.RouteQuery` object

		Args:
			data (dict): Dictionary representing the route query

		Returns:
			route_query (farely_api.entity.RouteQuery): `farely_api.entity.RouteQuery` object representing the route query
		"""
		data = super().to_internal_value(data)
		return RouteQuery(**data)

	def validate(self, route_query):
		"""Converts a route query into a `farely_api.entity.RouteQuery` object

		Args:
			data (dict): Dictionary representing the route query

		Returns:
			route_query (farely_api.entity.RouteQuery): `farely_api.entity.RouteQuery` object representing the route query

		Raises:
			rest_framework.serializers.ValidationError: If the route query's origin and destination can't be found or are not in Singapore.
		"""
		validation_errors = {}

		# Check origin
		origin_country = GoogleMapsService.getCountry(route_query.origin)
		if origin_country == None:
			validation_errors['origin'] = ["Origin could not be found"]

		elif origin_country != 'SG':
			validation_errors['origin'] = ["Origin must be within Singapore"]

		# Check destination
		destination_country = GoogleMapsService.getCountry(route_query.destination)
		if destination_country == None:
			validation_errors['destination'] = ["Destination could not be found"]

		elif destination_country != 'SG':
			validation_errors['destination'] = ["Destination must be within Singapore"]

		# Raise ValidationError if any
		if validation_errors:
			raise serializers.ValidationError(validation_errors)

		return route_query