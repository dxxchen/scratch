"""Determines the gender of a list of names using a local CSV and genderize.io.

Usage:
  python genderize.py filename
"""

from itertools import islice
import csv
import json
import sys
import urllib2


_LOCAL_CSV_NAME = 'genders.csv'
_CHUNK_SIZE = 10


def _main(argv):
	if len(argv) != 2:
		sys.exit('Usage: python genderize.py filename')

	genders = {}
	with open(_LOCAL_CSV_NAME) as f:
		reader = csv.reader(f)
		for row in reader:
			key = row[0]
			if key in genders:
				pass
			genders[key] = row[1]

	unresolved_lines = []
	resolved_genders = {}
	with open(argv[1]) as f:
		while True:
			# Read the next lines from the file.
			next_lines = list(islice(f, _CHUNK_SIZE))
			if not next_lines:
				break

			# For each line, check to see if it is in the local gender CSV.
			for line in next_lines:
				if line.strip().upper() in genders:
					resolved_genders[line.strip()] = genders[line.strip().upper()]
				else:
					unresolved_lines.append(line)

			unresolved_lines = _resolve_from_genderize(unresolved_lines, resolved_genders)

	unresolved_lines = _resolve_from_genderize(unresolved_lines, resolved_genders)

	for (key, value) in sorted(resolved_genders.items()):
		print key + ',' + value


def _resolve_from_genderize(unresolved_lines, resolved_genders):
	if len(unresolved_lines) >= _CHUNK_SIZE:
		query_string = '&'.join(
			['name[%d]=%s' % (i,x.strip())
			 for i,x in enumerate(unresolved_lines[:_CHUNK_SIZE])])
		url = 'https://api.genderize.io/?' + query_string
		unresolved_lines = unresolved_lines[_CHUNK_SIZE:]

		try:
			response = urllib2.urlopen(url)
			if response.getcode() == 200:
				results = json.loads(repsonse.read())
				for result in results:
					resolved_genders[result['name']] = result['gender'] or 'unknown'
		except urllib2.HTTPError, e:
			sys.stderr.write('Error fetching ' + url + '\n')

	return unresolved_lines


if __name__ == '__main__':
	_main(sys.argv)