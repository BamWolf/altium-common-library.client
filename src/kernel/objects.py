#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as eltree

#######################


class QueryMessage():
	Name = 'XML Query'

	def __init__(self):

		self.type = 'add'
		self.target = 'components'
		self.items = []


	def type(self):
		pass

	def add(self, item):
		self.items.append(item)


	def build(self):
		builder = eltree.TreeBuilder()
		builder.start('query', {})

		# header section
		builder.start('action', {'type': self.type, 'source': self.target})
		builder.end('action')

		# data section
		builder.start('data', {})

		for item in self.items:
			builder.start('Component', {'man': item.manufacturer, 'num': item.number})


			for parameter, value in item.get():

				builder.start(parameter, {'type': 'string'})
				builder.data(value)
				builder.end(parameter)

			builder.end('Component')

		builder.end('data')

		xmldata = builder.end('query')

		result = eltree.tostring(xmldata, encoding="utf-8") 

		with (open('data/gen.xml', 'wb')) as xmlfile:
			xmlfile.write(result)

		return result




class Component():
	Name = 'Component'

	def __init__(self, manufacturer, number):
		self.manufacturer = manufacturer or 'Unknown'
		self.number = number or 'Unknown'

		self._parameters = {}



	def id(self):
		return '.'.join((self.manufacturer, self.number))


	def set(self, parameter, value, mode='string'):
		""" добавляет новый параметр """
#		if not isinstance(parameter, Parameter):
#			raise TypeError, "Parameter object expected"

#		if paramter.name:
		if parameter:
			self._parameters[parameter] = value


	def get(self, parameter=None):
		""" возвращает  параметр parameter """
		if parameter:
			result = self._parameters.get(parameter)

		else:
			result = self._parameters.items()

		return result




class Parameter():
	Name = 'Parameter'

	def __init__(self, name, value, mode='string'):
		self.name = name
		self.value = value
		self.type = mode

		def __t(self):

			if isinstance(parameter.type, datetime.datetime):
				atr = {'type': 'datetime'}
#				item[field] = item[field].isoformat(' ')

			elif type(item[field]) == 'int':
				atr = {'type': 'float'}
#				item[field] = str(item[field])

			elif item[field] is None:
				atr = {}
#				item[field] = ''

			else:
				atr = {'type': 'string'}
