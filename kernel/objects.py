#-*- coding: utf-8 -*-

import datetime

lxml_installed = False

try:
	from lxml import etree
	lxml_installed = True
	print("running with lxml.etree")
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as etree
		print("running with cElementTree on Python 2.5+")
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as etree
			print("running with ElementTree on Python 2.5+")
		except ImportError:
			try:
				# normal cElementTree install
				import cElementTree as etree
				print("running with cElementTree")
			except ImportError:
				try:
					# normal ElementTree install
					import elementtree.ElementTree as etree
					print("running with ElementTree")
				except ImportError:
					print("Failed to import ElementTree from any known place")


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

	def __init__(self, manufacturer='Unknown', partnumber='Unknown'):
		self.manufacturer = manufacturer
		self.number = partnumber

		self._parameters = {}


	def get(self, parameter=None):
		""" возвращает  параметр parameter """
		if parameter:
			result = self._parameters.get(parameter)

		else:
			result = self._parameters.copy()

		return result


	def set(self, parameter):
		""" добавляет новый параметр """
		if not isinstance(parameter, Parameter):
			raise TypeError, "Parameter object expected"

		self._parameters[parameter.name] = parameter



	def parse(self, xml):
		pass

	def build(self):
		el = etree.Element('component')

		el.set('manufacturer', u'ИЖМАШ')
		el.set('partnumber', u'ТСП')

		for parameter in self._parameters:
			el.append(self._parameters[parameter].build())

		return el

class Parameter():

	def __init__(self, name, value):
		self.name = name
		self.value = value

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


	def build(self):
		el = etree.Element('parameter')
		el.set('name', 'Category')
		el.set('value', 'A')
		el.set('type', 'string')

		return el

if __name__ == '__main__':

	q = Component()

	p = Parameter('Value', '50')
	q.set(p)

	try:
		q.set('d')

	except TypeError, e:
		print e


	xmlobject = q.build()

	if lxml_installed:
		xml = etree.tostring(xmlobject, encoding='utf-8', xml_declaration=True, pretty_print=True)

	else:
		from xml.dom import minidom

		barexml = etree.tostring(xmlobject, encoding='utf-8')
		xml = minidom.parseString(barexml).toprettyxml(indent='\t', encoding='utf-8')

	with open('pretty.xml', 'w') as f:
		f.write(xml)
