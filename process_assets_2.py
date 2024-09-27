import argparse
import os
import re
import sys

parser = argparse.ArgumentParser(description='Process Pokémon GO assets into a CSV.')
parser.add_argument('-a', '--asset_path', help='Path to the directory containing Pokemon asset icons')
parser.add_argument('-p', '--previous_csv', help='Path to a previous CSV containing partial data')

args = parser.parse_args()

_FILENAME_RE = re.compile(r'^pm(?P<num>\d+)(?:\.f(?P<form>[^.]*))?(?:\.c(?P<costume>[^.]*))?(?P<gender>\.g2)?(?P<shiny>\.s)?\.icon\.png$')


class RawPokedexEntry:
	def __init__(self, num, form, costume, gender, shiny, filename):
		self.num = num
		self.form = form
		self.costume = costume
		self.gender = gender
		self.shiny = shiny
		self.filename = filename

	def to_csv_row(self):
		return f'{self.key()},{self.num},{self.gender},{self.form},{self.costume},{"shiny" if self.shiny else ""},https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Pokemon%20-%20256x256/Addressable%20Assets/{self.filename}'

	def key(self):
		return f'{self.num}_{"d" if self.gender == "" else "f"}_{self.form}_{self.costume}_{"s" if self.shiny else "n"}'

	def parse(filename):
		result = _FILENAME_RE.match(filename)
		if not result:
			return None

		num = int(result['num'])
		form = result['form'] or ''
		costume = result['costume'] or ''
		gender = '' if not result['gender'] else 'female'
		shiny = bool(result['shiny'])
		return RawPokedexEntry(num, form, costume, gender, shiny, filename)


print('key,num,form,costume,gender,shiny,url')

for filename in sorted(os.listdir(args.asset_path)):
	entry = RawPokedexEntry.parse(filename)
	if not entry:
		continue

	print(entry.to_csv_row())
	# result = _FILENAME_RE.match(filename)
	# if not result:
	# 	print(filename)
	# 	continue

	# num = result['num']
	# form = result['form'] or ''
	# costume = result['costume'] or ''
	# gender = 'default' if not result['gender'] else 'female'
	# shiny = 'shiny' if result['shiny'] else ''

	# print(f'{pokedex},{gender},{form},{costume},{shiny},{filename}')

