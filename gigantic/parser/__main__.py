# encoding: utf-8

import os
import configparser
import tempfile


class Archetype(object):
	def __init__(self, file_name):
		print("Parsing hero at {0}".format(file_name))
		self._config = configparser.ConfigParser(strict=False) # strict=False to allow duplicate keys within sections

		# Stupid hackiness to decode utf-16le file, encode it as utf-8, then write to temporary file to fix BOM
		u = open(file_name, "rb").read().decode("utf-16le").encode("utf-8")
		fp = tempfile.TemporaryFile()
		fp.write(u)
		fp.seek(0)

		# ConfigParser ultimately wants ascii
		self._config.read_string(fp.read().decode("ascii", "ignore"))

		self._hero_provider = {}
		self._skill_providers = []
		self._parse()

	def _parse(self):
		if not self._config:
			raise NotImplementedError()

		sections = self._config.sections()
		for section in sections:
			if 'RxHeroProvider' in section:
				self._hero_provider = self._config[section]
			elif 'RkSkillProvider' in section or 'RxSkillUpgradeProvider' in section:
				self._skill_providers.append(self._config[section])

		# print(self._skill_providers)
		# print(self._hero_provider)

		if not self._hero_provider:
			raise ValueError()

		self._name = self._hero_provider['HeroArchetypeName']

		# print(sections)

	def __repr__(self):
		return self._name


def parse_heroes():
	hero_files = os.listdir('Config/Heroes')
	if len(hero_files) == 0:
		print("Found no hero config files")
		return

	heroes = []
	os.chdir('Config/Heroes')

	for f in hero_files:
		try:
			heroes.append(Archetype(f))
		except ValueError:
			pass

	print(heroes)


if __name__ == '__main__':
	parse_heroes()
