class Location():
	def __init__(self, name, longitude, latitude):
		self.name = name
		self.longitude = longitude
		self.latitude = latitude

class DirectionStep():
	def __init__(self, distance, line, travel_time, travel_mode, departure_stop, arrival_stop):
		self.distance = distance
		self.line = line
		self.travel_time = travel_time
		self.travel_mode = travel_mode
		self.departure_stop = departure_stop
		self.arrival_stop = arrival_stop

class Route():
	def __init__(self, price, travel_time, distance, direction_steps):
		self.price = price
		self.travel_time = travel_time
		self.distance = distance
		self.direction_steps = direction_steps

class RouteQuery():
	def __init__(self, fare_type, departure_time, departure_location, arrival_location):
		self.fare_type = fare_type
		self.departure_time = departure_time
		self.departure_location = departure_location
		self.arrival_location = arrival_location