import argparse
import os
import re
import sys

parser = argparse.ArgumentParser(description='Process Pokémon GO assets into a CSV.')
parser.add_argument('-i', '--icon_path', help='Path to the directory containing Pokemon icons')
parser.add_argument('-p', '--previous_csv', help='Path to a previous CSV containing partial data')

args = parser.parse_args()

_ICON_RE = re.compile(r'pokemon_icon_(?:pm(?P<long_pokedex>\d{4})_(?P<long_gender>\d{2})(?:_pikachu)_pgo_(?P<long_form>[_]*?)|(?P<short_pokedex>\d{3})(?:_(?P<short_gender>(?:00|01)))?(?:_(?P<short_form>\d{2}(?:_\d{2})?)))?)(?P<shiny>_shiny)?\.png$')

_VARIANT_RE = re.compile(r'(\d{2})(?:_(\d{2}))')

_BULBASUAR_COSTUMES = {
	'11': 'Red Hat',
	'14': 'Pikachu Hat',
}

_CHARMANDER_COSTUMES = {
	'11': 'Red Hat',
	'14': 'Pikachu Hat',
}

_SQUIRTLE_COSTUMES = {
	'05': 'Sunglasses',
	'11': 'Red Hat',
	'14': 'Pikachu Hat',
}

_RATICATE_COSTUMES = {
	'11': 'Party Hat',
}

_PONYTA_COSTUMES = {
	'47': ''
}

# Costumes for Pikachu and its evolution chain.
_PIKACHU_COSTUMES = {
	'01': 'Christmas Hat',
	'02': 'Party Hat',
	'03': 'Trainer Hat',
	'04': 'Witch Hat',
	'05': 'Safari Hat',
	'06': 'Fragment Hat',
	'07': 'Flower',
	'08': 'Beanie Hat',
	'09': 'Detective',
	'10': 'Straw Hat',
	'11': 'Red Hat',
	'12': 'Easter Hat',
	'13': 'Black Hat',
	'16': 'Luchador',
	'22': 'Charizard Hat',
	'23': 'Umbreon Hat',
	'24': 'Rayquaza Hat',
	'25': 'Lucario Hat',
	'27': 'Worlds Hat',
	'28': 'Purple Hat',
	'47': 'Shaymin Hat',
	'4thanniversary': 'Balloon',
	'5thanniversary': '5th Anniversary Balloon',
	'fall2019': 'Mimikyu',
	'movie2020': 'Wailmer Pouch',
	'popstar': 'Pop Star',
	'rockstar': 'Rock Star',
	'winter2020': 'Winter Coat',
	'kariyushi': 'Kariyushi',
}

_CASTFORM_FORMS = 

def to_gender(s):
	#return 'male' if s == '00' else 'female'
	return '' if not s or s == '00' else 'female'

def to_form_and_aesthetic_str(variant_str):
	result = _VARIANT_RE.match(variant_str)
	if not result:
		return '', ''
	elif result.group(2):
		return result.group(1), result.group(2)
	else:
		return result.group(1), result.group(1)

def to_variant(pokedex, variant_str):
	if not variant_str:
		return '', ''

	variant_str_parts = variant_str.split('_') if variant_str else ['']

	aesthetic = ''
	form = ''

	match pokedex:
		case 1 | 2 | 3:
			# Bulbasaur, Ivysaur, Venusaur
			aesthetic = _BULBASAUR_COSTUMES[variant_str_parts[0]] or ''
		case 4 | 5 | 6:
			# Charmander, Charmeleon, Charizard:
			aesthetic = _CHARIZARD_COSTUMES[variant_str_parts[0]] or ''
		case 7 | 8 | 9:
			# Squirtle, Wartortle, Blastoise:
			aesthetic = _SQUIRTLE_COSTUMES[variant_str_parts[0]] or ''
		case 172 | 25 | 26:
			# Pichu, Pikachu, Raichu
			aesthetic = _PIKACHU_COSTUMES[variant_str_parts[0]] or ''
		case 201:
			# Unown
			match variant_str_parts[0]:
				case '37':
					aesthetic = '!'
				case '38':
					aesthetic = '?'
				case _:
					aesthetic = chr(ord('A') + int(variant_str_parts[0]) - 11)
		case 327:
			# Spinda
			spinda_number = int(variant_str_parts[0]) + 1
			if spinda_number > 1:
				spinda_number = spinda_number - 10
			aesthetic = str(spinda_number)


for f in sorted(os.listdir(args.icon_path)):
	result = _ICON_RE.match(f)
	if not result:
		continue

	long_form = ''
	short_form = ''

	if result.group('long_pokedex'):
		pokedex = int(result.group('long_pokedex'))
		gender = to_gender(result.group('long_gender'))
		long_form = result.group('long_form')
	elif result.group('short_pokedex'):
		pokedex = int(result.group('short_pokedex'))
		gender = to_gender(result.group('short_gender'))
		short_form = result.group('short_form') or ''

	shiny = 'shiny' if result.group('shiny') else ''

	print(f'{pokedex},{gender},{short_form},{long_form},{shiny},{f}')
