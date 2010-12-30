#-*- coding: utf-8 -*-

import os
import sys
import inspect

import ConfigParser

import gettext

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from kernel.plugin import plugin as pyplugin
from kernel.optionmgr import OptionManager

from kernel import i18n

################################

import urllib
import urllib2

from datetime import datetime

import xml.etree.ElementTree as etree

################################

class PyClient():
	def __init__(self, *argv):
		self.modules = {}

		self.settings = OptionManager('.'.join((os.path.basename(sys.argv[0]).split('.')[0], 'ini')))
		self.initialize()
		self.run()

		self.ui = QtGui.QApplication(sys.argv)
		self.widget = MainWindow(self)
		self.widget.show()
		self.ui.exec_()



	def initialize(self):
		# поддержка интернационализации
		i18n.load('messages')



	def exit(self):
		print _('exit')
		raw_input()
		sys.exit()



	def loadmodules(self):
		for filename in os.listdir(modulespath):
			if filename.endswith ('.py') and filename is not '__init__.py':
				modulename = filename[: -3]
				package = __import__('.'.join((modulespath, modulename)))
				module = getattr(package, modulename)

				for element in dir(module):
					obj = getattr(module, element)
	
					if inspect.isclass(obj):
						if issubclass(obj, pyplugin):
							plugininstance = obj()
							self.modules[plugininstance.name] = obj
							if plugininstance.modified:
								self.modified = True

 
	def getupdate(self, self2, username, password, category):
		proxydata = {}
		for option in ('user', 'pass', 'host', 'port'):
			proxydata[option] = self.settings.option('PROXY', option, '', True)

		proxydata['port'] = int(self.settings.option('PROXY', 'port', '', True) or '0')

#		print proxydata

		if proxydata['host']:
			print _('proxy %(host)s %(port)s') % proxydata
			proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxydata})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)

		authentificatedata = urllib.urlencode({'login': 'user', 'password': 'user'})
#		session = urllib2.urlopen(self.settings.option('CONNECTION', 'get url', defaultgeturl, True), authentificatedata)
#		print session.read()

		variable = urllib.urlencode({'ip': category})

#		print variable

		try:
			urldata = urllib2.urlopen(self.settings.option('CONNECTION', 'get url', defaultgeturl, True), variable).read()

		except urllib2.HTTPError, e:
			# неправильный адрес?
			print 'yes'
			print e
			self.exit()

		except urllib2.URLError, e:
			# нет инета (сетевого подключения)
			print e
			self.exit()

