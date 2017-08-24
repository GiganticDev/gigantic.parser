# encoding: utf-8

import os
import configparser
import tempfile
import json
import time

from bson.json_util import dumps


from gigantic.dao.model import *


log = __import__('logging').getLogger(__name__)

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
	f = open(file_name, "rb")
	u = f.read().decode("utf-16le").encode("utf-8")
	f.close()
	fp = tempfile.TemporaryFile()
	fp.write(u)
	fp.seek(0)
	
	# ConfigParser ultimately wants ascii
	config.read_string(fp.read().decode("ascii", "ignore"))
	fp.close()
	return config


def parse_file(file_name):
	"""
	Instantiate python objects in memory from the config files.
	Returns the data in a set which reprents the hero and their skills.
	"""
	
	
	# Section names in the gigantic files are in the format [ResourceID RxSkillProvider] where the string after
	# space is the object type, and the string before is the ResourceID. The ResourceID is normally redundantly
	# defined within the section as well.
	log.info("Parsing hero file {0}".format(file_name))
	config = get_hero_config(file_name)
	if not config:
		raise ValueError()
	
	sections = config.sections()
	for section in sections:
		res, _, res_type = section.partition(' ')
		if len(res_type) <= 0: # Make sure this is actually a resource section and not something like Core.System
			continue
		
		resource = dict(config.items(section))

		# Add resources to our basic hero set
		try:
			cls = Resource.__map__[res_type]
		except KeyError:
			pass
			# print(resource)
			# log.warn("Found un-known section " + res_type);
		else:
			inst = cls(resource)


def parse_heroes(directory='Config/Heroes'):
	"""
	Loops all files found in `directory` and attempts to parse them into the "Models". Returns a list consisting of
	sets each representing a hero.
	"""
	hero_files = os.listdir(directory)
	if len(hero_files) == 0:
		print("Found no hero config files")
		return
	
	os.chdir(directory)
	
	for f in hero_files:
		if '.DS_Store' in f: continue
		try:
			parse_file(f)
		except ValueError:
			pass
	
	for section, Res in Resource.__map__.items():
		for id, instance in Res.__dataset__.items():
			log.debug(instance)
	
	# Get skills for Adept, aka Aisling, to test timing of naive list comprehension filtering
	before = time.time()
	skills = [skill for skill in Skill.__dataset__.values() if skill.hero == 'Adept']
	after = time.time()
	# print("Fetched {0} skills for Aisling in {1:.3f}ms".format(len(skills), (after-before)*1000))
	# for skill in skills:
	# 	print(dumps(skill))
