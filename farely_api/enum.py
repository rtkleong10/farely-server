"""Contains the enumeration classes for the Farely API.
"""

from enum import IntEnum

__all__ = [
	'FareCategory',
	'FareType',
	'TravelMode'
]

class FareCategory(IntEnum):
	"""Represents the fare categories for calculating the fare of different transit modes
	"""
	MRT_LRT = 1
	"""MRTs and LRTs."""
	WALK = 2
	"""Walking."""
	FEEDER_BUS = 3
	"""Feeder buses."""
	EXPRESS_BUS = 4
	"""Expresses buses."""
	TRUNK_BUS = 5
	"""Trunk buses."""
	NIGHT_BUS = 6
	"""Night bus and night riders."""
	FLAT_FARE_2_BUS = 7
	"""Flat fare $2 buses."""

class FareType(IntEnum):
	"""Represents the fare types of the user to calculate the fare for
	"""
	WORKFARE = 1
	"""Workfare transport concession card fare."""
	STUDENT = 2
	"""Student card fare."""
	SINGLE_TRIP = 3
	"""Single trip."""
	SENIOR_CITIZEN = 4
	"""Senior citizen card fare."""
	PERSONS_WITH_DISABILITIES = 5
	"""Persons with disabilities card fare."""
	ADULT = 6
	"""Adult card fare."""

	@classmethod
	def choices(cls):
		"""Returns the choices of fare types.

		Returns:
			choices (tuple): Returns the choices of fare types as a tuple `(value, key)`. `value` is the `int` representation of the fare type and `key` if the `farely_api.enum.FareType` representation of the fare type.
		"""
		return [(key.value, key) for key in cls]

class TravelMode(IntEnum):
	"""Represents the travel modes.
	"""
	BUS = 1
	"""Buses."""
	MRT_LRT = 2
	"""MRTs and LRTs."""
	WALK = 3
	"""Walking."""