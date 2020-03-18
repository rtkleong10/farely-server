"""Contains the boundary classes for the Farely API.

Handles requests to and processes responses from APIs.
"""
import re
import requests
import geocoder

from farely_server.settings import GOOGLE_MAPS_API_KEY, LTA_API_KEY

from .enum import FareType, FareCategory
from .entity import Location

__all__ = [
	'GoogleMapsService',
	'DataGovService',
	'LTADataMallService',
]

class GoogleMapsService():
	"""Handle requests to and processes responses from Google Maps APIs.
	"""
	DIRECTIONS_API_URL = 'https://maps.googleapis.com/maps/api/directions/json'
	"""The url for the Google Maps Directions API"""

	@staticmethod
	def get_directions(origin, destination):
		"""Fetches the best routes from the origin to the destination.

		Uses the [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/start) to find the best routes from the origin to the destination.

		Args:
			origin (str): Starting location of route.
			destination (str): End location of route.

		Returns:
			directions (dict): Response from Google Maps Directions API.
		"""
		r = requests.get(
			url=GoogleMapsService.DIRECTIONS_API_URL,
			params={
				'key': GOOGLE_MAPS_API_KEY,
				'mode': 'transit',
				'units': 'metric',
				'alternatives': 'true', # To get more than 1 route
				'region': 'sg', # Region biasing for Singapore
				'origin': origin,
				'destination': destination,
			}
		)

		return r.json()

	@staticmethod
	def get_location(lat, lng):
		"""Returns a `farely_api.entity.Location` object corresponding to the latitude and longitude values

		Uses the [Google Maps Places API](https://developers.google.com/places/web-service/intro) to geocode the latitude and longitude, to get the name of the location. Combines the latitude, longitude and name into a `farely_api.entity.Location` object.

		Args:
			lat (float): Latitude of the location.
			lng (float): Longitude of the location.

		Returns:
			 location (farely_api.entity.Location): Location corresponding to the latitutde and longitude values.
		"""
		r = geocoder.google(
			key=GOOGLE_MAPS_API_KEY,
			method='places',
			location='{},{}'.format(lat, lng),
		)

		name = r.name

		location = Location(
			lat=lat,
			lng=lng,
			name=name
		)

		return location

	@staticmethod
	def get_country(query):
		"""
		Returns a `farely_api.entity.Location` object corresponding to the latitude and longitude values

		Uses the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start) to geocode the latitude and longitude, to get the country of the location.

		Args:
			query (str): Location represented in textual form (e.g. 'NTU').

		Returns:
			 country (str): Country corresponding to the location.
		"""
		r = geocoder.google(
			location=query,
			key=GOOGLE_MAPS_API_KEY,
			region='sg' # Region biasing for Singapore
		)

		country = r.country

		return country

