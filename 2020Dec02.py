from collections import namedtuple
import re

Rule = namedtuple('Rule', ['character', 'min', 'max'])
TestCase = namedtuple('TestCase', ['password', 'rule'])

def load_test_cases():
	input_file = open('./Inputs/Input2020Dec02.txt')
	test_cases = []
	for line in input_file:
		line = line.rstrip('\n')
		line_split = line.split(':')
		if len(line_split) != 2:
			raise Exception('Unable to parse input.  Not in format "rule: password"')
		rule_str, password = line_split
		rule_str = rule_str.strip()
		password = password.strip()
		
		rule_str_split = rule_str.split(' ')
		if len(rule_str_split) != 2:
			raise Exception('Unable to parse rule.  Not in format "min-max letter".')
			
		minmax_str, char_str = rule_str_split
		char_str.strip()
		
		if len(char_str) > 1:
			raise Exception(F'More than one character provided in rule: {char_str}')
		

		minmax_str_split = minmax_str.split('-')
		if len(minmax_str_split) != 2:
			raise Exception('Unable to parse minmax.  Not in format "min-max".')
		
		min_str, max_str = minmax_str_split
		
		rule = Rule(min=int(min_str), max=int(max_str), character=char_str)
		test_cases.append(TestCase(password=password, rule=rule))

	return test_cases
	

def is_password_valid_part1(test_case: TestCase):
	regex = re.compile(test_case.rule.character)
	matches = regex.findall(test_case.password)
	
	return test_case.rule.min <= len(matches) <= test_case.rule.max
	
	
def is_password_valid_part2(test_case: TestCase):
	matched_char = test_case.rule.character
	
	num_matched = 0
	if len(test_case.password) >= test_case.rule.min:
		if test_case.password[test_case.rule.min - 1] == matched_char:
			num_matched += 1
		
	if len(test_case.password) >= test_case.rule.max:
		if test_case.password[test_case.rule.max - 1] == matched_char:
			num_matched += 1
		
	return num_matched == 1
	

def num_valid_passwords_part1(test_cases: list):
	counter = 0
	for test_case in test_cases:
		if is_password_valid_part1(test_case):
			counter += 1
	
	return counter
	
	
def num_valid_passwords_part2(test_cases: list):
	counter = 0
	for test_case in test_cases:
		if is_password_valid_part2(test_case):
			counter += 1
	
	return counter


if __name__ == '__main__':
	test_cases = load_test_cases()
	num_valid1 = num_valid_passwords_part1(test_cases)
	print(F'Part 1: {num_valid1} of {len(test_cases)} are valid.')
	num_valid2 = num_valid_passwords_part2(test_cases)
	print(F'Part 2: {num_valid2} of {len(test_cases)} are valid.')


