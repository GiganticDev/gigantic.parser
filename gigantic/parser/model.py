# encoding: utf-8

from marrow.schema import Attribute, Attributes, Container


"""
Definition of the class attributes like this as empty strings or default values is _completely_ pointless and very
stupid considering the base resource class inherits from dict. I'm just doing it for documentation reasons, to sort of
1:1 map the data we expect with whats in the ini files. This will be cleaned up once I polish this utility.
"""

class Resource(Container):  # Abstraction, no real sections in the ini
	id = Attribute('resourceid')  # puAdept4_Cooldown_Upgrade, Adept, etc etc

	def __repr__(self):
		return self.id


class UIResource(Resource):  # Abstraction, no real sections in the ini
	ui_id = Attribute('uiresource')  # Adept, AdeptGhost, etc


class Upgrade(Resource):  # Abstraction, no real sections in the ini
	hero = Attribute('heroname')  # Adept, same as HeroArchetypeName
	tier = Attribute('upgradetier')  # ESUT_Upgrade1, ESUT_Upgrade1_SubUpgrade1, ESUT_Upgrade2, ESUT_Upgrade2_SubUpgrade1, ESUT_None, etc
	min_level = Attribute('minherolevel')  # 1 or 5?
	path_category = Attribute('upgradepathcategory')  # UPC_Offense, UPC_Defense, UPC_BurstDamage, UPC_Healing, UPC_Sustain, UPC_Mobility, UPC_AntiDebuffs


class Skill(UIResource):  # [ResourceID RxSkillProvider]
	__section__ = 'RxSkillProvider'

	archetype = Attribute('heroarchetypename')  # Adept, same as HeroArchetypeName in Archetype
	name = Attribute('skillname')  # Skill1, Skill2, Skill3, or Skill3 typically


class SkillUpgrade(Upgrade):  # [ResourceID RxSkillUpgradeProvider]
	__section__ = 'RxSkillUpgradeProvider'

	skill_category = Attribute('skillupgradecategory')  # EUC_Skill1Upgrade where Skill1 is the 'SkillName' of the skill
	index = Attribute('skillindex')  # Not sure what it corresponds to, have seen anywhere from 11-34


class PassiveUpgrade(Resource):  # [ResourceID RxPassiveUpgradeProvider]
	__section__ = 'RxPassiveUpgradeProvider'

	passive_category = Attribute('passiveupgradecategory')  # EUC_UnlockedDuringClash
	passive_icon_id = Attribute('passiveiconidentifier')  # AttackFocus
	passive_id = Attribute('passiveindex')  # 4, 5, 6?


class UpgradePath(Resource): # [ResourceID RxUpgradePathProvider]
	__section__ = 'RxUpgradePathProvider'

	set_name = Attribute('setname')  # up_Adept_Default
	upgrade_type = Attribute('upgradetype')  # UPT_Skill1_U1
	group_index = Attribute('groupindex')  # 0 - 15 in increments of 1?

	def __repr__(self):
		return str(self.set_name)


class SummonProvider(UIResource):  # [ResourceID RxSummonProvider]
	__section__ = 'RxSummonProvider'

	pawn_class_path = Attribute('providerpawnclasspath')  # "RxGameContent.RxPawn_AdeptAttacker"
	behavior_tree_name = Attribute('summonbehaviortreename')  # "BT_AdeptAttacker"
	creator_id = Attribute('creatorid')  # Adept (Maybe HeroArchetypeName?)


class Archetype(UIResource):  # [HeroArchetypeName RxHeroProvider]
	__section__ = 'RxHeroProvider'

	name = Attribute('heroarchetypename')  # Adept_Pawn_Arch
	pawn_class_path = Attribute('providerpawnclasspath')  # "RxGameContent.RxPawn_Adept"
	sort_priority = Attribute('datasortpriority')  # 1700
	primary_trait_path = Attribute('primarytraitpath')  # tp_Duelist
	secondary_trait_path = Attribute('secondarytraitpath')  # tp_helper
	attack = Attribute('attackstat')  # 50
	defenese = Attribute('defensestat')  # 60
	mobility = Attribute('mobilitystat')  # 30
	utility = Attribute('utilitystat')  # 80
	difficulty = Attribute('playdifficulty')  # 5
	style = Attribute('playstyle')  # 14
	reticle_spread = Attribute('baseuireticlespreadmultiplier')  # 1.0f
	health_min_trigger = Attribute('lowhealthtriggerpercent')  # 40.0f
	health_recover_trigger = Attribute('lowhealthrecoveredpercent')  # 43.3f
	stamina_min_trigger = Attribute('lowstaminatriggerpercent')  # 25.0f
	stamina_recover_trigger = Attribute('lowstaminarecoveredpercent')  # 30.0f

	def __repr__(self):
		return self.name
