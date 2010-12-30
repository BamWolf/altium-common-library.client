#-*- coding: utf-8 -*-

from PyQt4 import QtCore

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

	self.w = abstract.QWorker(self, shared.do_put_process, component)
	self.connect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_putButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.w.start()



def put_respond(self, data):
	self.disconnect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_putButton_respond)
	del self.w

	self.result_label.setText("Component %s have been added" % (data[0],))

	self.m_line.clear()
	self.pn_line.clear()
	self.parametersTable.clearContents()





def get_start(self):
	self.w = abstract.QWorker(self, shared.dosmthng, 'get')
	self.connect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), QtCore.SLOT('on_getButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
	self.w.start()


def get_respond(self, data):
	self.disconnect(self.w, QtCore.SIGNAL('exit(PyQt_PyObject)'), self.on_getButton_respond)

	self.m_label.setText(str(data))




def do_get_iter(self, data=None):
	self.m_label.setText(str(data))
