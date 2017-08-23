# encoding: utf-8

import os
import configparser
import tempfile
import json


"""
This is all mostly testing at the moment, don't judge me.

We expect to be run via `python -m gigantic.parser` while inside the base gigantic RxGame directory. This will currently
search for all files in the RxGame/Config/Heroes directory and read the values into python memory then just dump the
data we have to json to the cli output. Again, all testing.
"""

def get_hero_config(file_name):
	# print("Parsing hero at {0}".format(file_name))
	config = configparser.ConfigParser(strict=False) # strict=False to allow duplicate keys within sections
	
	# Stupid hackiness to decode utf-16le file, encode it as utf-8, then write to temporary file to fix BOM
	u = open(file_name, "rb").read().decode("utf-16le").encode("utf-8")
	fp = tempfile.TemporaryFile()
	fp.write(u)
	fp.seek(0)
	
	# ConfigParser ultimately wants ascii
	config.read_string(fp.read().decode("ascii", "ignore"))
	return config


def parse_hero(file_name):
	"""
	Instantiate python objects in memory from the config files.
	Returns the data in a set which reprents the hero and their skills.
	"""
	
	
	# Section names in the gigantic files are in the format [ResourceID RxSkillProvider] where the string after
	# space is the object type, and the string before is the ResourceID. The ResourceID is normally redundantly
	# defined within the section as well.
	config = get_hero_config(file_name)
	if not config:
		raise ValueError()
	
	sections = config.sections()
	hero = {'name': '', 'skills': [], 'skill_upgrades': []}
	
	for section in sections:
		res, _, res_type = section.partition(' ')
		if len(res_type) <= 0: # Make sure this is actually a resource section and not something like Core.System
			continue
		
		resource = dict(config.items(section))
		
		# Add resources to our basic hero set
		if res_type == 'RxHeroProvider':
			hero['name'] = resource['heroarchetypename']
		elif res_type == 'RxSkillProvider':
			hero['skills'].append(resource)
		elif res_type == 'RxSkillUpgradeProvider':
			hero['skill_upgrades'].append(resource)
	
	return hero


def parse_heroes(directory='Config/Heroes'):
	"""
	Loops all files found in `directory` and attempts to parse them into the "Models". Returns a list consisting of
	sets each representing a hero.
	"""
	hero_files = os.listdir(directory)
	if len(hero_files) == 0:
		print("Found no hero config files")
		return
	
	heroes = []
	os.chdir('Config/Heroes')
	
	for f in hero_files:
		try:
			heroes.append(parse_hero(f))
		except ValueError:
			pass
	
	return heroes


if __name__ == '__main__':
	print(json.dumps(parse_heroes()))
