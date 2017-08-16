# encoding: utf-8


import os
import configparser


class Archetype(object):
	def __init__(self, file_name):
		print("Parsing hero at {0}".format(file_name))
		self._config = configparser.ConfigParser(strict=False)
		with open(file_name, 'rb') as f:
			val = f.read().decode("utf-16le")
			self._config.readfp(val.encode('ascii', 'ignore'))
	
		self._name = 'test' # self._config['RxHeroProvider']['HeroArchetypeName']
	
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
		heroes.append(Archetype(f))
	
	print(heroes)


if __name__ == '__main__':
	parse_heroes()
