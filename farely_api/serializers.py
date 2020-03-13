from rest_framework import serializers
from .enum import FareType, TravelMode
from .entity import DirectionStep

class RouteQuerySerializer(serializers.Serializer):
	fare_type = serializers.ChoiceField(choices=FareType.choices())
	origin = serializers.CharField()
	destination = serializers.CharField()

class CheckPointSerializer(serializers.Serializer):
	lat = serializers.FloatField()
	lng = serializers.FloatField()
	travel_mode = serializers.ChoiceField(choices=TravelMode.choices())

class DirectionStepSerializer(serializers.Serializer):
	distance = serializers.FloatField()
	travel_mode = serializers.ChoiceField(choices=TravelMode.choices())
	line = serializers.CharField(required=False)

	def to_internal_value(self, data):
		return DirectionStep(**data)

class FareQuerySerializer(serializers.Serializer):
	fare_type = serializers.ChoiceField(choices=FareType.choices())
	direction_steps = DirectionStepSerializer(many=True)

class FareResponseSerializer(serializers.Serializer):
	fare = serializers.FloatField()