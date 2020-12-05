def load_hill():
	input_file = open('./Inputs/Input2020Dec03.txt')
	hill = []
	num_chars = -1
	for line in input_file:
		row = str(line.rstrip('\n').strip())
		if 0 < num_chars != len(row):
			raise Exception('Unexpected length of line.')

		num_chars = len(row)
		hill.append(row)

	return tuple(hill)


def is_tree(hill: tuple, x: int, y: int):
	row = hill[y]
	char = row[x]
	if char == '#':
		return True

	if char == '.':
		return False

	raise Exception(F'Unknown character: {char}')


def count_trees(hill: tuple, dx: int, dy: int):
	if not len(hill):
		return 0

	x, y = 0, 0
	max_x = len(hill[0])
	num_trees = 0

	while y < len(hill):
		if is_tree(hill, x, y):
			num_trees += 1

		x += dx
		x = x % max_x  # Pattern repeats itself
		y += dy

	return num_trees


def count_many_trees(hill: tuple, slopes: tuple):
	num_trees_arr = []
	product = 1
	for slope in slopes:
		dx, dy = slope
		num_trees = count_trees(hill, dx, dy)
		product *= num_trees
		num_trees_arr.append(num_trees)

	return num_trees_arr, product


if __name__ == '__main__':
	hill_input = load_hill()
	num_trees_part1 = count_trees(hill_input, 3, 1)
	print(F'Part 1: Hit {num_trees_part1} trees on the way down')

	all_slopes = (
		(1, 1),
		(3, 1),
		(5, 1),
		(7, 1),
		(1, 2),
	)

	all_trees, solution = count_many_trees(hill_input, all_slopes)
	all_trees_str = ' x '.join([str(x) for x in all_trees])
	print(F'Part 2: Hit {all_trees_str} on the way down. Product = {solution}.')
