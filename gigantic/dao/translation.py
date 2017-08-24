# encoding: utf-8

from marrow.schema import Attribute, Container

from .base import DAO

LANGUAGES = {'INT', 'FRA', 'DEU'}


class Translation(DAO):
	__map__ = {}  # this is global to the entire base class
	
	@classmethod
	def __attributed__(cls):
		if hasattr(cls, '__section__') and cls.__section__:
			cls.__map__[cls.__section__] = cls
		
		cls.__dataset__ = {language: {} for language in LANGUAGES}
	
	def __init__(self, language, section_id, data=None, *args, **kw):
		super(Translation, self).__init__(*args, **kw)
		
		if data is not None:
			self.__data__ = data
		
		self.section_id = section_id
		
		if self.section_id in self.__dataset__[language]:
			raise ValueError("Duplicate " + self.__class__.__name__ + " ID: " + self.section_id)
		
		self.__dataset__[language][self.section_id] = self  # Record ourselves.
		

class HeroTranslation(Translation):
	__section__ = 'RxHeroProvider'
	
	display_name = Attribute('herodisplayname')
	description = Attribute('herodescription')
	flavor_text = Attribute('heroflavortext')
	

class SkillTranslation(Translation):
	__section__ = 'RxSkillProvider'
	
	display_name = Attribute('skilldisplayname')
	description = Attribute('skilldescription')


class SkillUpgradeTranslation(Translation):
	__section__ = 'RxSkillUpgradeProvider'
	
	display_name = Attribute('skillupgradedisplayname')
	description = Attribute('skillupgradedescription')
