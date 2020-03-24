"""Contains the unit testing for the control classes.
"""

from django.test import TestCase
from farely_api.enum import FareType, TravelMode
from farely_api.entity import DirectionStep
from farely_api.control import FareController, FareControllerFactory

__all__ = {
	'FareControllerTest',
}

class FareControllerTest(TestCase):
	def setUp(self):
		self.FareControllerFactory= FareControllerFactory()

	def test_empty_route(self):
		fare_type = FareType.ADULT
		self.fare_controller = self.FareControllerFactory.getFareController(fare_type)
		fare = self.fare_controller.calculate_fare(
			fare_type,
			direction_steps=[],
		)

		self.assertEqual(fare, 0)

	def test_walking_route(self):
		fare_type = FareType.ADULT
		self.fare_controller = self.FareControllerFactory.getFareController(fare_type)
		fare = self.fare_controller.calculate_fare(
			fare_type,
			direction_steps=[
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.WALK
				)
			],
		)

		self.assertEqual(fare, 0)

	def test_mrt_bus_route(self):
		fare_type = FareType.STUDENT
		self.fare_controller = self.FareControllerFactory.getFareController(fare_type)
		fare = self.fare_controller.calculate_fare(
			fare_type,
			direction_steps=[
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.BUS,
					line="161"
				),
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.MRT_LRT
				),
			],
		)

		self.assertEqual(fare, 0.52)

	def test_invalid_travel_mode(self):
		fare_type = FareType.ADULT
		self.fare_controller = self.FareControllerFactory.getFareController(fare_type)
		fare = self.fare_controller.calculate_fare(
			fare_type,
			direction_steps=[
				DirectionStep(
					distance=2.3,
					travel_mode=4, # Invalid travel mode
					line="161"
				),
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.MRT_LRT
				),
			],
		)

		self.assertEqual(fare, None)

	def test_missing_line(self):
		fare_type = FareType.ADULT
		self.fare_controller = self.FareControllerFactory.getFareController(fare_type)
		fare = self.fare_controller.calculate_fare(
			fare_type,
			direction_steps=[
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.BUS,
				),
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.MRT_LRT
				),
			],
		)

		self.assertEqual(fare, None)