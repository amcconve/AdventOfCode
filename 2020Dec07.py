from collections import namedtuple
import re


Contents = namedtuple('Contents', ['bag', 'quantity'])

TRAVERSED_BAGS = []

class Bag(object):

	def __init__(self, color: str):
		self.color = color
		self.contents = tuple()
		self.contained_in = []
		self.traversed = False

	def __str__(self):
		return F"Bag(color='{self.color}')"

	def __repr__(self):
		return self.__str__()


def update_contained_in(outer_bag: Bag, inner_bag: Bag):
	if outer_bag is inner_bag or outer_bag in inner_bag.contained_in:
		return

	inner_bag.contained_in.append(outer_bag)
	for inner_color in inner_bag.contents:
		update_contained_in(outer_bag, inner_color.bag)


def populate_contained_in_fields(all_bags: dict):
	for color, outer_bag in all_bags.items():
		for outer_bag_contents in outer_bag.contents:
			update_contained_in(outer_bag, outer_bag_contents.bag)


def load_all_bags(test: bool = False, test_case: int = 1):
	test_str = ''
	if test:
		test_str += 'Test'
		if test_case > 1:
			test_str += str(test_case)
	input_file = open(F'./Inputs/Input2020Dec07{test_str}.txt')

	all_bags = {}
	for line in input_file:
		line = line.rstrip('\n')

		start_regex = r'(^[a-z]+ [a-z]+)'
		rule_regex = r'(\d+) ([a-z]+ [a-z]+) bags?[,|.]'
		bag_color = re.findall(start_regex, line)[0]
		bag = all_bags.get(bag_color, None)
		if bag is None:
			bag = Bag(bag_color)
			all_bags[bag_color] = bag

		raw_contents = re.findall(rule_regex, line)
		all_contents = []
		for raw_content in raw_contents:
			inner_bag_color = raw_content[1]
			inner_bag = all_bags.get(inner_bag_color, None)
			if inner_bag is None:
				inner_bag = Bag(inner_bag_color)
				all_bags[inner_bag_color] = inner_bag

			all_contents.append(Contents(bag=inner_bag, quantity=int(raw_content[0])))

		bag.contents = tuple(all_contents)

	# TODO: Populate as I go.  Updated contained in list when I see new rules, and when I update contents.
	populate_contained_in_fields(all_bags)

	return all_bags


def count_bags_inside(bag: Bag):
	bags_inside = 0
	for color in bag.contents:
		bags_inside += color.quantity * (1 + count_bags_inside(color.bag))

	return bags_inside


if __name__ == '__main__':
	my_bag_color = 'shiny gold'
	all_bags = load_all_bags(test=False)
	my_bag = all_bags[my_bag_color]
	bags_inside = count_bags_inside(my_bag)
	print(F'A {my_bag_color} may be inside {len(my_bag.contained_in)} different color bags.')
	print(F'There are {bags_inside} bags inside my {my_bag_color} bag.')
