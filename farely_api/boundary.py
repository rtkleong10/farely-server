from datetime import datetime
import re
import requests

from .enum import FareType, FareCategory
from farely_server.settings import GOOGLE_MAPS_API_KEY, LTA_API_KEY


class GoogleMapsService():
	"""
	Calculates directions between locations using Google Map Direction API

	"""
	DIRECTIONS_API_URL = 'https://maps.googleapis.com/maps/api/directions/json'

	@staticmethod
	def getDirections(origin, destination):
		# TODO: Add departure time
		"""

		:param origin: Starting location of route in textual format
		:param destination: End location of route in textual format
		:return: response from Google Maps Direction API in json format
		"""
		r = requests.get(
			url=GoogleMapsService.DIRECTIONS_API_URL,
			params={
				'key': GOOGLE_MAPS_API_KEY,
				'mode': 'transit',
				'units': 'metric',
				'alternatives': 'true',
				# 'departure_time': int(datetime.timestamp(departure_time)),
				'region': 'sg',
				'origin': origin,
				'destination': destination,
			}
		)

		return r.json()


class DataGovService():
	"""
	Handle requests to and process response from  Data.gov.sg API
	"""
	#TODO Differentiate between different cash fare types
	DATA_GOV_API_URL = 'https://data.gov.sg/api/action/datastore_search'
	FEEDER_BUS_RESOURCE_ID = '310d0e0a-892f-48c4-abda-bfbdded8cb21'
	EXPRESS_BUS_RESOURCE_ID = '32cf2f0a-7790-40f0-a6cd-929697edd3b8'
	TRUNK_BUS_RESOURCE_ID = '7a5c22f0-71da-4c24-b419-84322b54ce17'
	MRT_LRT_RESOURCE_ID = 'e496ae38-989e-4eac-977d-e64c9e91a20f'

	BUS_FARE_TYPE_MAPPING = {
		'adult_card_fare_per_ride': FareType.ADULT,
		'adult_cash_fare_per_ride': FareType.SINGLE_TRIP,
		'senior_citizen_card_fare_per_ride': FareType.SENIOR_CITIZEN,
		'student_card_fare_per_ride': FareType.STUDENT,
		'workfare_transport_concession_card_fare_per_ride': FareType.WORKFARE,
		'persons_with_disabilities_card_fare_per_ride': FareType.PERSONS_WITH_DISABILITIES,
		'cash_fare_per_ride': FareType.SINGLE_TRIP,
	}

	MRT_LRT_FARE_TYPE_MAPPING = {
		'Adult card fare': FareType.ADULT,
		'Single trip': FareType.SINGLE_TRIP,
		'Senior citizen card fare': FareType.SENIOR_CITIZEN,
		'Student card fare': FareType.STUDENT,
		'Workfare transport concession card fare': FareType.WORKFARE,
		'Persons with diabilities card fare': FareType.PERSONS_WITH_DISABILITIES,
	}

	MRT_LRT_FARE_CATEGORY_MAPPING = {
		'Before 7.45am  (Weekdays excluding public holidays)': FareCategory.MRT_LRT_EARLY,
		'All other timings': FareCategory.MRT_LRT,
		'All timings': FareCategory.MRT_LRT
	}

	@staticmethod
	def getResource(resource_id):
		"""
		Fetch fare records from Data.gov.sg API

		:param resource_id: id of the resource to be fetched from Data.gov.sg API
		:return: list of fare records in json format for a given resource
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
	def parseDistanceRange(str):
		"""
		Parse distance range into a tuple

			'38.3 km - 39.2 km': (38.3, 39.3) (38.2 ≤ x < 39.3)
			'Up to 3.2 km': (0, 3.3) (< 3.3)
			'Over 30.2 km': (30.3) (x ≥ 30.2)
			Otherwise: (0, None)

		:param str: distance range in string format from Data.gov.sg API eg. "3.3 km - 4.2 km"
		:return: (min distance, max distance) - tuple representing distance range
		"""

		decimal_num_regex = r'\d*\.?\d*'
		from_to_regex = r'({0}) km - ({0}) km'.format(decimal_num_regex)
		up_to_regex = r'Up to ({}) km'.format(decimal_num_regex)
		over_regex = r'Over ({}) km'.format(decimal_num_regex)

		if re.match(from_to_regex, str):
			match = re.match(from_to_regex, str)
			return (float(match[1]), float(match[2]) + 0.1)

		elif re.match(up_to_regex, str):
			return (0, float(re.match(up_to_regex, str)[1]) + 0.1)

		elif re.match(over_regex, str):
			return (float(re.match(over_regex, str)[1]), None)

		else:
			return (0, None)

	@staticmethod
	def parseBusResults(results):
		"""
		Parse bus fare records into a fare table

		:param results: list of bus fare records in json format
		:return: dictionary of fare table of bus fare category
		e.g.
		{(0, 3.3): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 },
		 (3.4, 6.5): {<FareType.ADULT: 6>: 90.0, <FareType.STUDENT: 2>: 42.0 }
		}
		"""
		fare_table = {}

		for result in results:
			distance_range = DataGovService.parseDistanceRange(result['distance'])

			distance_fare_table = {}

			for key in DataGovService.BUS_FARE_TYPE_MAPPING.keys():
				if key in result:
					fare_type = DataGovService.BUS_FARE_TYPE_MAPPING[key]
					fare = result[key]
					distance_fare_table[fare_type] = float(fare)

			fare_table[distance_range] = distance_fare_table

		return fare_table

	@staticmethod
	def getFaresForFeederBus():
		"""
		Generate a fare table for Feeder Bus using fare records from Data.gov.sg API

		:return: dictionary of fare table for feeder bus
		e.g.
		{<FareCategory.FEEDER_BUS: 4>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}

		"""
		results = DataGovService.getResource(DataGovService.FEEDER_BUS_RESOURCE_ID)

		if (len(results) != 1):
			return {}

		result = results[0]

		fare_table = {}

		distance_fare_table = {}

		for key in DataGovService.BUS_FARE_TYPE_MAPPING.keys():
			if key in result:
				fare_type = DataGovService.BUS_FARE_TYPE_MAPPING[key]
				fare = result[key]
				distance_fare_table[fare_type] = float(fare)

		fare_table[(0, None)] = distance_fare_table

		return {
			FareCategory.FEEDER_BUS: fare_table
		}

	@staticmethod
	def getFaresForExpressBus():
		"""
		Generate a fare table for Express Bus using fare records from Data.gov.sg API

		:return: dictionary of fare table for express bus
		e.g.
		{<FareCategory.EXPRESS_BUS: 5>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}

		"""
		results = DataGovService.getResource(DataGovService.EXPRESS_BUS_RESOURCE_ID)

		return {
			FareCategory.EXPRESS_BUS: DataGovService.parseBusResults(results)
		}

	@staticmethod
	def getFaresForTrunkBus():
		"""
		Generate a fare table for Trunk Bus using fare records from Data.gov.sg API

		:return: dictionary of fare table for trunk bus
		e.g.
		{<FareCategory.TRUNK_BUS: 6>: {(0, None): {<FareType.ADULT: 6>: 92.0, <FareType.STUDENT: 2>: 42.0 }}}

		"""
		results = DataGovService.getResource(DataGovService.TRUNK_BUS_RESOURCE_ID)

		return {
			FareCategory.TRUNK_BUS: DataGovService.parseBusResults(results)
		}

	@staticmethod
	def getFaresForMRTLRT():
		"""
			Generate a fare table for MRT and LRT using fare records from Data.gov.sg API

			:return: dictionary of fare table for MRT and LRT
			e.g.
			{<FareCategory.MRT_LRT: 2>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 170.0, <FareType.ADULT: 6>: 92.0}}}

		"""
		results = DataGovService.getResource(DataGovService.MRT_LRT_RESOURCE_ID)

		fare_table = {}

		for result in results:
			fare_type = DataGovService.MRT_LRT_FARE_TYPE_MAPPING[result['fare_type']]
			fare_category = DataGovService.MRT_LRT_FARE_CATEGORY_MAPPING[result['applicable_time']]

			distance_range = DataGovService.parseDistanceRange(result['distance'])
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
	def getStaticFares():

		return {
			FareCategory.NIGHT_BUS: {
				(0, None): 4.50
			},
			FareCategory.FLAT_FARE_2_BUS: {
				(0, None): 2
			},
		}

	@staticmethod
	def getFareTable():
		"""
		Generate a fare table for transits (bus, MRT and LRT)

		:return: dictionary of fare for bus and MRT and LRT
		{<FareCategory.FEEDER_BUS: 4>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 170.0}},
		 <FareCategory.EXPRESS_BUS: 5>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 150.0}},
		 <FareCategory.TRUNK_BUS: 6>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 120.0}},
		 <FareCategory.MRT_LRT: 2>: {(0, 3.3): {<FareType.SINGLE_TRIP: 3>: 110.0 }},
		}
		"""
		fare_table = DataGovService.getFaresForFeederBus()
		fare_table.update(DataGovService.getFaresForExpressBus())
		fare_table.update(DataGovService.getFaresForTrunkBus())
		fare_table.update(DataGovService.getFaresForMRTLRT())
		fare_table.update(DataGovService.getStaticFares())
		return fare_table

class LTADataMallService():
	"""
	Map bus service number to its corresponding fare category using LTA Data Mall service
	"""
	BUS_SERVICES_API_URL = 'http://datamall2.mytransport.sg/ltaodataservice/BusServices'

	FARE_CATEGORY_MAPPING = {
		'FEEDER': FareCategory.FEEDER_BUS,
		'EXPRESS': FareCategory.EXPRESS_BUS,
		'TRUNK': FareCategory.TRUNK_BUS,
		'NIGHT SERVICE': FareCategory.NIGHT_BUS,
		'NIGHT RIDER': FareCategory.NIGHT_BUS,
		'FLAT FARE $2.00': FareCategory.FLAT_FARE_2_BUS,

		# TRUNK BUS used as estimation because the actual bus fare for these bus types aren't provided by the Government API
		'INDUSTRIAL': FareCategory.TRUNK_BUS,
		'TOWNLINK': FareCategory.TRUNK_BUS,
		'2-TIER FLAT FARE': FareCategory.TRUNK_BUS,
	}

	@staticmethod
	def getBusServices():
		"""
		Map bus service number to its corresponding fare category

		:return: dictionary with bus service number and  fare category as key and value respectively
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