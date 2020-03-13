from rest_framework.test import APIRequestFactory, APITestCase
from farely_api.apis import FindRoutesApi

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

		self.assertTrue(all(["fare" in route["legs"][0] for route in response.data["routes"]]))
		self.assertTrue(all(["checkpoints" in route["legs"][0] for route in response.data["routes"]]))