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

def _(string):
	return string

###############################

### Preparing Main Window ###

def prepare_view(self):
	self.settings = self.appconfig()

	refresh_view(self)

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

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.components = shared.collect_components(xmlpath)

	items = self.components.keys()
	items.sort()
	self.componentList.clear()
	self.componentList.addItems(items)

	refresh_symbolbox(self)
	refresh_packagebox(self)
	refresh_modelbox(self)

def refresh_symbolbox(self):

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.symbols = shared.collect_symbols(xmlpath)

	items = self.symbols.keys()
	items.append(u'')
	items.sort()

	self.symbolBox.clear()
	self.symbolBox.addItems(items)

def refresh_packagebox(self):

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.packages = shared.collect_packages(xmlpath)

	items = self.packages.keys()
	items.append(u'')
	items.sort()

	self.packageBox.clear()
	self.packageBox.addItems(items)

def refresh_modelbox(self):

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.models = shared.collect_models(xmlpath)

	items = self.models.keys()
	items.append(u'')
	items.sort()

	self.modelBox.clear()
	self.modelBox.addItems(items)









def load_categories(self):

	self.settings = utils.OptionManager('data/categories.ini')
#	self.settings.load()

	categories = self.settings.options('GOST', {}).keys()
	categories.sort()

	self.categoryBox.addItems(categories)

	self.settings = utils.OptionManager(self.inifile)





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




def show_component(self, selected):

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
		clear_component(self)

def clear_component(self):
		self.manufacturerBox.lineEdit().setText('')
		self.partnumberEdit.setText('')

		self.categoryBox.lineEdit().setText('')

		self.symbolBox.setCurrentIndex(-1)
		self.packageBox.setCurrentIndex(-1)
		self.modelBox.setCurrentIndex(-1)

		self.linkEdit.setText('')
		self.descriptionEdit.clear()



def create_component(self):
	clear_component(self)

	self.editable = None

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def edit_component(self):
	self.editable = unicode(self.componentList.currentItem().text())

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def save_component(self):
	settings = self.appconfig()

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

	parameter = objects.Parameter(AUTHOR, settings.option('ACCOUNT', 'user'))
	component.set(parameter)

	parameter = objects.Parameter(CREATIONTIME, datetime.utcnow().isoformat(' '), 'datetime')
	component.set(parameter)

	### сохранение файла

	xmldata = component.xml()

	componentpath = os.path.join(settings.option('DATA', 'xmlrepository'), 'components')
	container = '.'.join((manufacturer.upper(), partnumber.upper(), 'xml'))
	filename = os.path.join(componentpath, container)

	try:
		with (open(filename, 'w')) as xmlfile:
			xmlfile.write(xmldata)

	except IOError, e:
		message = _('cannot save file: %s') % (e,)
		self.statusbar.showMessage(message)
		return

	if self.editable:
		try:
			os.remove(self.components[self.editable])
			del self.components[self.editable]

		except OSError, e:
			self.statusbar.showMessage(e)
			return

	self.infoWidget.setEnabled(False)
	self.components[component.id()] = component
	self.editable = None
	refresh_view(self)
	self.listWidget.setEnabled(True)


def cancel_component(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)

	current = self.componentList.currentItem()
	show_component(self, current)
	self.statusbar.clearMessage()


###############################
#
# SYMBOL MANAGER SECTION
#
###############################

def load_symbols(self):
	self.settings = self.parent().appconfig()

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.symbols = shared.collect_symbols(xmlpath)

	items = self.symbols.keys()
	items.sort()

	self.symbolList.clear()
	self.symbolList.addItems(items)

	designators = set()

	for symbol in self.symbols.values():
		designators.add(symbol.get(u'Designator'))

	designators = list(designators)
	designators.sort()
	self.designatorBox.addItems(designators)
	self.designatorBox.setCurrentIndex(-1)

def show_symbol(self, selected):
	if selected:
		symbol = self.symbols[unicode(selected.text())]
		print symbol

		self.nameEdit.setText(symbol.id())
		self.referrenceEdit.setText(symbol.get(u'Referrence'))

		index = self.designatorBox.findText(symbol.get(u'Designator'))
		self.designatorBox.setCurrentIndex(index)

		self.descriptionEdit.clear()
		self.descriptionEdit.insertPlainText(symbol.get(DESCRIPTION))

	else:
		clear_symbol(self)

def clear_symbol(self):
	self.nameEdit.setText('')
	self.referrenceEdit.setText('')

	self.designatorBox.lineEdit().setText('')
	self.descriptionEdit.clear()

