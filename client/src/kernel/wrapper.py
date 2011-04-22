#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

import os
import sys

from kernel import abstract
from kernel import shared
from kernel import objects
from kernel import database
from kernel import utils
from datetime import datetime

###############################

accountoptionlist = {'login': '', 'password': ''}

SYMBOL = 'Symbol'
PACKAGE = 'Package'
MODEL = 'Model'

CATEGORY = 'Category'

URL = 'URL'
DESCRIPTION = 'Description'

AUTHOR = 'Author'
CREATIONTIME = 'CreationTime'

###############################

### Preparing Main Window ###

def prepare_view(self):
	settings = self.appconfig()

	xmlpath = os.path.abspath(settings.option('DATA', 'xmlrepository'))
	self.components = shared.collect_components(xmlpath)

	self.symbols = shared.collect_symbols(xmlpath)
	self.packages = shared.collect_packages(xmlpath)
	self.models = shared.collect_models(xmlpath)

	manufacturers = set()
	categories = set()

	for component in self.components.values():
		manufacturers.add(component.manufacturer())
		categories.add(component.get(CATEGORY))

	manufacturers = list(manufacturers)
	manufacturers.sort()
	self.manufacturerBox.addItems(manufacturers)
	self.manufacturerBox.setCurrentIndex(-1)

	categories = list(categories)
	categories.sort()
	self.categoryBox.addItems(categories)
	self.categoryBox.setCurrentIndex(-1)


def refresh_view(self):
	self.componentList.clear()
	self.componentList.addItems(self.components.keys())

	self.symbolBox.clear()
	items = self.symbols.keys()
	items.append(u'')
	items.sort()
	self.symbolBox.addItems(items)

	self.packageBox.clear()
	items = self.packages.keys()
	items.append(u'')
	items.sort()
	self.packageBox.addItems(items)

	self.modelBox.clear()
	items = self.models.keys()
	items.append(u'')
	items.sort()
	self.modelBox.addItems(items)


def load_categories(self):
	

	self.settings = utils.OptionManager('data/categories.ini')
#	self.settings.load()

	categories = self.settings.options('GOST', {}).keys()
	categories.sort()

	self.categoryBox.addItems(categories)

	self.settings = utils.OptionManager(self.inifile)


#def setup(self):

#	self.settings = utils.OptionManager('settings.ini')



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

#	component.set('CreationDate', datetime.utcnow(), 'datetime')

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


def sync(self):
	try:
		shared.sync(self)

	except abstract.AppException, e:
		print 'EXCEPTION:', e


class PackageWorker():

	def __init__(self):
		pass

	def load(self):
		selfpath = os.path.abspath(os.curdir)

		packagepath = os.path.join(selfpath, 'xml', 'packages')
		print 'xmlpath:', packagepath

		unique = {}

		import fnmatch
		import xml.etree.ElementTree as ElementTree

		for path, dirs, files in os.walk(packagepath):

			for filename in files:
				if fnmatch.fnmatch(filename, '*.xml'):
					if filename in unique:
						print 'Duplicate Error:', filename, path

					else:
						unique[filename] = os.path.abspath(os.path.join(path, filename))

		print unique

#		self.package_list.addItems(unique.keys())




def clear_info_view(self):
		self.manufacturerBox.lineEdit().setText('')
		self.partnumberEdit.setText('')

		self.categoryBox.lineEdit().setText('')

		self.symbolBox.setCurrentIndex(-1)
		self.packageBox.setCurrentIndex(-1)
		self.modelBox.setCurrentIndex(-1)

		self.linkEdit.setText('')
		self.descriptionEdit.clear()

def show_component_properties(self, selected):

	if selected:
		component = self.components[unicode(selected.text())]

		index = self.categoryBox.findText(component.get(CATEGORY))
		self.categoryBox.setCurrentIndex(index)

		self.manufacturerBox.lineEdit().setText(component.manufacturer())
		self.partnumberEdit.setText(component.partnumber())

#		self.symbolBox.lineEdit().setText(component.get(SYMBOL))
#		self.packageBox.lineEdit().setText(component.get(PACKAGE))
#		self.modelBox.lineEdit().setText(component.get(MODEL))

		index = self.symbolBox.findText(component.get(SYMBOL))
		self.symbolBox.setCurrentIndex(index)

		index = self.packageBox.findText(component.get(PACKAGE))
		self.packageBox.setCurrentIndex(index)

		index = self.modelBox.findText(component.get(MODEL))
		self.modelBox.setCurrentIndex(index)

		self.linkEdit.setText(component.get(URL))
		self.descriptionEdit.clear()
		self.descriptionEdit.insertPlainText(component.get(DESCRIPTION))


	else:
		clear_info_view(self)

def create_component(self):
	clear_info_view(self)

	self.editable = None

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def edit_component(self):
	self.editable = unicode(self.componentList.currentItem().text())

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def save_component(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)




	manufacturer = unicode(self.manufacturerBox.currentText())
	partnumber = unicode(self.partnumberEdit.text())

	component = objects.Component(manufacturer, partnumber)

	value = unicode(self.categoryBox.currentText())
	if value:
		parameter = objects.Parameter(CATEGORY, value)
		component.set(parameter)

	value = unicode(self.symbolBox.currentText())
	if value:
		parameter = objects.Parameter(SYMBOL, value)
		component.set(parameter)

	value = unicode(self.packageBox.currentText())
	if value:
		parameter = objects.Parameter(PACKAGE, value)
		component.set(parameter)

	value = unicode(self.modelBox.currentText())
	if value:
		parameter = objects.Parameter(MODEL, value)
		component.set(parameter)

	value = unicode(self.descriptionEdit.toPlainText())
	if value:
		parameter = objects.Parameter(DESCRIPTION, value)
		component.set(parameter)

	value = unicode(self.linkEdit.text())
	if value:
		parameter = objects.Parameter(URL, value)
		component.set(parameter)

	row = 0
	while row < self.parametersTable.rowCount():
		# if not None
		name = unicode(self.parametersTable.item(row, 0).text())
		value = unicode(self.parametersTable.item(row, 1).text())
		mode = unicode(self.parametersTable.item(row, 2).text())

		parameter = objects.Parameter(name, value, mode)
		component.set(parameter)
		row = row + 1

	parameter = objects.Parameter(AUTHOR, self.appconfig().option('ACCOUNT', 'user'))
	component.set(parameter)

	parameter = objects.Parameter(CREATIONTIME, datetime.utcnow(), 'datetime')
	component.set(parameter)

	if self.editable:
		del self.components[self.editable]

	self.components[component.id()] = component

	self.editable = None

#	prepare_view(self)
	refresh_view(self)

def cancel_component(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)

	current = self.componentList.currentItem()
	show_component_properties(self, current)
