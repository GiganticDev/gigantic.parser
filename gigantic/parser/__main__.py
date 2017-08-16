# encoding: utf-8

import os
import configparser
import tempfile


class Resource(object): # Abstraction, no real sections in the ini
	ResourceID = ''						# puAdept4_Cooldown_Upgrade, Adept, etc etc


class UIResource(Resource): # Abstraction, no real sections in the ini
	UIResourceID = ''					# Adept, AdeptGhost, etc


class Skill(Resource): # [ResourceID RxSkillProvider]
	UIResourceID = ''					# Skill1, used as translation index?
	HeroArchetypeName = ''				# Adept, same as HeroArchetypeName in Archetype
	SkillName = ''						# Skill1, Skill2, Skill3, or Skill3 typically


class Upgrade(Resource): # Abstraction, no real sections in the ini
	HeroName = ''						# Adept, same as HeroArchetypeName
	UpgradeTier = ''					# ESUT_Upgrade1, ESUT_Upgrade1_SubUpgrade1, ESUT_Upgrade2, ESUT_Upgrade2_SubUpgrade1, ESUT_None, etc
	MinHeroLevel = 0					# 1 or 5?
	UpgradePathCategory = ''			# UPC_Offense, UPC_Defense, UPC_BurstDamage, UPC_Healing, UPC_Sustain, UPC_Mobility, UPC_AntiDebuffs


class SkillUpgrade(Upgrade): # [ResourceID RxSkillUpgradeProvider]
	SkillUpgradeCategory = ''			# EUC_Skill1Upgrade where Skill1 is the 'SkillName' of the skill
	SkillIndex = 0						# Not sure what it corresponds to, have seen anywhere from 11-34


class PassiveUpgrade(Resource): # [ResourceID RxPassiveUpgradeProvider]
	PassiveUpgradeCategory = '' 		# EUC_UnlockedDuringClash
	PassiveIconIdentifier = ''			# AttackFocus
	PassiveIndex = 0					# 4, 5, 6?


class SummonProvider(UIResource): # [ResourceID RxSummonProvider]
	ProviderPawnClassPath = ''			# "RxGameContent.RxPawn_AdeptAttacker"
	SummonBehaviorTreeName = ''			# "BT_AdeptAttacker"
	CreatorID = ''						# Adept (Maybe HeroArchetypeName?)


class Archetype(UIResource): # [HeroArchetypeName RxHeroProvider]
	HeroArchetypeName = ''				# Adept_Pawn_Arch
	ProviderPawnClassPath = ''			# "RxGameContent.RxPawn_Adept"
	DataSortPriority = 1700				# 1700
	PrimaryTraitPath = ''				# tp_Duelist
	SecondaryTraitPath = ''				# tp_helper
	AttackStat = 0						# 50
	DefenseStat = 0						# 60
	MobilityStat = 0					# 30
	UtilityStat = 0						# 80
	PlayDifficulty = 0					# 5
	PlayStyle = 0						# 14
	BaseUIReticleSpreadMultiplier = 1.0	# 1.0f
	LowHealthTriggerPercent = 40.0		# 40.0f
	LowHealthRecoveredPercent = 43.0	# 43.3f
	LowStaminaTriggerPercent = 25.0		# 25.0f
	LowStaminaRecoveredPercent = 30.0	# 30.0f

	def __repr__(self):
		return self.HeroArchetypeName


def get_hero_config(file_name):
	print("Parsing hero at {0}".format(file_name))
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
	hero = Archetype()

	"""
	Instantiate class object based on section name, names are like [ResourceID RxSkillProvider] where the string after
	space is the object type, and the string before is the ResourceID... but the ResourceID is also specified within
	the section so... whatever?
	"""

	for section in sections:
		data = config[section]
		if 'RxHeroProvider' in section: # Named like [Adept_Pawn_Arch RxHeroProvider]
			resource_id = data['ResourceID']
			hero.HeroArchetypeName = data['HeroArchetypeName']

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

	print(heroes)


if __name__ == '__main__':
	parse_heroes()
