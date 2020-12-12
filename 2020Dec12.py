from collections import namedtuple
from enum import Enum
import cmath
import numpy as np
import re


EvasiveAction = namedtuple('EvasiveAction', ['dir', 'amt'])
Direction = namedtuple('Direction', ['N', 'E', 'S', 'W', 'L', 'R', 'F'])


class CardinalDirection(Enum):
	N = 0
	E = 1
	S = 2
	W = 3


class Ship(object):
	def __init__(self, use_waypoints=True):
		self.location = np.array([0, 0])
		self.waypoint = np.array([10, 1])
		self.facing = CardinalDirection.E

		self.naive_evasions = Direction(
			L=self.turn_left,
			R=self.turn_right,
			F=self.go_forward,
			N=self.go_north,
			E=self.go_east,
			S=self.go_south,
			W=self.go_west,
		)

		self.waypoint_evasions = Direction(
			L=self.rotate_waypoint_left,
			R=self.rotate_waypoint_right,
			F=self.go_to_waypoint,
			N=self.move_waypoint_north,
			E=self.move_waypoint_east,
			S=self.move_waypoint_south,
			W=self.move_waypoint_west,
		)

		self.evasions = self.waypoint_evasions if use_waypoints else self.naive_evasions

	def __repr__(self):
		return F'Ship(loc={self.location[0], self.location[1]}, waypoint={self.waypoint[0], self.waypoint[1]})'

	def __str__(self):
		return F'Ship(loc={self.location[0], self.location[1]}, waypoint={self.waypoint[0], self.waypoint[1]})'

	def go_north(self, amt: int):
		self.location[1] += amt

	def go_east(self, amt: int):
		self.location[0] += amt

	def go_south(self, amt: int):
		self.location[1] -= amt

	def go_west(self, amt: int):
		self.location[0] -= amt

	def turn(self, amt: int):
		if amt % 90 != 0:
			raise Exception(F'Only able to turn in increments of 90 degrees. Received {amt}')

		amt = amt // 90
		self.facing = CardinalDirection((self.facing.value + amt) % 4)

	def turn_left(self, amt: int):
		self.turn(-amt)

	def turn_right(self, amt: int):
		self.turn(amt)

	def go_forward(self, amt: int):
		evasive_action = getattr(self.evasions, self.facing.name)
		evasive_action(amt)

	def move_waypoint_north(self, amt: int):
		self.waypoint[1] += amt

	def move_waypoint_east(self, amt: int):
		self.waypoint[0] += amt

	def move_waypoint_south(self, amt: int):
		self.waypoint[1] -= amt

	def move_waypoint_west(self, amt: int):
		self.waypoint[0] -= amt

	def rotate_waypoint(self, amt: int):
		if amt % 90 != 0:
			raise Exception(F'Only able to turn in increments of 90 degrees. Received {amt}')

		sign = 1 if amt >= 0 else -1
		mag = (amt * sign) // 90

		for i in range(mag):
			self.waypoint[0], self.waypoint[1] = self.waypoint[1] * sign, -self.waypoint[0] * sign

	def rotate_waypoint_right(self, amt: int):
		self.rotate_waypoint(amt)

	def rotate_waypoint_left(self, amt: int):
		self.rotate_waypoint(-amt)

	def go_to_waypoint(self, amt: int):
		self.location += (self.waypoint * amt)

	def evade(self, action: EvasiveAction):
		evasive_action = getattr(self.evasions, action.dir)
		evasive_action(action.amt)


def perform_evasive_actions(ship: Ship, evasive_actions: tuple):
	for evasive_action in evasive_actions:
		ship.evade(evasive_action)


def load_evasive_actions(test: bool = False):
	input_file = open(F'./Inputs/Input2020Dec12{"Test" if test else ""}.txt').read()
	regex = r'(\w)(\d+)(\Z|\n)'  # TODO: Shouldn't need to return the '\n' as the thirst item in the group
	action_strs = re.findall(regex, input_file)

	return tuple([EvasiveAction(dir=act[0].upper(), amt=int(act[1])) for act in action_strs])


if __name__ == '__main__':
	ferry = Ship(use_waypoints=True)
	list_of_actions = load_evasive_actions(test=False)
	perform_evasive_actions(ferry, list_of_actions)
	manhattan = np.sum(np.abs(ferry.location))
	location = ferry.location[0], ferry.location[1]
	print(F'Final location of the ferry is {location} and total manhattan distance is {manhattan}.')
	pass
