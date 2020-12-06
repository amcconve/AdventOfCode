import re


def get_unique_characters(input_str: str, ignore_whitespace: bool = True):
	"""
	Uses regex r'(.)(?=.*?\1)' to remove duplicate characters.
	Specifically, use a 'lookahead' (?=...) that take any character, specified by the 'target group' (.), and replace
	it with ''.  The .*? means anything can be in between and the match.  And we are looking to match \1, which
	specifies that we are matching the first 'target group'
	"""

	if ignore_whitespace:
		input_str = re.sub(r'[\n\t\s]*', '', input_str)

	return re.sub(r'(.)(?=.*?\1)', '', input_str)


def get_unanimous_characters(input_str: str, delim: str = '\n'):
	all_characters = get_unique_characters(input_str)
	num_groups = len(input_str.split('\n'))

	ret = ''
	for char in all_characters:
		regex = rf'(^|\n)(.*)?(?={char})'
		if num_groups == len(re.findall(regex, input_str)):
			ret += char

	return ret


def sum_unique_responses(all_responses_by_group: list):
	unique_responses_by_group = [get_unique_characters(responses) for responses in all_responses_by_group]

	return sum([len(responses) for responses in unique_responses_by_group])


def sum_unanimous_responses(all_responses_by_group: list):
	unanimous_responses = [get_unanimous_characters(responses) for responses in all_responses_by_group]

	return sum([len(responses) for responses in unanimous_responses])


def load_all_responses_by_group(test: bool = False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec06{test_str}.txt')

	return input_file.read().split('\n\n')


if __name__ == '__main__':
	all_responses = load_all_responses_by_group(test=False)

	unique = sum_unique_responses(all_responses)
	print(F'There are {unique} total unique responses.')

	unanimous = sum_unanimous_responses(all_responses)
	print(F'There are {unanimous} total unanimous responses.')
