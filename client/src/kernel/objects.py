#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as xmltree

lxml_installed = False

try:
	from lxml import etree as xmltree
	lxml_installed = True
	print("running with lxml.etree")
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as xmltree
		print("running with cElementTree on Python 2.5+")
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as xmltree
			print("running with ElementTree on Python 2.5+")
		except ImportError:
			try:
				# normal cElementTree install
				import cElementTree as xmltree
				print("running with cElementTree")
			except ImportError:
				try:
					# normal ElementTree install
					import elementtree.ElementTree as xmltree
					print("running with ElementTree")
				except ImportError:
					print("Failed to import ElementTree from any known place")

print


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

		return



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

#		print xmldata.tag
#		print xmldata.get('type')

		self.type = xmldata.get('type')

		if not xmldata.tag == 'query':
			print 'Warning: WFT?'

		method = xmldata.find('method')

		### только текстовые !!
		for value in method.findall('value'):
			self.values[value.get('name')] = value.get('value')

#		print 'VALUES', self.values

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

#				print '\t', name, value, mode

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

	def build(self, builder):
		return


class Component():

	def __init__(self, manufacturer='Unknown', partnumber='Unknown'):
		self._manufacturer = manufacturer
		self._partnumber = partnumber
		self._parameters = {}

	def manufacturer(self):
		""" возвращает производителя компонента """
		return self._manufacturer

	def partnumber(self):
		""" возвращает артикул компонента """
		return self._partnumber

	def id(self):
		""" возвращает id компонента """
		return '.'.join((self._manufacturer, self._partnumber))

	def __iter__(self):
		return iter(self._parameters.values())

	def get(self, parameter, real=False):
		""" возвращает значение параметра с наименованием parameter (имя уже известно) """

		if parameter.lower() == 'manufacturer':
			return self._manufacturer

		elif parameter.lower() == 'partnumber':
			return self._partnumber

		elif self._parameters.get(parameter):
			if real:
				return self._parameters.get(parameter).real()

			else:
				return self._parameters.get(parameter).value()

		else:
			if real:
				return None

			else:
				return u''

	def set(self, parameter):
		""" добавляет новый параметр """
		if not isinstance(parameter, Parameter):
			raise TypeError, "Parameter object expected"

		self._parameters[parameter.name()] = parameter

	def build(self):
		""" возвращает Element компонента """
		el = xmltree.Element('component')

		el.set('manufacturer', self.manufacturer())
		el.set('partnumber', self.partnumber())

		for parameter in sorted(self._parameters.keys()):
			el.append(self._parameters[parameter].build())

		return el

	def xml(self):
		""" возвращает pretty_printed XML компонента """
		xmlobject = self.build()

		if lxml_installed:
			xml = xmltree.tostring(xmlobject, encoding='utf-8', xml_declaration=True, pretty_print=True)

		else:
			from xml.dom import minidom

			barexml = xmltree.tostring(xmlobject, encoding='utf-8')
			xml = minidom.parseString(barexml).toprettyxml(indent='\t', encoding='utf-8')

		return xml

	def parse(self, xml):
		""" генерирует компонент из XML """
		try:
			el = xmltree.XML(xml)

		except:
			print 'Non-valid XML: error parsing document'
			return

		if not el.tag == 'component':
			raise Exception, 'Non-valid XML: it is not a component'

		self._manufacturer = el.get('manufacturer')
		self._partnumber = el.get('partnumber')

		for sub in el.findall('parameter'):
			try:
				parameter = Parameter(sub.get('name'), sub.get('value'), sub.get('type'))
				self.set(parameter)
			except:
				print 'Non-valid XML: it is not parameter'



class Symbol():

	def __init__(self, name='Unknown'):
		self._name = name
		self._parameters = {}

	def id(self):
		""" возвращает id символа """
		return self._name

	def __iter__(self):
		return iter(self._parameters.values())

	def get(self, parameter, real=False):
		""" возвращает значение параметра с наименованием parameter (имя уже известно) """
		exist = self._parameters.get(parameter)

		if not exist:
			return u''

		if real:
			return self._parameters.get(parameter).real()

		else:
			return self._parameters.get(parameter).value()

	def set(self, parameter):
		""" добавляет новый параметр """
		if not isinstance(parameter, Parameter):
			raise TypeError, "Parameter object expected"

		self._parameters[parameter.name()] = parameter

	def build(self):
		""" возвращает Element символа """
		el = xmltree.Element('symbol')

		el.set('name', self.id())

		for parameter in sorted(self._parameters.keys()):
			el.append(self._parameters[parameter].build())

		return el

	def xml(self):
		""" возвращает pretty_printed XML символа """
		xmlobject = self.build()

		if lxml_installed:
			xml = xmltree.tostring(xmlobject, encoding='utf-8', xml_declaration=True, pretty_print=True)

		else:
			from xml.dom import minidom

			barexml = xmltree.tostring(xmlobject, encoding='utf-8')
			xml = minidom.parseString(barexml).toprettyxml(indent='\t', encoding='utf-8')

		return xml

	def parse(self, xml):
		""" генерирует символ из XML """
		try:
			el = xmltree.XML(xml)

		except:
			print 'Non-valid XML: error parsing document'
			return

		if not el.tag == 'symbol':
			raise Exception, 'Non-valid XML: it is not a symbol'

		self._name = el.get('name')

		for sub in el.findall('parameter'):
			try:
				parameter = Parameter(sub.get('name'), sub.get('value'), sub.get('type'))
				self.set(parameter)
			except:
				print 'Non-valid XML: it is not parameter'