class DataGovService():
	"""Handle requests to and processes responses from Data.gov.sg APIs.

	Fetches the fare tables from the Data.gov.sg for feeder buses, express buses, trunk buses, MRTs and LRTs. Parses the data into a dictionary. Combines the fare tables in the `farely_api.boundary.DataGovService.get_fare_table()` method.

	It uses the following resources:
	- [Fares for Feeder Bus Services](https://data.gov.sg/dataset/fares-for-feeder-bus-services)
	- [Fares for Express Bus Services](https://data.gov.sg/dataset/fare-for-express-bus-services)
	- [Fares for Trunk Bus Services](https://data.gov.sg/dataset/fare-structure-for-trunk-bus-services)
	- [Fares for MRT and LRT](https://data.gov.sg/dataset/fare-structure-mrts-and-lrts)
	"""
	DATA_GOV_API_URL = 'https://data.gov.sg/api/action/datastore_search'
	"""The base url for the Data.gov.sg resources."""
	FEEDER_BUS_RESOURCE_ID = '310d0e0a-892f-48c4-abda-bfbdded8cb21'
	"""The resource id for [Fares for Feeder Bus Services](https://data.gov.sg/dataset/fares-for-feeder-bus-services)."""
	EXPRESS_BUS_RESOURCE_ID = '32cf2f0a-7790-40f0-a6cd-929697edd3b8'
	"""The resource id for [Fares for Express Bus Services](https://data.gov.sg/dataset/fare-for-express-bus-services)."""
	TRUNK_BUS_RESOURCE_ID = '7a5c22f0-71da-4c24-b419-84322b54ce17'
	"""The resource id for [Fares for Trunk Bus Services](https://data.gov.sg/dataset/fare-structure-for-trunk-bus-services)."""
	MRT_LRT_RESOURCE_ID = 'e496ae38-989e-4eac-977d-e64c9e91a20f'
	"""The resource id for [Fares for MRT and LRT](https://data.gov.sg/dataset/fare-structure-mrts-and-lrts)."""

	BUS_FARE_TYPE_MAPPING = {
		'adult_card_fare_per_ride': FareType.ADULT,
		'adult_cash_fare_per_ride': FareType.SINGLE_TRIP,
		'senior_citizen_card_fare_per_ride': FareType.SENIOR_CITIZEN,
		'student_card_fare_per_ride': FareType.STUDENT,
		'workfare_transport_concession_card_fare_per_ride': FareType.WORKFARE,
		'persons_with_disabilities_card_fare_per_ride': FareType.PERSONS_WITH_DISABILITIES,
		'cash_fare_per_ride': FareType.SINGLE_TRIP,
	}
	"""A dictionary that maps the name of the fare types used by Data.gov.sg for buses to `farely_api.enum.FareType` objects."""
	MRT_LRT_FARE_TYPE_MAPPING = {
		'Adult card fare': FareType.ADULT,
		'Single trip': FareType.SINGLE_TRIP,
		'Senior citizen card fare': FareType.SENIOR_CITIZEN,
		'Student card fare': FareType.STUDENT,
		'Workfare transport concession card fare': FareType.WORKFARE,
		'Persons with diabilities card fare': FareType.PERSONS_WITH_DISABILITIES,
	}
	"""A dictionary that maps the name of the fare types used by Data.gov.sg for MRTs and LRTs to `farely_api.enum.FareType` objects."""
	MRT_LRT_FARE_CATEGORY_MAPPING = {
		'All other timings': FareCategory.MRT_LRT,
		'All timings': FareCategory.MRT_LRT
	}
	"""A dictionary that maps the timing of the MRT and LRT fare used by Data.gov.sg for MRTs and LRTs to `farely_api.enum.FareCategory` objects."""

	STATIC_FARES = {
		FareCategory.NIGHT_BUS: {
			(0, None): 4.50
		},
		FareCategory.FLAT_FARE_2_BUS: {
			(0, None): 2
		},
	}
	"""A dictionary representing the fare table for the night and flat fare buses whose fares do not change."""

	@staticmethod
	def get_resource(resource_id):
		"""Fetches the resource from Data.gov.sg corresponding to the resource_id.

		Loops through the result pages of the Data.gov.sg resource and combines them into one list.

		Args:
			resource_id (str): id of the resource to be fetched from Data.gov.sg API.

		Returns:
			results (list): A list of results in json format for a given resource.
		"""
		all_results = []

		while True:
			try:
				r = requests.get(
					url=DataGovService.DATA_GOV_API_URL,
					params={
						'resource_id': resource_id,
						'offset': len(all_results),
					}
				)
				r.raise_for_status()


			except Exception as e:
				print(e)
				break

			data = r.json()
			results = data['result']['records']

			# Stop if no more results to add
			if len(results) == 0:
				break

			all_results.extend(results)

		return all_results

	@staticmethod
	def parse_distance_range(distance_range):
		"""Parses the distance range into a tuple

		Accepts input in the form of either '__ km - __ km', 'Up to __ km' and 'Over __ km'. For all other kinds of input, it will treat the distance range as spanning from 0 to infinity.

		Example:
			>>> from farely_api.boundary import DataGovService
			>>> DataGovService.parse_distance_range('38.3 km - 39.2 km') # (38.2 ≤ x < 39.3)
			(38.3, 39.3)
			>>> DataGovService.parse_distance_range('Up to 3.2 km') # (< 3.3)
			(0, 3.3)
			>>> DataGovService.parse_distance_range('Over 30.2 km') # (x ≥ 30.2)
			(30.2, None)
			>>> DataGovService.parse_distance_range('') # For input that doesn't match the other formats, it will treat the distance range as spanning from 0 to infinity
			(0, None)

		Args:
			distance_range (str): Distance range in the string format from Data.gov.sg API eg. "3.3 km - 4.2 km".

		Returns:
			distance_range_tuple (tuple): Tuple representing the time range in the format: `(min_distance, max_distance)`. This means the distance range is from the `min_distance` to `max_distance`, inclusive of `min_distance` but not `max_distance`. If there is no max distance, `max_distance` will be `None`.
		"""

		decimal_num_regex = r'\d*\.?\d*'
		from_to_regex = r'({0}) km - ({0}) km'.format(decimal_num_regex)
		up_to_regex = r'Up to ({}) km'.format(decimal_num_regex)
		over_regex = r'Over ({}) km'.format(decimal_num_regex)

		# Format: '__ km - __ km'
		if re.match(from_to_regex, distance_range):
			match = re.match(from_to_regex, distance_range)
			return (float(match[1]), float(match[2]) + 0.1) # 0.1 added to account for rounding error

		# Format: 'Up to __ km'
		elif re.match(up_to_regex, distance_range):
			return (0, float(re.match(up_to_regex, distance_range)[1]) + 0.1) # 0.1 added to account for rounding error

		# Format: 'Over __ km'
		elif re.match(over_regex, distance_range):
			return (float(re.match(over_regex, distance_range)[1]), None)

		# Others: Assume distance range from 0 to infinity
		else:
			return (0, None)

	@staticmethod
	def parse_bus_results(results):
		"""Parses bus fare records into a fare table

		Used as a helper function parse the bus fare table for express and trunk buses, since they have a similar API format.

		Example:
			>>> from farely_api.boundary import DataGovService
			>>> DataGovService.parse_bus_results([
			... 	{
			... 		'distance': 'Up to 3.3 km',
			... 		'adult_card_fare_per_ride': '92.0',
			... 		'student_card_fare_per_ride': '42.0',
			... 	}
			... ])
			{(0, 3.4): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0}}

		Args:
			results (list): List of bus fare records in json format

		Returns:
			fare_table (dict): Dictionary of fare table of bus fare category.
		"""
		fare_table = {}

		for result in results:
			distance_range = DataGovService.parse_distance_range(result['distance'])

			distance_fare_table = {}

			for key in DataGovService.BUS_FARE_TYPE_MAPPING.keys():
				if key in result:
					fare_type = DataGovService.BUS_FARE_TYPE_MAPPING[key]
					fare = result[key]
					distance_fare_table[fare_type] = float(fare)

			fare_table[distance_range] = distance_fare_table

		return fare_table

	@staticmethod
	def get_fares_for_feeder_bus():
		"""Generates a fare table for feeder buses using fare records from Data.gov.sg API

		Returns:
			fare_table (dict): Dictionary of fare table for feeder buses. For example, `{<FareCategory.FEEDER_BUS: 4>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}`.
		"""
		results = DataGovService.get_resource(DataGovService.FEEDER_BUS_RESOURCE_ID)

		if (len(results) != 1):
			return {}

		result = results[0]

		distance_fare_table = {}

		for key in DataGovService.BUS_FARE_TYPE_MAPPING.keys():
			if key in result:
				fare_type = DataGovService.BUS_FARE_TYPE_MAPPING[key]
				fare = result[key]
				distance_fare_table[fare_type] = float(fare)

		return {
			FareCategory.FEEDER_BUS: {
				(0, None): distance_fare_table
			}
		}

	@staticmethod
	def get_fares_for_express_bus():
		"""Generates a fare table for express buses using fare records from Data.gov.sg API

		Returns:
			fare_table (dict): Dictionary of fare table for express buses. For example, `{<FareCategory.EXPRESS_BUS: 4>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}`.
		"""
		results = DataGovService.get_resource(DataGovService.EXPRESS_BUS_RESOURCE_ID)

		return {
			FareCategory.EXPRESS_BUS: DataGovService.parse_bus_results(results)
		}

	@staticmethod
	def get_fares_for_trunk_bus():
		"""Generates a fare table for trunk buses using fare records from Data.gov.sg API

		Returns:
			fare_table (dict): Dictionary of fare table for trunk buses. For example, `{<FareCategory.TRUNK_BUS: 4>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}`.
		"""
		results = DataGovService.get_resource(DataGovService.TRUNK_BUS_RESOURCE_ID)

		return {
			FareCategory.TRUNK_BUS: DataGovService.parse_bus_results(results)
		}

	@staticmethod
	def get_fares_for_mrt_lrt():
		"""Generate a fare table for MRTs and LRTs using fare records from Data.gov.sg API

		Returns:
			fare_table (dict): Dictionary of fare table for MRTs and LRTs. For example, `{<FareCategory.MRT_LRT: 4>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}`.
		"""
		results = DataGovService.get_resource(DataGovService.MRT_LRT_RESOURCE_ID)

		fare_table = {}

		for result in results:
			fare_type = DataGovService.MRT_LRT_FARE_TYPE_MAPPING.get(result['fare_type'])
			fare_category = DataGovService.MRT_LRT_FARE_CATEGORY_MAPPING.get(result['applicable_time'])

			if fare_type == None or fare_category == None:
				continue

			distance_range = DataGovService.parse_distance_range(result['distance'])
			fare = result['fare_per_ride']

			if fare_category not in fare_table:
				fare_table[fare_category] = {
					distance_range: {}
				}

			elif distance_range not in fare_table[fare_category]:
				fare_table[fare_category][distance_range] = {}

			fare_table[fare_category][distance_range][fare_type] = float(fare)

		return fare_table

	@staticmethod
	def get_fare_table():
		"""Generates a fare table for transit modes by combining the individual fare tables.

		Returns:
			fare_table (dict): Dictionary of fare table for all transit modes. For example, `{<FareCategory.FEEDER_BUS: 4>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 170.0}}, <FareCategory.EXPRESS_BUS: 5>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 150.0}}, <FareCategory.TRUNK_BUS: 6>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 120.0}}, <FareCategory.MRT_LRT: 2>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 110.0 }}}`.
		"""
		fare_table = DataGovService.get_fares_for_feeder_bus()
		fare_table.update(DataGovService.get_fares_for_express_bus())
		fare_table.update(DataGovService.get_fares_for_trunk_bus())
		fare_table.update(DataGovService.get_fares_for_mrt_lrt())
		fare_table.update(DataGovService.STATIC_FARES)

		return fare_table

