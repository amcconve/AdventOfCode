import itertools


def create_possible_sums(data: tuple):
	possible_sums = {}
	for a, b in itertools.combinations(data, 2):
		if a == b:  # Summands must be different
			continue

		entry = a + b
		possible_sums[entry] = possible_sums.get(entry, 0) + 1

	return possible_sums


def find_weakness(data: tuple, preamble: int):
	possible_sums = create_possible_sums(data[:preamble])

	for next_idx in range(preamble, len(data)):
		next_entry = data[next_idx]
		if possible_sums.get(next_entry, 0) == 0:
			return next_entry

		first_idx = next_idx - preamble
		first_entry = data[first_idx]
		for j in range(next_idx - preamble + 1, next_idx):
			to_remove = first_entry + data[j]
			to_add = next_entry + data[j]
			possible_sums[to_remove] -= 1
			possible_sums[to_add] = possible_sums.get(to_add, 0) + 1

	raise Exception(f'Every entry is the sum of two of the previous {preamble}.')


def find_contiguous_summands(data: tuple, target: int):
	first_idx = 0
	last_idx = 1
	partial_sum = data[first_idx] + data[last_idx]

	while last_idx < len(data):
		if partial_sum == target:
			return first_idx, last_idx

		elif partial_sum < target:
			last_idx += 1
			if last_idx > len(data):  # Should never happen, otherwise we've exhausted all possibilities
				break
			partial_sum += data[last_idx]

		else:
			partial_sum -= data[first_idx]
			first_idx += 1

	raise Exception('Unable to find consecutive set of numbers summing to {target}.')


def load_dataset(test: bool = False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec09{test_str}.txt')

	return tuple([int(x) for x in input_file.read().split('\n')])


if __name__ == '__main__':
	is_test = False
	preamble_length = 5 if is_test else 25
	dataset = load_dataset(test=is_test)
	weakness = find_weakness(dataset, preamble_length)
	first, last = find_contiguous_summands(dataset, weakness)
	max_val, min_val = max(dataset[first: last + 1]), min(dataset[first: last + 1])
	print(F'{weakness} is the first number not to be sum of two numbers from the previous {preamble_length}.')
	print(F'The numbers between index {first} and index {last} (inclusive) sum to {weakness}.')
	print(F'The max and min of that range are {max_val} and {min_val}, respectively, and sum to {max_val + min_val}.')