def create_symbol(self):
	clear_symbol(self)

	self.editable = None

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def edit_symbol(self):
	self.editable = unicode(self.symbolList.currentItem().text())

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def save_symbol(self):
	name = unicode(self.nameEdit.text())

	symbol = objects.Symbol(name)

	value = unicode(self.designatorBox.currentText())
	if value:
		parameter = objects.Parameter(u'Designator', value)
		symbol.set(parameter)

	value = unicode(self.descriptionEdit.toPlainText())
	if value:
		parameter = objects.Parameter(DESCRIPTION, value)
		symbol.set(parameter)

	value = unicode(self.referrenceEdit.text())
	if value:
		parameter = objects.Parameter(u'Referrence', value)
		symbol.set(parameter)

#	parameter = objects.Parameter(AUTHOR, settings.option('ACCOUNT', 'user'))
#	component.set(parameter)

#	parameter = objects.Parameter(CREATIONTIME, datetime.utcnow().isoformat(' '), 'datetime')
#	component.set(parameter)

	### сохранение файла

	xmldata = symbol.xml()

	symbolpath = os.path.join(self.settings.option('DATA', 'xmlrepository'), 'symbols')
	container = '.'.join((name.upper(), 'xml'))
	filename = os.path.abspath(os.path.join(symbolpath, container))

	try:
		with (open(filename, 'w')) as xmlfile:
			xmlfile.write(xmldata)

	except IOError, e:
		message = _('cannot save file: %s') % (e,)
#		self.statusbar.showMessage(message)
		return

	if self.editable == symbol.id():
		del self.symbols[self.editable]
		### удаление файла

	self.infoWidget.setEnabled(False)
	self.symbols[symbol.id()] = symbol
	self.editable = None
	load_symbols(self)
	self.listWidget.setEnabled(True)



def cancel_symbol(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)

	current = self.symbolList.currentItem()
	show_symbol(self, current)
#	self.statusbar.clearMessage()

def open_symbol(self):
	defaultpath = os.path.abspath(self.settings.option('DATA', 'datarepository'))
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .SCHLib file', defaultpath, 'SCH Library File (*.schlib)')
	symbol = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	self.referrenceEdit.setText(symbol)


###############################
#
# PACKAGE MANAGER SECTION
#
###############################

def load_packages(self):
	self.settings = self.parent().appconfig()

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.packages = shared.collect_packages(xmlpath)

	items = self.packages.keys()
	items.sort()

	self.packageList.clear()
	self.packageList.addItems(items)

def show_package(self, selected):

	if selected:
		package = self.packages[unicode(selected.text())]

		self.nameEdit.setText(package.id())
		self.linkEdit.setText(package.get(URL))

		self.referrenceEdit.setText(package.get(u'Referrence'))
		self.referrenceEdit2.setText(package.get(u'Referrence2'))
		self.referrenceEdit3.setText(package.get(u'Referrence3'))

		self.descriptionEdit.clear()
		self.descriptionEdit.insertPlainText(package.get(DESCRIPTION))

	else:
		clear_package(self)

def clear_package(self):
	self.nameEdit.setText('')
	self.linkEdit.setText('')

	self.referrenceEdit.setText('')
	self.referrenceEdit2.setText('')
	self.referrenceEdit3.setText('')

	self.descriptionEdit.clear()

def create_package(self):
	clear_package(self)

	self.editable = None

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def edit_package(self):
	self.editable = unicode(self.packageList.currentItem().text())

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def save_package(self):
	name = unicode(self.nameEdit.text())
	package = objects.Package(name)

	value = unicode(self.referrenceEdit.text())
	if value:
		parameter = objects.Parameter(u'Referrence', value)
		package.set(parameter)

	value = unicode(self.referrenceEdit2.text())
	if value:
		parameter = objects.Parameter(u'Referrence2', value)
		package.set(parameter)

	value = unicode(self.referrenceEdit3.text())
	if value:
		parameter = objects.Parameter(u'Referrence3', value)
		package.set(parameter)

	value = unicode(self.descriptionEdit.toPlainText())
	if value:
		parameter = objects.Parameter(DESCRIPTION, value)
		package.set(parameter)

	value = unicode(self.linkEdit.text())
	if value:
		parameter = objects.Parameter(URL, value)
		package.set(parameter)



#	parameter = objects.Parameter(AUTHOR, self.settings.option('ACCOUNT', 'user'))
#	package.set(parameter)

#	parameter = objects.Parameter(CREATIONTIME, datetime.utcnow().isoformat(' '), 'datetime')
#	package.set(parameter)

	### сохранение файла

	xmldata = package.xml()

	packagepath = os.path.join(self.settings.option('DATA', 'xmlrepository'), 'packages')
	container = '.'.join((name.upper(), 'xml'))
	filename = os.path.abspath(os.path.join(packagepath, container))

	try:
		with (open(filename, 'w')) as xmlfile:
			xmlfile.write(xmldata)

	except IOError, e:
		message = _('cannot save file: %s') % (e,)
		return

	if self.editable == package.id():
		del self.packages[self.editable]
		### удаление файла

	self.infoWidget.setEnabled(False)
	self.packages[package.id()] = package
	self.editable = None
	load_packages(self)
	self.listWidget.setEnabled(True)


