#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as eltree

#######################

class RequestMessage():
	Name = 'XML Query'

	def __init__(self, method, mode='request'):

		self.type = mode
		self.method = method
		self.values = {}
		self.data = []
		self.id = 0



	def add_value(self, name, value):
		self.values[name] = value


	def add_item(self, item):
		self.data.append(item)


	def build(self):
		builder = eltree.TreeBuilder()
		builder.start('query', {'type': self.type})

		# header section
		builder.start('method', {'name': self.method})

		for value in self.values:
			print value
			builder.start('value', {'name': value, 'value': str(self.values[value]), 'type':self. __t(self.values[value])})
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

		return result


	def __t(self, value):

		if isinstance(value, datetime.datetime):
			atr = 'datetime'

		elif type(value) == 'int':
			atr = 'float'

		elif value is None:
			atr = 'none'

		else:
			atr = 'string'

		return atr



class ResponseMessage():
	Name = 'XML Query'

	def __init__(self, xmldata=None):

		self.type = None
		self.xmldata = xmldata
		self.error = None
		self.data = []
		self.method = None
		self.values = {}
		self.id = 0



	def parse(self):
		if not self.xmldata:
			print 'no data'
			self.error = 'no data to parse'
			return

		try:
			xmldata = eltree.XML(self.xmldata)


		except eltree.ParseError, e:
			print 'parse error %s' % (e,)
			self.error = e
			return

		print xmldata.tag
		print xmldata.get('type')

		self.type = xmldata.get('type')

		if not xmldata.tag == 'query':
			print 'Warning: WFT?'

		method = xmldata.find('method')

		### только текстовые !!
		for value in method.findall('value'):
			self.values[value.get('name')] = value.get('value')

		print 'VALUES', self.values

		data = xmldata.find('data')

		elements = data.findall('component')

		for element in elements:
			
			manufacturer = element.get('manufacturer')
			partnumber = element.get('partnumber')

			if not isinstance(manufacturer, unicode):
				manufacturer = unicode(manufacturer, 'utf-8')

			if not isinstance(partnumber, unicode):
				partnumber = unicode(partnumber, 'utf-8')

			el = Component(manufacturer, partnumber)

			for parameter in element.findall('parameter'):
				name = parameter.get('name')
				value = parameter.get('value')
				mode = parameter.get('type')

				print '\t', name, value, mode

				el.set(name, value, mode)

			self.data.append(el)



		def _element2dict(element):

			if len(element):
				for child in element:
					_element2dict(child)

		return self

class QueryItem():

	def __init__(self, element):
		self.element = element

	def __t(self, value):

		if isinstance(value, unicode):
			return value, 'string'

		elif isinstance(value, int):
			return str(value), 'float'

		elif isinstance(value, datetime.datetime):
			return value.isoformat(' '), 'datetime'

		elif value is None:
			return '', ''

		else:
			print 'FUCKK!!!'
			return '', ''



	def build(self, builder):

		if isinstance(self.element, Component):
			builder.start('component', {'manufacturer': self.element.manufacturer, 'partnumber': self.element.number})

			parameters = self.element.get()

			for parameter in parameters:
#				print parameters[parameter]
				value, mode = self.__t(parameters[parameter])

				builder.start('parameter', {'name': parameter, 'value': value, 'type': mode})
				builder.end('parameter')

			builder.end('component')

		else:
			print 'x3'


class Component():
	Name = 'Component'

	def __init__(self, manufacturer, partnumber):
		self.manufacturer = manufacturer or 'Unknown'
		self.number = partnumber or 'Unknown'

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
