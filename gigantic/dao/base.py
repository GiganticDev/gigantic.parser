# encoding: utf-8

from marrow.schema import Attribute, Attributes, Container
from collections import MutableMapping


class DAO(Container):
	__map__ = {}  # this is global to the entire base class
	__fields__ = Attributes(Attribute)
	
	@classmethod
	def __attributed__(cls):
		"""Called after a new subclass is constructed."""
		
		if hasattr(cls, '__section__') and cls.__section__:
			cls.__map__[cls.__section__] = cls
		
		cls.__relations__ = set()  # this is specific to a subclass
		cls.__dataset__ = {}  # this is also specific to a subclass
	
	def __init__(self, data=None, *args, **kw):
		super().__init__(*args, **kw)
		
		if data is not None:
			self.__data__ = data
		
		if self.id in self.__dataset__:
			raise ValueError("Duplicate " + self.__class__.__name__ + " ID: " + self.id)
		
		self.__dataset__[self.id] = self  # Record ourselves.
	
	@classmethod
	def __relates_to__(cls, foreign):
		cls.__relations__.add(foreign)
	
	def __repr__(self):
		parts = []
		for name, field in self.__fields__.items():
			value = getattr(self, name, None)
			if value:
				parts.append(name + "=" + repr(value))
				
		return "{0}({1})".format(self.__class__.__name__, ", ".join(parts))
		
		# Mapping Protocol
	
	def __getitem__(self, name):
		"""Retrieve data from the backing store."""
		
		attr = self.__fields__[name]
		return self.__data__[attr.__name__]
	
	def __setitem__(self, name, value):
		"""Assign data directly to the backing store."""
		
		attr = self.__fields__[name]
		self.__data__[attr.__name__] = value
	
	def __delitem__(self, name):
		"""Unset a value from the backing store."""
		
		attr = self.__fields__[name]
		del self.__data__[attr.__name__]
	
	def __iter__(self):
		"""Iterate the names of the python attributes."""
		
		return iter(self.__fields__.keys())
	
	def __len__(self):
		"""Retrieve the size of the backing store."""
		
		return len(getattr(self, '__data__', {}))
	
	def keys(self):
		"""Iterate the keys assigned to the python attributes."""
		
		return self.__fields__.keys()
	
	def items(self):
		"""Iterate 2-tuple pairs of (key, value) from the backing store."""
		
		# I can't decide how best to wrap this... =/
		return {
			name: self.__data__[field.__name__]
			for name, field in self.__attributes__.items() if field.__name__ in self.__data__
		}.items()
	
	iteritems = items  # Python 2 interation, as per items.
	
	def values(self):
		"""Iterate the values within the backing store."""
		
		return self.__data__.values()
	
	def __contains__(self, key):
		"""Determine if the given key is present in the backing store."""
		
		return key in self.__fields__
	
	def __eq__(self, other):
		"""Equality comparison between the backing store and other value."""
		
		return self.__data__ == other  # Can't decide whether or not to change this...
	
	def __ne__(self, other):
		"""Inverse equality comparison between the backing store and other value."""
		
		return self.__data__ != other  # Can't decide whether or not to change this...
	
	def get(self, key, default=None):
		"""Retrieve a value from the backing store with a default value."""
		
		attr = self.__fields__[key]
		return self.__data__.get(attr.__name__, default)
	
	def clear(self):
		"""Empty the backing store of data."""
		
		self.__data__.clear()
	
	def pop(self, name, default=None):
		"""Retrieve and remove a value from the backing store, optionally with a default."""
		
		attr = self.__fields__[name]
		if default is None:
			return self.__data__.pop(attr.__name__)
		
		return self.__data__.pop(attr.__name__, default)
	
	def popitem(self):
		"""Pop an item 2-tuple off the backing store."""
		
		return self.__data__.popitem()  # TODO:
	
	def update(self, *args, **kw):
		"""Update the backing store directly."""
		
		self.__data__.update(*args, **kw)  # TODO
	
	def setdefault(self, key, value=None):
		"""Set a value in the backing store if no value is currently present."""
		
		return self.__data__.setdefault(key, value)  # TODO


MutableMapping.register(DAO)  # Metaclass conflict if we subclass.
