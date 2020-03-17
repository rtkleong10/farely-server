"""
This module contains the unit testing for the control classes.
"""

from django.test import TestCase
from farely_api.enum import FareType, TravelMode
from farely_api.entity import DirectionStep
from farely_api.control import FareController, FindRoutesController

__all__ = {
	'FareControllerTest',
	'RouteControllerTest',
}

class RouteControllerTest(TestCase):
	pass

class FareControllerTest(TestCase):
	def setUp(self):
		self.fare_controller = FareController()

	def test_empty_route(self):
		fare = self.fare_controller.calculateFare(
			fare_type=FareType.ADULT,
			direction_steps=[],
		)

		self.assertEqual(fare, 0)

	def test_walking_route(self):
		fare = self.fare_controller.calculateFare(
			fare_type=FareType.ADULT,
			direction_steps=[
				DirectionStep(
					distance=2.3,
					travel_mode=TravelMode.WALK
				)
			],
		)

		self.assertEqual(fare, 0)

	def test_mrt_bus_route(self):
		fare = self.fare_controller.calculateFare(
			fare_type=FareType.STUDENT,
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
		fare = self.fare_controller.calculateFare(
			fare_type=FareType.ADULT,
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
		fare = self.fare_controller.calculateFare(
			fare_type=FareType.ADULT,
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