class LTADataMallService():
	"""Handle requests to and processes responses from LTA DataMall APIs.
	"""
	BUS_SERVICES_API_URL = 'http://datamall2.mytransport.sg/ltaodataservice/BusServices'
	"""The url for the LTA DataMall's bus service API."""

	FARE_CATEGORY_MAPPING = {
		'FEEDER': FareCategory.FEEDER_BUS,
		'EXPRESS': FareCategory.EXPRESS_BUS,
		'TRUNK': FareCategory.TRUNK_BUS,
		'NIGHT SERVICE': FareCategory.NIGHT_BUS,
		'NIGHT RIDER': FareCategory.NIGHT_BUS,
		'FLAT FARE $2.00': FareCategory.FLAT_FARE_2_BUS,

		# TRUNK BUS used as estimation because the actual bus fare for these bus types aren't provided by the Government APIs
		'INDUSTRIAL': FareCategory.TRUNK_BUS,
		'TOWNLINK': FareCategory.TRUNK_BUS,
		'2-TIER FLAT FARE': FareCategory.TRUNK_BUS,
	}
	"""A dictionary that maps the name of the fare categories used by LTA DataMall for buses to `farely_api.enum.FareCategory` objects."""

	@staticmethod
	def get_bus_services():
		"""Map bus service number to its corresponding `farely_api.enum.FareCategory` object.

		Returns:
			bus_services (dict): Dictionary mapping bus service name bus service number to `farely_api.enum.FareCategory` object.
		"""
		bus_service_list = []

		while True:
			try:
				r = requests.get(
					url=LTADataMallService.BUS_SERVICES_API_URL,
					headers={
						'AccountKey': LTA_API_KEY,
					},
					params={
						'$skip': len(bus_service_list)
					}
				)

				r.raise_for_status()

			except Exception as e:
				print(e)
				break

			data = r.json()
			results = data['value']

			# Stop if no more results to add
			if len(results) == 0:
				break

			for result in results:
				service_no = result['ServiceNo']
				category = result['Category']
				bus_service_list.append((service_no, category))

		# Convert into dictionary
		bus_service_dict = {}

		for bus_service in bus_service_list:
			service_no = bus_service[0]
			category = LTADataMallService.FARE_CATEGORY_MAPPING.get(bus_service[1])

			if category != None:
				bus_service_dict[service_no] = category

		return bus_service_dict
