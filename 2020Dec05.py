from collections import namedtuple
from operator import attrgetter
import re

Seat = namedtuple('Seat', ['row', 'col', 'seat_id'])


def seat_from_str(seat_str: str) -> Seat:
	regex_match = re.fullmatch(r'^([F|B]{7})([L|R]{3})$', seat_str, re.IGNORECASE)
	if not regex_match or len(regex_match.groups()) != 2:
		raise Exception(F'Unexpected format of seat string: {seat_str}.')

	row_str, col_str = regex_match.groups()

	# Turn columns into binary strings. Python's 'int' can convert directally from binary.
	row = int(row_str.lower().replace('f', '0').replace('b', '1'), base=2)
	col = int(col_str.lower().replace('l', '0').replace('r', '1'), base=2)

	return Seat(row=row, col=col, seat_id=(8*row + col))


def get_seats(test=False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec05{test_str}.txt')
	return [seat_from_str(seat_str.rstrip('\n')) for seat_str in input_file.readlines()]


def find_open_seat(all_seats: list):
	if len(all_seats) < 2:
		raise Exception('Fewer than 2 seats. Unable to find missing seat.')
	all_seats.sort(key=attrgetter('seat_id'))  # Sort by seat id
	for i in range(len(all_seats)-1):
		seat, next_seat = all_seats[i], all_seats[i+1]
		if seat.seat_id + 2 == next_seat.seat_id:
			my_seat_id = seat.seat_id + 1
			col = my_seat_id // 8
			row = my_seat_id % 8
			return Seat(row=row, col=col, seat_id=my_seat_id)

	raise Exception('Unable to find missing seat.  No consecutive two seat ids differ by exactly 2.')


if __name__ == '__main__':
	all_seats = get_seats()
	open_seat = find_open_seat(all_seats)
	max_id = max([seat.seat_id for seat in all_seats])
	print(all_seats)
	print(F'The max seat ID among the {len(all_seats)} seats is {max_id}.')
	print(F'My seat is {open_seat}.')
	pass
