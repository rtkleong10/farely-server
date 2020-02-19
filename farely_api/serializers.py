from rest_framework import serializers
from .enum import FareType, TravelMode

class PlaintextLocationSerializer(serializers.Serializer):
	plaintext = serializers.CharField()

class LocationSerializer(serializers.Serializer):
	name = serializers.CharField()
	latitude = serializers.FloatField()
	longitude = serializers.FloatField()

class LocationListSerializer(serializers.Serializer):
	locations = LocationSerializer(many=True)

class RouteQuerySerializer(serializers.Serializer):
	sort_mode = serializers.IntegerField()
	fare_type = serializers.ChoiceField(choices=FareType.choices())
	departure_time = serializers.DateTimeField()
	departure_location = serializers.CharField()
	arrival_location = serializers.CharField()

class DirectionStepSerializer(serializers.Serializer):
	travel_mode = serializers.ChoiceField(choices=TravelMode.choices())
	line = serializers.CharField()
	travel_time = serializers.TimeField()
	departure_stop = LocationSerializer()
	arrival_stop = LocationSerializer()

class RouteSerializer(serializers.Serializer):
	travel_time = serializers.TimeField()
	price = serializers.DecimalField(max_digits=None, decimal_places=2)
	distance = serializers.FloatField()
	direction_steps = DirectionStepSerializer(many=True)

class RouteListSerializer(serializers.Serializer):
	routes = RouteSerializer(many=True)
