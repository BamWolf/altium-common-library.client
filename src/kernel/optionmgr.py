#-*- coding: utf-8 -*-

import ConfigParser
import codecs

class OptionManager():
	def __init__(self, filename):
		self.cfg = ConfigParser.SafeConfigParser()
		self.cfgfilename = filename

		self.modified = False
		self.error = None



	def initialize(self, section, optionlist):
		if optionlist:
			for option in optionlist:
				self.option(section, option, optionlist[option], True)



	def option(self, section, option, value='', force=False):
		try:
			# Open the file with the correct encoding
			with codecs.open(self.cfgfilename, 'r', encoding='windows-1251') as f:
				self.cfg.readfp(f)

			#self.cfg.read(self.cfgfilename)

		except ConfigParser.ParsingError, e:
			self.error = e
			return

		try:
			value = self.cfg.get(section, option)

		except ConfigParser.NoOptionError:
			if force:
				self.cfg.set(section, option, str(value))
				self.modified = True

		except ConfigParser.NoSectionError:
			if force:
				self.cfg.add_section(section)
				self.cfg.set(section, option, str(value))
				self.modified = True

		if self.modified:
			with open(self.cfgfilename, 'w') as cfgfile:
				self.cfg.write(cfgfile)

		return value


	def options(self, section, force=False):
		self.cfg.read(self.cfgfilename)
		values = []

		try:
			values = self.cfg.items(section)

		except ConfigParser.NoSectionError:
			if force:
				self.cfg.add_section(section)
				self.modified = True

		if self.modified:
			with open(self.cfgfilename, 'w') as cfgfile:
				self.cfg.write(cfgfile)

		return values