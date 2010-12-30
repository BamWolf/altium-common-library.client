#-*- coding: utf-8 -*-

#import xml.etree.ElementTree as eltree

#######################


class QueryMessage():
	Name = 'XML Query'

	def __init__(self):
		pass


	def type(self):
		pass

	def additem(self, item):
		pass

	def build(self):
		pass



class Component():
	Name = 'CAD Component'

	def __init__(self, manufacturer, part_number):
		self.name = '.'.join((manufacturer, part_number))
		self.m = manufacturer
		self.pn = part_number
		self.category = None
		self.description = None
		self.parameters = []

	def add_parameter(self, parameter):
		if isinstance(parameter, cParameter):
			self.parameters.append(parameter)

		else:
			raise TypeError, "should be cParameter object"

	def build(self):
		pass


class cParameter():
	Name = 'Component Parameter'

	def __init__(self, name, value, mode):
		self.name = name
		self.value = value
		self.type = mode


if __name__ == '__main__':
	i = Component('m', 'pn')

	p = cParameter('Value', 'My', 'string')
	i.add_parameter(p)
	i.add_parameter('')