class Package():

	def __init__(self, name='Unknown'):
		self._name = name
		self._parameters = {}

	def id(self):
		""" возвращает id корпуса """
		return self._name

	def __iter__(self):
		return iter(self._parameters.values())

	def get(self, parameter, real=False):
		""" возвращает значение параметра с наименованием parameter (имя уже известно) """
		exist = self._parameters.get(parameter)

		if not exist:
			return u''

		if real:
			return self._parameters.get(parameter).real()

		else:
			return self._parameters.get(parameter).value()

	def set(self, parameter):
		""" добавляет новый параметр """
		if not isinstance(parameter, Parameter):
			raise TypeError, "Parameter object expected"

		self._parameters[parameter.name()] = parameter

	def build(self):
		""" возвращает Element корпуса """
		el = xmltree.Element('package')

		el.set('name', self.id())

		for parameter in sorted(self._parameters.keys()):
			el.append(self._parameters[parameter].build())

		return el

	def xml(self):
		""" возвращает pretty_printed XML символа """
		xmlobject = self.build()

		if lxml_installed:
			xml = xmltree.tostring(xmlobject, encoding='utf-8', xml_declaration=True, pretty_print=True)

		else:
			from xml.dom import minidom

			barexml = xmltree.tostring(xmlobject, encoding='utf-8')
			xml = minidom.parseString(barexml).toprettyxml(indent='\t', encoding='utf-8')

		return xml

	def parse(self, xml):
		""" генерирует корпус из XML """
		try:
			el = xmltree.XML(xml)

		except:
			print 'Non-valid XML: error parsing document'
			return

		if not el.tag == 'package':
			raise Exception, 'Non-valid XML: it is not a package'

		self._name = el.get('name')

		for sub in el.findall('parameter'):
			try:
				parameter = Parameter(sub.get('name'), sub.get('value'), sub.get('type'))
				self.set(parameter)
			except:
				print 'Non-valid XML: it is not parameter'


class Model():

	def __init__(self, name='Unknown'):
		self._name = name
		self._parameters = {}

	def id(self):
		""" возвращает id модели """
		return self._name

	def __iter__(self):
		return iter(self._parameters.values())

	def get(self, parameter, real=False):
		""" возвращает значение параметра с наименованием parameter (имя уже известно) """
		exist = self._parameters.get(parameter)

		if not exist:
			return u''

		if real:
			return self._parameters.get(parameter).real()

		else:
			return self._parameters.get(parameter).value()

	def set(self, parameter):
		""" добавляет новый параметр """
		if not isinstance(parameter, Parameter):
			raise TypeError, "Parameter object expected"

		self._parameters[parameter.name()] = parameter

	def build(self):
		""" возвращает Element модели """
		el = xmltree.Element('model')

		el.set('name', self.id())

		for parameter in sorted(self._parameters.keys()):
			el.append(self._parameters[parameter].build())

		return el

	def xml(self):
		""" возвращает pretty_printed XML символа """
		xmlobject = self.build()

		if lxml_installed:
			xml = xmltree.tostring(xmlobject, encoding='utf-8', xml_declaration=True, pretty_print=True)

		else:
			from xml.dom import minidom

			barexml = xmltree.tostring(xmlobject, encoding='utf-8')
			xml = minidom.parseString(barexml).toprettyxml(indent='\t', encoding='utf-8')

		return xml

	def parse(self, xml):
		""" генерирует модель из XML """
		try:
			el = xmltree.XML(xml)

		except:
			print 'Non-valid XML: error parsing document'
			return

		if not el.tag == 'model':
			raise Exception, 'Non-valid XML: it is not a model'

		self._name = el.get('name')

		for sub in el.findall('parameter'):
			try:
				parameter = Parameter(sub.get('name'), sub.get('value'), sub.get('type'))
				self.set(parameter)
			except:
				print 'Non-valid XML: it is not parameter'


class Parameter():

	def __init__(self, name, value, mode='string'):
		if not name:
			raise Exception, 'Empty Parameter Name'

		self._name = name
		self._value = value
		self._type = mode

		### добавить валидацию входных значений

	def name(self):
		""" возвращает наименование параметра """
		return self._name

	def value(self):
		""" возвращает строковое значение параметра """
		return self._value

	def type(self):
		"""возвращает тип параметра """
		return self._type

	def real(self):
		""" возвращает приведенное значение параметра """
		if self._type == 'string':
			return unicode(self._value)

		elif self._type == 'float':
			return float(self._value)

		elif self._type == 'datetime':
			return datetime.datetime.strptime(self._value, '%Y-%m-%d %H:%M:%S.%f')

	def build(self):
		""" возвращает Element параметра """
		el = xmltree.Element('parameter')
		el.set('name', self.name())
		el.set('value', self.value())
		el.set('type', self.type())

		return el
