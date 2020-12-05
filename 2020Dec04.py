from collections import namedtuple
import re

# === Passport Fields ===
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
PassportData = namedtuple('PassportData', ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])


def create_passport(raw_passport_str: str):
	regex = '(\w+):(\S+)'
	passport_dict = {k: v for k, v in re.findall(regex, raw_passport_str)}

	return passport_dict


def byr_valid(value: str):
	if not re.match(r'^\d{4}$', value):
		return False

	year = int(value)
	return 1920 <= year <= 2002


def iyr_valid(value: str):
	if not re.match(r'^\d{4}$', value):
		return False

	year = int(value)
	return 2010 <= year <= 2020


def eyr_valid(value: str):
	if not re.match(r'^\d{4}$', value):
		return False

	year = int(value)
	return 2020 <= year <= 2030


def hgt_valid(value: str):
	regex_match = re.fullmatch(r'^(\d+)(in|cm)$', value, re.IGNORECASE)
	if not regex_match:
		return False

	hgt, unit = regex_match.groups()
	hgt = int(hgt)
	if unit.lower() == 'in':
		return 59 <= hgt <= 76

	if unit.lower() == 'cm':
		return 150 <= hgt <= 193

	return False


def hcl_valid(value: str):
	return re.fullmatch(r'^#[a-f\d]{6}$', value)


def ecl_valid(value: str):
	return value.lower() in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def pid_valid(value: str):
	return re.fullmatch(r'^\d{9}$', value)


def cid_valid(value: any):
	return True  # CID optional, so always valid


ValidationFunctions = PassportData(
	byr=byr_valid,
	iyr=iyr_valid,
	eyr=eyr_valid,
	hgt=hgt_valid,
	hcl=hcl_valid,
	ecl=ecl_valid,
	pid=pid_valid,
	cid=cid_valid
)


def is_passport_valid(passport: dict):
	for field in PassportData._fields:
		if field not in passport.keys() and field != 'cid':
			return False

		value = passport.get(field, None)  # Default value for 'cid'
		validation_function = getattr(ValidationFunctions, field)
		if not validation_function(value):
			return False

	return True


def load_all_passports(test: bool = False):
	test_str = 'Test' if test else ''
	input_file = open(F'./Inputs/Input2020Dec04{test_str}.txt')
	all_passport_str = input_file.read().split('\n\n')

	return [create_passport(passport_str) for passport_str in all_passport_str]


if __name__ == '__main__':
	all_passports = load_all_passports(test=False)
	validity = [is_passport_valid(passport) for passport in all_passports]
	print(F'{sum(validity)} of {len(all_passports)} passports are valid')
