#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as eltree

#######################


class QueryMessage():
	Name = 'XML Query'

	def __init__(self):

		self.type = ''
		self.items = []


	def type(self):
		pass

	def additem(self, item):
		self.items.append(item)

	def build(self):
		xmldata = eltree.TreeBuilder()
		xmldata.start('data', {})

		for item in self.items:
			xmldata.start('Component', {'man': item.manufacturer, 'num': item.number})


			for parameter in item.parameters:

				"""
				if isinstance(parameter.type, datetime.datetime):
					atr = {'type': 'datetime'}
#					item[field] = item[field].isoformat(' ')

				elif type(item[field]) == 'int':
					atr = {'type': 'float'}
#					item[field] = str(item[field])

				elif item[field] is None:
					atr = {}
#					item[field] = ''

				else:
					atr = {'type': 'string'}
				"""

				xmldata.start(parameter.name, {'type': parameter.type})
				xmldata.data(parameter.value)
				xmldata.end(parameter.name)

			xmldata.end('Component')

		res = xmldata.end('data')

		print eltree.tostring(res, encoding="utf-8")





class Component():
	Name = 'CAD Component'

	def __init__(self, manufacturer, number):
		self.manufacturer = manufacturer or 'Unknown'
		self.number = number or 'Unknown'

		self.id = '.'.join((self.manufacturer, self.number))

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