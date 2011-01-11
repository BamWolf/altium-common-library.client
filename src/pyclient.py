#-*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtGui

from kernel.ui import PyMainWindow

from kernel.plugin import plugin as pyplugin

from kernel.utils import OptionManager
#from kernel.db import Database

#import gettext
from kernel import i18n

#########################

class PyClient(QtGui.QApplication):

	def __init__(self, *argv):
		QtGui.QApplication.__init__(self, *argv)

		self.settings = OptionManager(configfile)
		self.settings.read()

		self.ui = PyMainWindow('ui/mainwindow.ui')
		self.ui.settings = self.settings

		self.ui.prepare()
		self.ui.show()




if __name__ == '__main__':
	# modules directory
	modulespath = 'modules'

	# localization
	localepath = './locale'
	localefile = 'messages'

	configfile = 'pyclient.ini'

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

	i = PyClient(sys.argv)
	i.exec_()
	