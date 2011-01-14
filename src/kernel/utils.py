#-*- coding: utf-8 -*-

from configobj import ConfigObj

class OptionManager():
	def __init__(self, filename, encoding='cp1251'):
		self.modified = False
		self.error = None

		try:
			self.parser = ConfigObj(filename, encoding=encoding)

		except ConfigObjError, e:
			self.error = e



	def initialize(self, section, optionlist):
		pass
#		if optionlist:
#			for option in optionlist:
#				self.option(section, option, optionlist[option], True)



	def save(self):
		try:
			self.parser.write()

		except IOError, e:
			print e
			self.error = e


	def load(self):
		pass
#		try:
			# Open the file with the correct encoding
#			with codecs.open(self.filename, 'r', encoding='windows-1251') as f:
#			with open(self.filename, 'r', encoding='windows-1251') as f:
#				self.parser.readfp(f)

#		except IOError, e:
#			print e
#			self.error = e

#		except ConfigParser.ParsingError, e:
#			self.error = e



	def option(self, section, option, default=u'', debug=False):
#		print 'DEBUG:', section, option

		section = section.upper()
		option = option.lower()
			
		if not debug:
			if not section in self.parser:
				self.parser[section] = {}

			value = self.parser[section].setdefault(option, default)

			self.modified = True
#			self.save()

		else:
			if not section in self.parser:
				value = default

			else:
				value = self.parser[section].get(option, default)

		return value



	def options(self, section, force=False):
		self.parser.read(self.filename)
		values = []

		try:
			values = self.parser.items(section)

		except ConfigParser.NoSectionError:
			if force:
				self.parser.add_section(section)
				self.modified = True

		return values


if __name__ == '__main__':

	pass
