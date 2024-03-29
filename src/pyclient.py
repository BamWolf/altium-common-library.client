#-*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from kernel.ui import PyMainWindow

#import gettext
from kernel import i18n

#########################

class PyClient(QtGui.QApplication):

	def __init__(self, *argv):
		QtGui.QApplication.__init__(self, *argv)

#		self.settings = OptionManager(inifile)
#		self.settings.load()

#		self.settings.initialize('ACCOUNT', accountoptionlist)

#		if self.settings.modified:
#			self.settings.save()

		self.ui = PyMainWindow('ui/mainwindow.ui')

		self.ui.prepare()
		self.ui.show()





if __name__ == '__main__':
	# modules directory
	modulespath = 'modules'

	# localization
	localepath = './locale'
	localefile = 'messages'

	inifile = 'pyclient.ini'

	i = PyClient(sys.argv)
	i.exec_()
	