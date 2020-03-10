from rest_framework import serializers
from .enum import FareType, TravelMode
from .entity import DirectionStep

# class PlaintextLocationSerializer(serializers.Serializer):
# 	plaintext = serializers.CharField()

# class LocationSerializer(serializers.Serializer):
# 	name = serializers.CharField()
# 	lat = serializers.FloatField()
# 	lng = serializers.FloatField()

# class LocationListSerializer(serializers.Serializer):
# 	locations = LocationSerializer(many=True)

# class RouteQuerySerializer(serializers.Serializer):
# 	sort_mode = serializers.IntegerField()
# 	fare_type = serializers.ChoiceField(choices=FareType.choices())
# 	departure_time = serializers.DateTimeField()
# 	departure_location = serializers.CharField()
# 	arrival_location = serializers.CharField()

# class DirectionStepSerializer(serializers.Serializer):
# 	travel_mode = serializers.ChoiceField(choices=TravelMode.choices())
# 	line = serializers.CharField()
# 	travel_time = serializers.DurationField()
# 	departure_stop = LocationSerializer()
# 	arrival_stop = LocationSerializer()
#
# class RouteSerializer(serializers.Serializer):
# 	travel_time = serializers.DurationField()
# 	price = serializers.DecimalField(max_digits=None, decimal_places=2)
# 	distance = serializers.FloatField()
# 	direction_steps = DirectionStepSerializer(many=True)
#

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