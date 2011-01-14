#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from kernel import abstract
from kernel import shared
from kernel import objects
from kernel import db
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

	database = db.Database(self.dbname)

	set = database.get_man()
	set.append(u'')
	set.sort()

	for i in set:
		self.manufacturerBox.addItem(i)

	set = database.get_symbols()
	set.append(u'')
	set.sort()

	for i in set:
		self.symbolBox.addItem(i)

	set = database.get_packages()
	set.append(u'')
	set.sort()

	for i in set:
		self.packageBox.addItem(i)

	set = database.get_models()
	set.append(u'')
	set.sort()

	for i in set:
		self.modelBox.addItem(i)



### Add New Component ###

def put_start(self):
	self.putButton.setEnabled(False)

	man = unicode(self.manufacturerBox.currentText())
	num = unicode(self.pn_line.text())
	component = objects.Component(man, num)

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

	self.m_label.setText("Component %s have been added" % (data,))
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

def get_start(self):
	self.getButton.setEnabled(False)

	self.w = abstract.QWorker(self, shared.dosmthng, 'get')
	self.connect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_getButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.w.start()


def get_respond(self, data):
	self.disconnect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_getButton_respond)

	self.m_label.setText(str(data))

	self.getButton.setEnabled(True)


def do_get_iter(self, data=None):
	self.m_label.setText(str(data))



### Adding New Parameter ###

def add_parameter_start(self):
	parameter = unicode(self.nameBox.currentText())
	value = unicode(self.valueEdit.text())

	mode = None
	for t in (self.stringRadio, self.floatRadio, self.datetimeRadio):
		mode =  (t.isChecked() and t.text()) or mode

	self.emit(QtCore.SIGNAL('add(PyQt_PyObject)'), (parameter, value, mode))
	self.close()



def on_addButton_respond(self, data):
	self.disconnect(self.second, QtCore.SIGNAL('add(PyQt_PyObject)'), self.on_addButton_respond)

	i = self.parametersTable.rowCount()
	self.parametersTable.insertRow(i)

	parameter, value, mode = data

	if parameter:
		self.parametersTable.setItem(i, 0, QtGui.QTableWidgetItem(parameter))
		self.parametersTable.setItem(i, 1, QtGui.QTableWidgetItem(value))
		self.parametersTable.setItem(i, 2, QtGui.QTableWidgetItem(mode))
