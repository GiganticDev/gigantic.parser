# encoding: utf-8

from marrow.schema import Attribute


class Relationship(Attribute):
	resource = Attribute()
	
	def __fixup__(self, cls):
		self.resource.__relates_to__(cls)  # cls == the class a Relationship instance is being assigned to
	
	def __get__(self, obj, cls=None):
		id = super(Relationship, self).__get__(obj, cls)
		return id
		# if id is None or id == 'None': return id # There are some RxSkillUpgradeProvider's with HeroName = None
		# try:
		# 	return self.resource.__dataset__[id]
		# except KeyError:
		# 	raise ValueError("No {0} found with id {1}".format(self.resource.__name__, id))
