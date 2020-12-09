from enum import Enum
import re


class Operation(Enum):
	nop = 1
	acc = 2
	jmp = 3


class Instruction(object):
	def __init__(self, op: Operation, arg: int, idx: int):
		self.op = op
		self.arg = arg
		self.idx = idx
		self.traversed = False

	def __str__(self):
		return F"Instruction({self.op.name} {'+' if self.arg >= 0 else ''}{self.arg})"

	def __repr__(self):
		return self.__str__()


def load_all_instructions(test: bool = False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec08{test_str}.txt')

	instructions = []
	idx = 0
	for line in input_file:
		regex = r'^(nop|acc|jmp) ([+|-]\d+)\n?$'  # Optional new line at end of line
		op_str, arg_str = re.fullmatch(regex, line).groups()
		instructions.append(Instruction(op=getattr(Operation, op_str), arg=int(arg_str), idx=idx))
		idx += 1

	return tuple(instructions)


def traverse_instruction_list(instructions: tuple):
	idx = 0
	accumulator = 0
	last_node = None

	while True:
		if idx >= len(instructions) or idx < 0:
			break
		node = instructions[idx]
		if node.traversed:
			break

		if node.op == Operation.nop:
			idx += 1
		if node.op == Operation.acc:
			accumulator += node.arg
			idx += 1
		if node.op == Operation.jmp:
			idx += node.arg

		node.traversed = True
		last_node = node

	success = idx >= len(instructions) and last_node.idx == len(instructions) - 1

	return success, last_node, accumulator


def modify_instruction_list(instructions: tuple):

	for i in range(len(instructions)):
		node = instructions[i]
		orig_op = node.op
		new_op = orig_op

		if orig_op == Operation.nop:
			new_op = Operation.jmp
		if orig_op == Operation.jmp:
			new_op = Operation.nop

		node.op = new_op

		for inst in instructions:
			inst.traversed = False

		test_success, test_last_node, test_accummulator = traverse_instruction_list(instructions)
		if test_success:
			return test_success, node, test_accummulator

		node.op = orig_op

	raise Exception('Unable to find modification that causes function to terminate')


if __name__ == '__main__':
	instruction_list = load_all_instructions(test=False)
	succeeded, last_inst, final_accumulator = traverse_instruction_list(instruction_list)
	test_succeeded, modified, test_accumulator = modify_instruction_list(instruction_list)
	pass
	# my_bag = all_bags[my_bag_color]
	# bags_inside = count_bags_inside(my_bag)
	# print(F'A {my_bag_color} may be inside {len(my_bag.contained_in)} different color bags.')
	# print(F'There are {bags_inside} bags inside my {my_bag_color} bag.')
