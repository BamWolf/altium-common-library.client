#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from kernel import abstract
from kernel import shared
from kernel import objects


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
	component = objects.Component(unicode(self.m_line.text()), unicode(self.pn_line.text()))

	row = 0
	while row < self.parametersTable.rowCount():
		# if not None
		pname = unicode(self.parametersTable.item(row, 0).text())
		pvalue = unicode(self.parametersTable.item(row, 1).text())
		ptype = unicode(self.parametersTable.item(row, 2).text())

		parameter = objects.cParameter(pname, pvalue, ptype)
		component.add_parameter(parameter)
		row = row + 1

	self.pw = abstract.QWorker(self, shared.do_put_process, component)
	self.connect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_putButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.pw.start()



def put_respond(self, data):
	self.disconnect(self.pw, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_putButton_respond)
	del self.pw

	self.m_label.setText("Component %s have been added" % (data,))
	print "Component %s have been added" % (data,)

	self.m_line.clear()
	self.pn_line.clear()
	self.parametersTable.clearContents()
	self.parametersTable.setRowCount(0)



### Get Update ###

def get_start(self):
	self.w = abstract.QWorker(self, shared.dosmthng, 'get')
	self.connect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_getButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.w.start()


def get_respond(self, data):
	self.disconnect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_getButton_respond)

	self.m_label.setText(str(data))




def do_get_iter(self, data=None):
	self.m_label.setText(str(data))




def prepare_main_form(self):
	pl = ['CR0805', 'CR1206', 'CR0603', 'CR0402']
	pl.sort()

	for i in pl:
		self.packageBox.addItem(i)

	sl = ['RES', 'CAP', 'VD']
	sl.sort()

	for i in sl:
		self.symbolBox.addItem(i)

	ml = ['RES', 'CAP']
	ml.sort()

	for i in ml:
		self.modelBox.addItem(i)



### Adding New Parameter ###

def add_parameter_start(self):
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
