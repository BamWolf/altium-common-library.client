#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from kernel import abstract
from kernel import shared
from kernel import objects
from kernel import db

from datetime import datetime

###############################


class PutWrapper():

	def __init__(self):
		pass

	def before(self):
		pass

	def run(self, data):
		self.w = abstract.QWorker(shared.put, data = data, parent = self)

	def after(self):
		pass




### Add New Component ###

def put_start(self):
	self.putButton.setEnabled(False)

	component = objects.Component(unicode(self.manufacturerBox.currentText()), unicode(self.pn_line.text()))

	value = unicode(self.symbolBox.currentText())
	if value:
		parameter = objects.cParameter(u'SYM', value)
		component.set(parameter)

	value = unicode(self.packageBox.currentText())
	if value:
		parameter = objects.cParameter(u'PKG', value)
		component.set(parameter)

	value = unicode(self.modelBox.currentText())
	if value:
		parameter = objects.cParameter(u'MDL', value)
		component.set(parameter)

	value = unicode(self.descriptionEdit.toPlainText())
	if value:
		parameter = objects.cParameter(u'Description', value)
		component.set(parameter)

	value = unicode(self.linkEdit.text())
	if value:
		parameter = objects.cParameter(u'URL', value)
		component.set(parameter)

	row = 0
	while row < self.parametersTable.rowCount():
		# if not None
		pname = unicode(self.parametersTable.item(row, 0).text())
		pvalue = unicode(self.parametersTable.item(row, 1).text())
		ptype = unicode(self.parametersTable.item(row, 2).text())

		parameter = objects.cParameter(pname, pvalue, ptype)
		component.set(parameter)
		row = row + 1

	self.pw = abstract.QWorker(self, shared.do_put_process, component)
	self.connect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_putButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.pw.start()



def put_respond(self, data):
	self.disconnect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_putButton_respond)
	del self.pw

	self.m_label.setText("Component %s have been added" % (data,))
	print "Component %s have been added" % (data,)

	self.manufacturerBox.clearEditText()
	self.pn_line.clear()
	self.parametersTable.clearContents()
	self.parametersTable.setRowCount(0)

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


### Preparing Main Window ###

def prepare_main_form(self):

	database = db.Database(self.dbname)
	database.init()

	set = database.get_symbols()
	set.sort()

	for i in set:
		self.manufacturerBox.addItem(i)

	sl = database.get_symbols()
	sl.sort()

	for i in sl:
		self.symbolBox.addItem(i)

	pl = database.get_packages()
	pl.sort()

	for i in pl:
		self.packageBox.addItem(i)

	ml = database.get_models()
	ml.sort()

	for i in ml:
		self.modelBox.addItem(i)



### Adding New Parameter ###

def set_start(self):
	name = unicode(self.nameBox.currentText())
	value = unicode(self.valueEdit.text())

	mode = None
	for t in (self.stringRadio, self.floatRadio, self.datetimeRadio):
		mode =  (t.isChecked() and t.text()) or mode

	self.emit(QtCore.SIGNAL('add(PyQt_PyObject)'), objects.cParameter(name, value, mode))
	self.close()

def on_addButton_respond(self, data):
	self.disconnect(self.second, QtCore.SIGNAL('add(PyQt_PyObject)'), self.on_addButton_respond)

	i = self.parametersTable.rowCount()
	self.parametersTable.insertRow(i)

	self.parametersTable.setItem(i, 0, QtGui.QTableWidgetItem(data.name))
	self.parametersTable.setItem(i, 1, QtGui.QTableWidgetItem(data.value))
	self.parametersTable.setItem(i, 2, QtGui.QTableWidgetItem(data.type))
