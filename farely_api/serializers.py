from rest_framework import serializers

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
	fare_type = serializers.IntegerField()
	departure_time = serializers.TimeField()
	departure_location = serializers.ListField(
		child=serializers.IntegerField()
	)
	arrival_location = serializers.ListField(
		child=serializers.IntegerField()
	)

class DirectionStepSerializer(serializers.Serializer):
	transport_type = serializers.IntegerField()
	line = serializers.CharField()
	time = serializers.TimeField()
	departure_stop = LocationSerializer()
	arrival_stop = LocationSerializer()

class RouteSerializer(serializers.Serializer):
	time = serializers.TimeField()
	price = serializers.DecimalField(max_digits=None, decimal_places=2)
	directions = DirectionStepSerializer(many=True)

class RouteListSerializer(serializers.Serializer):
	routes = RouteSerializer(many=True)
