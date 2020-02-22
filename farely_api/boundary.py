from datetime import datetime
import re
import requests
from .enum import FareType, FareCategory
from farely_server.settings import GOOGLE_MAPS_API_KEY, LTA_API_KEY


class GoogleMapsService():
	PLACES_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
	DIRECTIONS_API_URL = 'https://maps.googleapis.com/maps/api/directions/json'

	@staticmethod
	def getLocations(plaintext):
		r = requests.get(
			url=GoogleMapsService.PLACES_API_URL,
			params={
				'key': GOOGLE_MAPS_API_KEY,
				'inputtype': 'textquery',
				'fields': 'name,geometry',
				'input': plaintext,
			}
		)

		return r.json()

	@staticmethod
	def getDirections(departure_time, departure_location, arrival_location):
		r = requests.get(
			url=GoogleMapsService.DIRECTIONS_API_URL,
			params={
				'key': GOOGLE_MAPS_API_KEY,
				'mode': 'transit',
				'units': 'metric',
				'departure_time': int(datetime.timestamp(departure_time)),
				'origin': '{},{}'.format(departure_location.lat, departure_location.lng),
				'destination': '{},{}'.format(arrival_location.lat, arrival_location.lng),
			}
		)

		return r.json()


class DataGovService():
	#todo differentiate between different cash fare types & morning fare
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
		r = requests.get(
			url=DataGovService.DATA_GOV_API_URL,
			params={
				'resource_id': resource_id
			}
		)

		return r.json()

	@staticmethod
	def parseDistanceRange(str):
		"""
			'38.3 km - 39.2 km': (38.3, 39.2)
			'Up to 3.2 km': (0, 3.2)
			'Over 30.2 km': (30.2)
			Otherwise: (0, None)
		"""

		decimal_num_regex = r'\d*\.?\d*'
		from_to_regex = r'({0}) km - ({0}) km'.format(decimal_num_regex)
		up_to_regex = r'Up to ({}) km'.format(decimal_num_regex)
		over_regex = r'Over ({}) km'.format(decimal_num_regex)

		if re.match(from_to_regex, str):
			match = re.match(from_to_regex, str)
			return (float(match[1]), float(match[2]))

		elif re.match(up_to_regex, str):
			return (0, float(re.match(up_to_regex, str)[1]))

		elif re.match(over_regex, str):
			return (float(re.match(over_regex, str)[1]), None)

		else:
			return (0, None)

	@staticmethod
	def parseBusResults(results):
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
		data = DataGovService.getResource(DataGovService.FEEDER_BUS_RESOURCE_ID)
		results = data['result']['records']
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
		data = DataGovService.getResource(DataGovService.EXPRESS_BUS_RESOURCE_ID)
		results = data['result']['records']

		return {
			FareCategory.EXPRESS_BUS: DataGovService.parseBusResults(results)
		}

	@staticmethod
	def getFaresForTrunkBus():
		data = DataGovService.getResource(DataGovService.TRUNK_BUS_RESOURCE_ID)
		results = data['result']['records']

		return {
			FareCategory.TRUNK_BUS: DataGovService.parseBusResults(results)
		}

	@staticmethod
	def getFaresForMRTLRT():
		data = DataGovService.getResource(DataGovService.MRT_LRT_RESOURCE_ID)
		results = data['result']['records']

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
	def getFareTable():
		fare_table = DataGovService.getFaresForFeederBus()
		fare_table.update(DataGovService.getFaresForExpressBus())
		fare_table.update(DataGovService.getFaresForTrunkBus())
		fare_table.update(DataGovService.getFaresForMRTLRT())
		return fare_table

class LTADataMallService():
	BUS_SERVICES_API_URL = 'http://datamall2.mytransport.sg/ltaodataservice/BusServices'

	FARE_CATEGORY_MAPPING = {
		'FEEDER': FareCategory.FEEDER_BUS,
		'EXPRESS': FareCategory.EXPRESS_BUS,
		'TRUNK': FareCategory.TRUNK_BUS
	}

	@staticmethod
	def getBusServices():
		bus_service_list = []

		while True:
			r = requests.get(
				url=LTADataMallService.BUS_SERVICES_API_URL,
				headers={
					'AccountKey': LTA_API_KEY,
				},
				params={
					'$skip': len(bus_service_list)
				}
			)

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