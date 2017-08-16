# encoding: utf-8

import os
import configparser
import tempfile
import json


class Resource(dict): # Abstraction, no real sections in the ini
	resourceid = None					# puAdept4_Cooldown_Upgrade, Adept, etc etc

	def __repr__(self):
		return self.resourceid


class UIResource(Resource): # Abstraction, no real sections in the ini
	uiresourceid = ''					# Adept, AdeptGhost, etc


class Skill(UIResource): # [ResourceID RxSkillProvider]
	heroarchetypename = ''				# Adept, same as HeroArchetypeName in Archetype
	skillname = ''						# Skill1, Skill2, Skill3, or Skill3 typically


class Upgrade(Resource): # Abstraction, no real sections in the ini
	heroname = ''						# Adept, same as HeroArchetypeName
	upgradetier = ''					# ESUT_Upgrade1, ESUT_Upgrade1_SubUpgrade1, ESUT_Upgrade2, ESUT_Upgrade2_SubUpgrade1, ESUT_None, etc
	minherolevel = 0					# 1 or 5?
	upgradepathcategory = ''			# UPC_Offense, UPC_Defense, UPC_BurstDamage, UPC_Healing, UPC_Sustain, UPC_Mobility, UPC_AntiDebuffs


class SkillUpgrade(Upgrade): # [ResourceID RxSkillUpgradeProvider]
	skillupgradecategory = ''			# EUC_Skill1Upgrade where Skill1 is the 'SkillName' of the skill
	skillindex = 0						# Not sure what it corresponds to, have seen anywhere from 11-34


class PassiveUpgrade(Resource): # [ResourceID RxPassiveUpgradeProvider]
	passiveupgradecategory = '' 		# EUC_UnlockedDuringClash
	passiveiconidentifier = ''			# AttackFocus
	passiveindex = 0					# 4, 5, 6?


class UpgradePath(Resource): # [ResourceID RxUpgradePathProvider]
	setname = ''						# up_Adept_Default
	upgradetype = ''					# UPT_Skill1_U1
	groupindex = 0						# 0 - 15 in increments of 1?

	def __repr__(self):
		return str(self.setname)


class SummonProvider(UIResource): # [ResourceID RxSummonProvider]
	providerpawnclasspath = ''			# "RxGameContent.RxPawn_AdeptAttacker"
	summonbehaviortreename = ''			# "BT_AdeptAttacker"
	creatorid = ''						# Adept (Maybe HeroArchetypeName?)


class Archetype(UIResource): # [HeroArchetypeName RxHeroProvider]
	heroarchetypename = ''				# Adept_Pawn_Arch
	providerpawnclasspath = ''			# "RxGameContent.RxPawn_Adept"
	datasortpriority = 1700				# 1700
	primarytraitpath = ''				# tp_Duelist
	secondarytraitpath = ''				# tp_helper
	attackstat = 0						# 50
	defensestat = 0						# 60
	mobilitystat = 0					# 30
	utilitystat = 0						# 80
	playdifficulty = 0					# 5
	playstyle = 0						# 14
	baseuireticlespreadmultiplier = 1.0	# 1.0f
	lowhealthtriggerpercent = 40.0		# 40.0f
	lowhealthrecoveredpercent = 43.0	# 43.3f
	lowstaminatriggerpercent = 25.0		# 25.0f
	lowstaminarecoveredpercent = 30.0	# 30.0f

	def __repr__(self):
		return self.heroarchetypename


class_section_map = {
		'RxHeroProvider': Archetype,
		# 'RxSummonProvider': SummonProvider,
		'RxSkillProvider': Skill,
		'RxSkillUpgradeProvider': SkillUpgrade,
		# 'RxPassiveUpgradeProvider': PassiveUpgrade,
		# 'RxUpgradePathProvider': UpgradePath,
	}

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