def cancel_package(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)

	current = self.packageList.currentItem()
	show_package(self, current)


def open_package(self):
	defaultpath = os.path.abspath(self.settings.option('DATA', 'datarepository'))
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .PCBLib file', defaultpath, 'PCB Library File (*.pcblib)')
	symbol = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	self.referrenceEdit.setText(symbol)

def open_package_2(self):
	defaultpath = os.path.abspath(self.settings.option('DATA', 'datarepository'))
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .PCBLib file', defaultpath, 'PCB Library File (*.pcblib)')
	symbol = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	self.referrenceEdit2.setText(symbol)

def open_package_3(self):
	defaultpath = os.path.abspath(self.settings.option('DATA', 'datarepository'))
	filename = QtGui.QFileDialog.getOpenFileName(self, 'Select .PCBLib file', defaultpath, 'PCB Library File (*.pcblib)')
	symbol = os.path.splitext(os.path.basename(unicode(filename)))[0].upper()

	self.referrenceEdit3.setText(symbol)


###############################
#
# MODEL MANAGER SECTION
#
###############################

def load_models(self):
	self.settings = self.parent().appconfig()

	xmlpath = os.path.abspath(self.settings.option('DATA', 'xmlrepository'))
	self.models = shared.collect_packages(xmlpath)

def clear_model(self):
	self.manufacturerBox.lineEdit().setText('')
	self.partnumberEdit.setText('')

	self.categoryBox.lineEdit().setText('')

	self.modelBox.setCurrentIndex(-1)
	self.packageBox.setCurrentIndex(-1)
	self.modelBox.setCurrentIndex(-1)

	self.linkEdit.setText('')
	self.descriptionEdit.clear()

def show_model(self, selected):

	if selected:
		component = self.components[unicode(selected.text())]

		index = self.categoryBox.findText(component.get(CATEGORY))
		self.categoryBox.setCurrentIndex(index)

		self.manufacturerBox.lineEdit().setText(component.manufacturer())
		self.partnumberEdit.setText(component.partnumber())

#		self.modelBox.lineEdit().setText(component.get(model))
#		self.packageBox.lineEdit().setText(component.get(PACKAGE))
#		self.modelBox.lineEdit().setText(component.get(MODEL))

		index = self.modelBox.findText(component.get(model))
		self.modelBox.setCurrentIndex(index)

		index = self.packageBox.findText(component.get(PACKAGE))
		self.packageBox.setCurrentIndex(index)

		index = self.modelBox.findText(component.get(MODEL))
		self.modelBox.setCurrentIndex(index)

		self.linkEdit.setText(component.get(URL))
		self.descriptionEdit.clear()
		self.descriptionEdit.insertPlainText(component.get(DESCRIPTION))


	else:
		clear_info_view(self)

def create_model(self):
	clear_info_view(self)

	self.editable = None

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def edit_model(self):
	self.editable = unicode(self.componentList.currentItem().text())

	self.infoWidget.setEnabled(True)
	self.listWidget.setEnabled(False)

def save_model(self):
	manufacturer = unicode(self.manufacturerBox.currentText())
	partnumber = unicode(self.partnumberEdit.text())

	component = objects.Component(manufacturer, partnumber)

	value = unicode(self.categoryBox.currentText())
	if value:
		parameter = objects.Parameter(CATEGORY, value)
		component.set(parameter)

	value = unicode(self.modelBox.currentText())
	if value:
		parameter = objects.Parameter(model, value)
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

	parameter = objects.Parameter(AUTHOR, self.settings.option('ACCOUNT', 'user'))
	component.set(parameter)

	parameter = objects.Parameter(CREATIONTIME, datetime.utcnow().isoformat(' '), 'datetime')
	component.set(parameter)

	### сохранение файла

	xmldata = component.xml()

	componentpath = os.path.join(settings.option('DATA', 'xmlrepository'), 'components')
	container = '.'.join((manufacturer.upper(), partnumber.upper(), 'xml'))
	filename = os.path.join(componentpath, container)

	try:
		with (open(filename, 'w')) as xmlfile:
			xmlfile.write(xmldata)

	except IOError, e:
		message = _('cannot save file: %s') % (e,)
#		self.statusbar.showMessage(message)
		return

	if self.editable:
		del self.components[self.editable]

	self.infoWidget.setEnabled(False)
	self.components[component.id()] = component
	self.editable = None
	refresh_view(self)
	self.listWidget.setEnabled(True)

def cancel_model(self):
	self.infoWidget.setEnabled(False)
	self.listWidget.setEnabled(True)

	current = self.componentList.currentItem()
	show_component_properties(self, current)
#	self.statusbar.clearMessage()
