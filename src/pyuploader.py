#-*- coding: utf-8 -*-

import os
import sys

import ConfigParser

import gettext

from kernel.optionmgr import OptionManager
from datetime import datetime

from kernel import i18n

import modules.be_acl

################################

import urllib
import urllib2

import xml.etree.ElementTree as etree

################################

class PyUploader():
	def __init__(self):
		self.modules = {}

		self.settings = OptionManager('.'.join((os.path.basename(sys.argv[0]).split('.')[0], 'ini')))

		self.initialize()
		self.run()




	def initialize(self):
		# поддержка интернационализации
		i18n.load('messages')




	def exit(self):
		print _('exit')
		raw_input()
		sys.exit()




	def setupdate(self, data):
		proxydata = {}
		for option in ('user', 'pass', 'host', 'port'):
			proxydata[option] = self.settings.option('PROXY', option, '', True)

		proxydata['port'] = int(self.settings.option('PROXY', 'port', '', True) or 0)

		if proxydata['host']:
			proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxydata})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)

		p = urllib.urlencode({'xml': data})

		try:
			urldata = urllib2.urlopen(self.settings.option('CONNECTION', 'set url', defaultseturl), p).read()

		except urllib2.HTTPError, e:
			# неправильный адрес?
			print 'yes'
			print e
			self.exit()

		except urllib2.URLError, e:
			# нет инета (сетевого подключения)
			print e
			self.exit()

		print urldata

		with (open('data/answer.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata








	def run(self):
		# загрузка языковых ресурсов
		i18n.setup_env()
#		language = self.settings.option('ACCOUNT', 'locale', 'ru_RU')
#		e = i18n.setlanguage(localefile, localepath, language)
#		if e:
#			print e
#			self.exit()

		target = modules.be_acl.SQLDB()

		if target.error:
			print target.error
			self.exit()

		category = 'Components'
		fieldlist = systemfieldlist

		data = target.get(category, fieldlist)

		# [()] -> ({})

		out = []
		for i in data:
#			print i
			v = {field: (i[fieldlist.index(field)]) for field in fieldlist}

			out.append((v))

		data = tuple(out)



		xmldata = etree.TreeBuilder()
		xmldata.start('dataroot', {})

		for item in data:
			xmldata.start(category, {})
			for field in fieldlist:
				if isinstance(item[field], datetime):
					atr = {'type': 'datetime'}
					item[field] = item[field].isoformat(' ')

				elif type(item[field]) == 'int':
					atr = {'type': 'float'}
					item[field] = str(item[field])

				elif item[field] is None:
					atr = {}
					item[field] = ''

				else:
					atr = {'type': 'string'}

#				print item[field]

				xmldata.start(field, atr)
				xmldata.data(item[field])
				xmldata.end(field)

			xmldata.end(category)

		res = xmldata.end('dataroot')

		print etree.tostring(res, encoding="utf-8")

		if not len(res):
			print _('nothing to upload')
			self.exit()

		xmlfilename = 'data\gen.xml'

		try:
			with open(xmlfilename, 'wb') as xmlfile:
				xmlfile.write(etree.tostring(res, encoding="utf-8"))

		except IOError, e:
			print _('no file %s') % (xmlfilename)
			self.exit()

		self.setupdate(etree.tostring(res, encoding="utf-8"))

		print 'Well done!'

#######################

if __name__ == '__main__':
	# plugins directory
	modulespath = 'modules'

	# localization directory
	localepath = './locale'
	localefile = 'messages'

#	configfile = 'pyclient.ini'

	defaultseturl = 'http://noxius.ru/index2.php'

	systemfieldlist = ('M', 'MN', 'PN', 'PC', 'D', 'URL', 'SYM', 'PKG', 'MDL', 'MD', 'CD', 'A',)
	defaultfieldlist = ('Manufacturer', 'Manufacturer_Number', 'Modify_Date')

	PyUploader()