#		print urldata

		with (open('data\get.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata


	def parseupdate(self, data):
		if not data:
			print _('no data')
			self.exit()

		try:
			xmldata = etree.XML(data)

		except etree.ParseError, e:
			print _('parse error %s') % (e,)
			self.exit()

		print xmldata.tag

		if not xmldata.tag == 'message':
			print 'WFT?'

		head = xmldata.find('Header')

		elements = xmldata.findall('component')

		for element in elements:
			print element

		data = []

		# к удалению #################
		fields = sysstrfields + sysdtfields

		def _element2dict(element):
		


			if len(element):
				for child in element:
					_element2dict(child)


		for element in elements:
			component = {}

			for i in xrange(0, len(fields)):
				el = element.find(fields[i])

				if el is None:
					print 'NO ELEMENT'
					return

				eltype = el.get('type')

				if eltype == 'string':
					elvalue = (lambda s: s and s.strip())(el.text)

				elif eltype == 'datetime':
					elvalue = datetime.strptime(el.text, "%Y-%m-%d %H:%M:%S")

				else:
					print 'TYPE ERROR'
					return

				component[fields[i]] = elvalue

			data.append(component)

		return data




	def sortupdate(self, category, data):
		if not data:
			print _('nothing to sort')
			self.exit()

		print _('processing')
		cfg = OptionManager('data.ini')

		if cfg.error:
			print cfg.error
			self.exit()


		table = cfg.option('TABLES', category, '', True)

		if not table:
			print _('no table %s') % (category,)
			self.exit()

		####### оптимизировать ########
		tablefields = tuple(cfg.options(table + '_Fields', True))
		fieldlist = tuple([item[0] for item in tablefields])

		if not tablefields:
			print _('no fields in %s') % (table,)
			self.exit()

		content = []




		def stringize(s):

#			print s
			if isinstance(s, datetime):
				return s.isoformat(' ')

			elif isinstance(s, bool) or isinstance(s, int) or isinstance(s, float):
				return str(s)

			elif s is None:
				return ''

			else:
				return s



		for component in data:
			dataout = []


			### причесать, очень коряво ###
			for field in tablefields:
				value = unicode(field[1], 'utf-8')

				if value in [''.join(( '[', s, ']' )) for s in sysdtfields]:
					value = component[value[1:-1]] or None

				else:
					for item in sysstrfields:
						value = value.replace(''.join(('[', item, ']')), stringize(component[item]) or '')

				dataout.append(value)

			content.append(tuple(dataout))

		return fieldlist, content



	def run(self):
		# загрузка языковых ресурсов
		i18n.setup_env()
#		language = self.settings.option('ACCOUNT', 'locale', 'ru_RU')
#		e = i18n.setlanguage(localefile, localepath, language)

#		if e:
#			print e
#			self.exit()

		# идентификация		
		username = self.settings.option('ACCOUNT', 'username', '', True)
		password = self.settings.option('ACCOUNT', 'password', '', True)

		if not username:
			print _('no username')
			self.exit()

		if not password:
			print _('no password')
			self.exit()

		#загрузка модулей
		print _('loading modules')
		self.loadmodules()

		for module in self.modules:
			print '\t%s' % (module,)

		print

		# инициализация фронтенда
		frontend = self.settings.option('DATA', 'Frontend', '', True)

		if not frontend in self.modules:
			print _('no frontend %s') % (frontend,)
			self.exit()

		print _('frontend %s') % (frontend,)
		target = self.modules[frontend]()

		if target.error:
			print target.error
			self.exit()

		###
"""
		# получение данных по категориям
		for category in systemcategories:
			# получение данных
			print _('getting update')
			xmlfilename = self.settings.option('CONNECTION', 'debug')

			if xmlfilename:
				try:
					with open(xmlfilename) as xmlfile:
						data = xmlfile.read()

				except IOError, e:
					print _('no file %s') % (xmlfilename)
					self.exit()

			else:
				data = self.getupdate(username, password, category)

			# парсинг XML
			data = self.parseupdate(data)

			if not data:
				print _('no data')
				self.exit()

			# обработка данных
			fieldlist, content = self.sortupdate(category, data)

			# обновление локального источника
			target.set(category, fieldlist, content)

			if target.error:
				print target.error
				self.exit()

		print
		print 'Well done!'
"""

#######################


class MainWindow(QtGui.QMainWindow):

	def __init__(self, parent, *args):
		super(MainWindow, self).__init__(*args)
		uic.loadUi('ui/window.ui', self)
		self.w = QWorker(parent.getupdate, None, 'jack', 'passwd', 'Components')
		self.connect(self.w, QtCore.SIGNAL("data(QString)"), self.do)
		self.connect(self.w, QtCore.SIGNAL("ok(QString)"), self.end)

	@QtCore.pyqtSlot()
	def on_goButton_clicked(self):
		self.w.start()

	def do(self, text):
		self.m_label.setText(text)

	def end(self, data):
		self.m_label.setText(data)



class QWorker(QtCore.QThread):

	def __init__(self, callable, parent=None, *args, **kwargs):
		QtCore.QThread.__init__(self, parent)
		self.callable = callable
		self.args = args
		self.kwargs = kwargs
		print self.args, self.kwargs

	def run(self):
		data = ''

		try:
			data = self.callable(self, *self.args, **self.kwargs)

			print data
		except Exception, e:
			print e
			self.emit(QtCore.SIGNAL("exception()"), e)

		else:
			self.emit(QtCore.SIGNAL("ok(QString)"), data)



	def it(self, data=None):
		print data
		self.emit(QtCore.SIGNAL("data(QString)"), data)




if __name__ == '__main__':
	# modules directory
	modulespath = 'modules'

	# localization
	localepath = './locale'
	localefile = 'messages'

#	configfile = 'pyclient.ini'

	# connection
	defaultgeturl = 'http://noxius.ru/index2.php'
	defaultseturl = 'http://noxius.ru/index2.php'

	systemgetvariable = 'ip'
	systempostvariable = 'xml'

	# data
	systemcategories = ('Components',)# 'Resistors')
#	systemfieldlist = ('M', 'MN', 'PN', 'PC', 'D', 'URL', 'SYM', 'PKG', 'MDL', 'CD', 'MD', 'A')
	sysstrfields = ('M', 'MN', 'PN', 'PC', 'D', 'URL', 'SYM', 'PKG', 'MDL', 'A')
	sysdtfields = ('CD', 'MD')

	PyClient(sys.argv)