"""Contains the integration testing for the API Views.
"""

from rest_framework.test import APIRequestFactory, APITestCase
from farely_api.apis import FindRoutesApi
from rest_framework import status
from farely_api.enum import FareType

__all__ = {
	'FindRoutesApiTest',
}

class FindRoutesApiTest(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()

	def test_for_fare_and_checkpoints(self):
		data = {
			"fare_type": 1,
			"origin": "NTU",
			"destination": "Boon Lay",
		}

		request = self.factory.get('/api/find-routes/', data)
		view = FindRoutesApi.as_view()
		response = view(request)

		self.assertTrue(status.is_success(response.status_code))
		self.assertTrue(all(["fare" in route["legs"][0] for route in response.data["routes"]]))
		self.assertTrue(all(["checkpoints" in route["legs"][0] for route in response.data["routes"]]))

	def test_different_fare_types(self):
		for fare_type in FareType.choices():
			data = {
				"fare_type": fare_type[0],
				"origin": "NTU",
				"destination": "Boon Lay",
			}

			request = self.factory.get('/api/find-routes/', data)
			view = FindRoutesApi.as_view()
			response = view(request)
			self.assertTrue(status.is_success(response.status_code))

	def test_out_of_singapore(self):
		data = {
			"fare_type": 1,
			"origin": "NTU",
			"destination": "New York University",
		}

		request = self.factory.get('/api/find-routes/', data)
		view = FindRoutesApi.as_view()
		response = view(request)

		self.assertTrue(status.is_client_error(response.status_code))