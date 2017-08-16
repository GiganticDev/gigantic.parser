# encoding: utf-8

import os
import configparser
import tempfile
import json

from .model import *


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
	config = get_hero_config(file_name)
	if not config:
		raise ValueError()

	sections = config.sections()
	hero = {'name': '', 'skills': [], 'skill_upgrades': []}

	"""
	Instantiate class object based on section name, names are like [ResourceID RxSkillProvider] where the string after
	space is the object type, and the string before is the ResourceID... but the ResourceID is also specified within
	the section so... whatever?
	"""

	for section in sections:
		res, _, res_type = section.partition(' ')
		if len(res_type) <= 0:
			continue
		try:
			Cls = class_section_map[res_type]
		except KeyError:
			continue

		resource = Cls( **{key: val for key,val in config.items(section)} )
		if isinstance(resource, Archetype):
			hero['name'] = resource.heroarchetypename
		elif isinstance(resource, Skill):
			hero['skills'].append(resource)
		elif isinstance(resource, SkillUpgrade):
			hero['skills'].append(resource)

	return hero


def parse_heroes():
	hero_files = os.listdir('Config/Heroes')
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

	print(json.dumps(heroes))


if __name__ == '__main__':
	parse_heroes()
