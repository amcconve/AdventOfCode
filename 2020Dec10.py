import numpy as np


def count_one_and_three_jolt_steps(arrangement: np.array):
	diffs = np.diff(arrangement)
	if np.max(diffs) > 3 or np.min(diffs) < 0:
		raise Exception(F'Received an unexpected joltage difference: min={np.min(diffs)}<0, or max={np.max(diffs)}>3.')

	return np.sum(diffs == 1), np.sum(diffs == 3)


def count_chains_reaching_max(arrangement: np.array):
	if len(arrangement) == 1:
		return 1

	num_arrangements = 0
	min_val = arrangement.min()
	if len(arrangement) > 1 and arrangement[1] <= min_val + 3:
		num_arrangements += count_chains_reaching_max(arrangement[1:])

	if len(arrangement) > 2 and arrangement[2] <= min_val + 3:
		num_arrangements += count_chains_reaching_max(arrangement[2:])

	if len(arrangement) > 3 and arrangement[3] <= min_val + 3:
		num_arrangements += count_chains_reaching_max(arrangement[3:])

	return num_arrangements


def get_subchains(arrangement: np.array):
	three_jolt_jumps = np.diff(arrangement, prepend=0) == 3
	subchains = []
	start = 0
	for end in range(1, len(arrangement)):
		if three_jolt_jumps[end]:
			subchains.append(arrangement[start: end+1])
			start = end

	return subchains


def split_and_count_chains_reaching_max(arrangement: np.array):
	num_arrangements = 1
	for subchain in get_subchains(arrangement):
		num_arrangements *= count_chains_reaching_max(subchain)

	return num_arrangements


def load_dataset(test: bool = False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec10{test_str}.txt')
	adapters = sorted([int(x) for x in input_file.read().split('\n')])

	return np.array([0] + adapters + [max(adapters) + 3])


if __name__ == '__main__':
	is_test = False
	dataset = load_dataset(test=is_test)
	one_jolt, three_jolts = count_one_and_three_jolt_steps(dataset)
	num_chains = split_and_count_chains_reaching_max(dataset)

	prod = one_jolt * three_jolts

	print(F'There are {one_jolt} one jolt jumps and {three_jolts} three jolt jumps. Their product is {prod}.')
	print(F'There are {num_chains} possible chains of adapters to get from 0 jolts to {np.max(dataset)} jolts.')
