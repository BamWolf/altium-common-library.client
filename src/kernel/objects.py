#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as eltree

#######################

class QueryMessage():
	Name = 'XML Query'

	def __init__(self, method, mode='request'):

		self.type = mode
		self.method = method
		self.values = {}
		self.data = {}
		self.id = 0



	def add_value(self, name, value):
		self.values[name] = value



	def build(self):
		builder = eltree.TreeBuilder()
		builder.start('query', {'type': self.type})

		# header section
		builder.start('method', {'name': self.method})


		print self.values
		print self.data

		def __t(value):

			if isinstance(value, datetime.datetime):
				atr = 'datetime'

			elif type(value) == 'int':
				atr = 'float'

			elif value is None:
				atr = 'none'

			else:
				atr = 'string'

			return atr

		for value in self.values:
			print value
			builder.start('value', {'name': value, 'type': __t(self.values[value])})
			builder.data(self.values[value])
			builder.end('value')

		builder.end('method')

		# data section
		if self.data:
			builder.start('data', {})

			for element in self.data:
				element = QueryItem(element).build(builder)

			builder.end('data')

		xmldata = builder.end('query')

		result = eltree.tostring(xmldata, encoding="utf-8") 

		with (open('data/generated.xml', 'wb')) as xmlfile:
			xmlfile.write(result)

		return result




class ResponseMessage():
	Name = 'XML Query'

	def __init__(self, xmldata=None):

		self.xmldata = xmldata
		self.error = None
		self.items = []
		self.method = None
		self.values = {}



	def parse(self):
		if not self.xmldata:
			print 'no data'
			self.error = True
			return

		try:
			xmldata = eltree.XML(self.xmldata)

		except eltree.ParseError, e:
			print 'parse error %s' % (e,)
			self.error = True
			return

		print xmldata.tag

		if not xmldata.tag == 'query':
			print 'Warning: WFT?'

		method = xmldata.find('method')

		print method.tag

		for value in method.findall('value'):
			self.values[value.get('type')] = value.text.strip()

		print 'VALUES', self.values



#		elements = xmldata.findall('component')

#		for element in elements:
#			print element

#		data = []

		def _element2dict(element):

			if len(element):
				for child in element:
					_element2dict(child)

		return self

class QueryItem():

	def __init__(self, element):
		self.element = element


	def build(self, builder):

		if isinstance(element, Component):
			print 'it is objects.Component'
		else:
			print 'x3'


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
			result = self._parameters.copy()

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


if __name__ == '__main__':
	i = QueryMessage('identify')
	i.add_value('login', u'Джек')
	i.add_value('password', u'blablabla')



	i.build()


	i = QueryMessage('getall')
	i.add_value('sessionid', u'5dg54sd8th')



	i.build()

