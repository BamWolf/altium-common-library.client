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

	# определяем путь к программе

	selfpath = os.path.abspath(os.curdir)
	print 'selfpath:', selfpath

	# путь к папке плагинами

	modulepath = os.path.join(selfpath, 'modules')
	print 'modulepath:', modulepath

	# добавление папки плагинов в sys.path
	sys.path.insert(0, modulepath)

	# localization
	localepath = './locale'
	localefile = 'messages'

	inifile = os.path.join(selfpath, 'config.ini')

	print 'inifile:', inifile

	i = PyClient(sys.argv)
	i.exec_()
	