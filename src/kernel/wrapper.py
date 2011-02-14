#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

import os

from kernel import abstract
from kernel import shared
from kernel import objects
from kernel import database
from kernel import utils

#from datetime import datetime

###############################

accountoptionlist = {'login': '', 'password': ''}

###############################

### Preparing Main Window ###

def prepare_main_form(self):

	self.settings = utils.OptionManager(self.inifile)
#	self.settings.load()

#	self.settings.initialize('ACCOUNT', accountoptionlist)

	db = database.Database(self.dbname)
	db.init()

	self.manufacturerBox.clear()
	set = db.get_man()
	set.append(u'')
	set.sort()
	self.manufacturerBox.addItems(set)

	self.symbolBox.clear()
	set = db.get_symbols()
	set.append(u'')
	set.sort()
	self.symbolBox.addItems(set)

	self.packageBox.clear()
	set = db.get_packages()
	set.append(u'')
	set.sort()
	self.packageBox.addItems(set)

	self.modelBox.clear()
	set = db.get_models()
	set.append(u'')
	set.sort()
	self.modelBox.addItems(set)

	db.close()

### Add New Component ###

def put_start(self):
	self.putButton.setEnabled(False)

	man = unicode(self.manufacturerBox.currentText())
	num = unicode(self.pn_line.text())
	component = objects.Component(man, num)

	value = unicode(self.categoryBox.currentText())
	component.set(u'Category', value)

	value = unicode(self.symbolBox.currentText())
	if value:
		component.set(u'Symbol', value)

	value = unicode(self.packageBox.currentText())
	if value:
		component.set(u'Package', value)

	value = unicode(self.modelBox.currentText())
	if value:
		component.set(u'Model', value)

	value = unicode(self.descriptionEdit.toPlainText())
	if value:
		component.set(u'Description', value)

	value = unicode(self.linkEdit.text())
	if value:
		component.set(u'URL', value)

	row = 0
	while row < self.parametersTable.rowCount():
		# if not None
		parameter = unicode(self.parametersTable.item(row, 0).text())
		value = unicode(self.parametersTable.item(row, 1).text())
		mode = unicode(self.parametersTable.item(row, 2).text())

		component.set(parameter, value, mode)
		row = row + 1

	self.pw = abstract.QWorker(self, shared.do_put_process, component)
	self.connect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_putButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.pw.start()



def put_respond(self, data):
	self.disconnect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_putButton_respond)
	del self.pw

	self.statusLabel.setText("Component %s have been added" % (data,))
	print "Component %s have been added" % (data,)

#	self.manufacturerBox.clearEditText()

#	self.symbolBox.setCurrentIndex(0)
#	self.packageBox.setCurrentIndex(0)
#	self.modelBox.setCurrentIndex(0)

	self.manufacturerBox.clear()

	self.symbolBox.clear()
	self.packageBox.clear()
	self.modelBox.clear()

	prepare_main_form(self)

	self.pn_line.clear()
	self.parametersTable.clearContents()
	self.parametersTable.setRowCount(0)

	if self.settings.modified:
		self.settings.save()

	self.putButton.setEnabled(True)



### Get Update ###

def download_start(self):
	self.downloadButton.setEnabled(False)

	self.dw = abstract.QWorker(self, shared.do_download, 'download')
	self.connect(self.dw, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_downloadButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.dw.start()


def download_respond(self, data):
	self.disconnect(self.dw, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_downloadButton_respond)
	del self.dw

	prepare_main_form(self)

	self.statusLabel.setText(str(data))
	self.downloadButton.setEnabled(True)


def download_iter(self, data=None):
	self.statusLabel.setText(str(data))


### Send Update ###

def upload_start(self):
	self.uploadButton.setEnabled(False)

	self.uw = abstract.QWorker(self, shared.do_upload, 'upload')
	self.connect(self.uw, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_uploadButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.uw.start()


def upload_respond(self, data):
	self.disconnect(self.uw, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_uploadButton_respond)
	del self.uw

	self.statusLabel.setText(str(data))
	self.uploadButton.setEnabled(True)




### Export ###

def export_start(self):
	self.exportButton.setEnabled(False)

	self.ew = abstract.QWorker(self, shared.do_export, 'export')
	self.connect(self.ew, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_exportButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.ew.start()


def export_respond(self, data):
	self.disconnect(self.ew, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_exportButton_respond)

	self.statusLabel.setText(str(data))

	self.exportButton.setEnabled(True)





def add_symbol(self):
	defaultpath = self.settings.option('DATA', 'repository')
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .SCHLib file', defaultpath, 'SCH Library File (*.schlib)')
	symbol = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	if not symbol:
		return

	print symbol

	db = database.Database(self.dbname)

	if not db.get_symbol(symbol):
		db.set_symbol(symbol)

	db.close()

	prepare_main_form(self)
	index = self.symbolBox.findText(symbol)

	print index

	self.symbolBox.setCurrentIndex(index)

#	self.packageBox.setCurrentIndex(self.packageBox.count() - 1)

def add_package(self):
	defaultpath = self.settings.option('DATA', 'repository')
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .PCBLib file', defaultpath, 'PCB Library File (*.pcblib)')
	package = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	if not package:
		return

	index = self.packageBox.findText(package)

	print index

	if index == -1:
		db = database.Database(self.dbname)
		db.set_package(package)
		db.close()
		self.packageBox.addItem(package)

	print self.packageBox.count()

	self.packageBox.setCurrentIndex(self.packageBox.count() - 1)


def add_model(self):
	defaultpath = self.settings.option('DATA', 'repository')
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .MDL file', defaultpath, 'Model Library File (*.mdl *.ckt)')
	model = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	print model


### TRUNCATE TABLES ###

def truncate_tables(self):
	db = database.Database(self.dbname)
	db.clear()



class ItemBox():
	def __init__(self, widget, table):
		self.widget = widget
		self.table = table

	def reload(self):
		pass


### Adding New Parameter ###

def add_parameter(self):
	parameter = unicode(self.nameBox.currentText())
	value = unicode(self.valueEdit.text())

	mode = None
	for t in (self.stringRadio, self.numberRadio):	#, self.datetimeRadio):
		mode =  (t.isChecked() and t.text()) or mode

	self.emit(QtCore.SIGNAL('add(PyQt_PyObject)'), (parameter, value, mode))

#	self.disconnect(self.second, QtCore.SIGNAL('add(PyQt_PyObject)'), self.on_addButton_respond)

	if parameter:
		i = self.parametersTable.rowCount()
		self.parametersTable.insertRow(i)

		self.parametersTable.setItem(i, 0, QtGui.QTableWidgetItem(parameter))
		self.parametersTable.setItem(i, 1, QtGui.QTableWidgetItem(value))
		self.parametersTable.setItem(i, 2, QtGui.QTableWidgetItem(mode))

		self.nameBox.setCurrentIndex(0)
		self.valueEdit.setText('')
		self.stringRadio.setChecked(True)
