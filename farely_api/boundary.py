from datetime import datetime
import requests
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
	DATA_GOV_API_URL = 'https://data.gov.sg/api/action/datastore_search'
	FEEDER_BUS_RESOURCE_ID = '310d0e0a-892f-48c4-abda-bfbdded8cb21'
	EXPRESS_BUS_RESOURCE_ID = '32cf2f0a-7790-40f0-a6cd-929697edd3b8'
	TRUNK_BUS_RESOURCE_ID = '7a5c22f0-71da-4c24-b419-84322b54ce17'
	MRT_LRT_RESOURCE_ID = 'e496ae38-989e-4eac-977d-e64c9e91a20f'

	@staticmethod
	def getResults(resource_id):
		r = requests.get(
			url=DataGovService.DATA_GOV_API_URL,
			params={
				'resource_id': resource_id
			}
		)

		return r.json()

	@staticmethod
	def getFaresForFeederBus():
		return DataGovService.getResults(DataGovService.FEEDER_BUS_RESOURCE_ID)

	@staticmethod
	def getFaresForExpressBus():
		return DataGovService.getResults(DataGovService.EXPRESS_BUS_RESOURCE_ID)

	@staticmethod
	def getFaresForTrunkBus():
		return DataGovService.getResults(DataGovService.TRUNK_BUS_RESOURCE_ID)

	@staticmethod
	def getFaresForMRTLRT():
		return DataGovService.getResults(DataGovService.MRT_LRT_RESOURCE_ID)


class LTADataMallService():
	BUS_SERVICES_API_URL = 'http://datamall2.mytransport.sg/ltaodataservice/BusServices'

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
			category = bus_service[1]
			bus_service_dict[service_no] = category

		return bus_service_dict