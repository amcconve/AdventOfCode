import numpy as np


EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'


def next_seat_state(floorplan: np.array, row: int, col: int, direction: tuple, ignore_open_floor: bool):
	next_row = row + direction[0]
	next_col = col + direction[1]
	num_rows, num_cols = floorplan.shape
	if (not 0 <= next_row < num_rows) or (not 0 <= next_col < num_cols):
		return False

	next_space = floorplan[next_row][next_col]

	if ignore_open_floor and next_space == FLOOR:
		return next_seat_state(floorplan, next_row, next_col, direction, ignore_open_floor)

	return next_space


def iterate_seat(floorplan: np.array, row: int, col: int, threshold: int, ignore_open_floor: bool):
	current_state = floorplan[row][col]
	if current_state == FLOOR:
		return FLOOR, 0

	occupied_neighbors = 0
	for direction in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
		next_seat = next_seat_state(floorplan, row, col, direction, ignore_open_floor)
		if next_seat == OCCUPIED_SEAT:
			occupied_neighbors += 1

	if current_state == EMPTY_SEAT and occupied_neighbors == 0:
		return OCCUPIED_SEAT, 1

	if current_state == OCCUPIED_SEAT and occupied_neighbors >= threshold:
		return EMPTY_SEAT, 1

	return current_state, 0


def iterate_floorplan(floorplan: np.array, threshold: int, ignore_open_floor: bool):
	new_floorplan = floorplan.copy()
	num_rows, num_cols = floorplan.shape
	num_changes = 0
	occupied_seats = 0

	for row in range(num_rows):
		for col in range(num_cols):
			new_floorplan[row, col], changed = iterate_seat(floorplan, row, col, threshold, ignore_open_floor)
			if new_floorplan[row][col] == OCCUPIED_SEAT:
				occupied_seats += 1
			num_changes += changed

	return new_floorplan, num_changes, occupied_seats


def find_stable_floorplan(floorplan: np.array, threshold: int, ignore_open_floor: bool):
	num_iterations = 0
	while True:
		floorplan, num_changes, occupied_seats = iterate_floorplan(floorplan, threshold, ignore_open_floor)
		if num_changes == 0:
			break

		num_iterations += 1

	return floorplan, num_iterations, occupied_seats


def load_initial_floorplan(test: bool = False):
	input_file = open(F'./Inputs/Input2020Dec11{"Test" if test else ""}.txt')
	floorplan = []
	for line in input_file:
		floorplan.append(list(line.strip('\n')))

	return np.array(floorplan, dtype='U1')


if __name__ == '__main__':
	initial_floorplan = load_initial_floorplan(test=False)

	info_str = 'With a threshold of {} and{} using sightlines,'
	info_str += 'seating stablized with {} seats occupied after {} iterations.'

	thresh = 4
	use_sightlines = False
	final_floorplan, num_iter, num_occ = find_stable_floorplan(initial_floorplan, thresh, use_sightlines)
	print(info_str.format(thresh, "" if use_sightlines else " not", num_occ, num_iter))

	thresh = 5
	use_sightlines = True
	final_floorplan, num_iter, num_occ = find_stable_floorplan(initial_floorplan, thresh, use_sightlines)
	print(info_str.format(thresh, "" if use_sightlines else " not", num_occ, num_iter))
