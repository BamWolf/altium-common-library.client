#-*- coding: utf-8 -*-

from PyQt4 import QtCore

from kernel import abstract
from kernel import wrapper

##################################

class PyMainWindow(abstract.QWindow):

	def prepare(self):
		wrapper.prepare_main_form(self)

	# getButton

	@QtCore.pyqtSlot()
	def on_getButton_clicked(self):
		wrapper.get_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_getButton_respond(self, data=None):
		wrapper.get_respond(self, data)

	# putButton

	@QtCore.pyqtSlot()
	def on_putButton_clicked(self):
		wrapper.put_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_putButton_respond(self, data=None):
		wrapper.put_respond(self, data)

	# addButton

	@QtCore.pyqtSlot()
	def on_addButton_clicked(self):
		self.second = AddDialogWindow('ui/parameterdialog.ui', self)

		self.connect(self.second, QtCore.SIGNAL('add(PyQt_PyObject)'), QtCore.SLOT('on_addButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)

		self.second.show()

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_addButton_respond(self, data=None):
		wrapper.on_addButton_respond(self, data)


	# delButton

	@QtCore.pyqtSlot()
	def on_delButton_clicked(self):
		self.parametersTable.removeRow(self.parametersTable.currentRow())

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_delButton_respond(self, data=None):
		pass



class AddDialogWindow(abstract.QWindow):

	# okButton

	@QtCore.pyqtSlot()
	def on_okButton_clicked(self):
		wrapper.add_parameter_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_okButton_respond(self, data=None):
		wrapper.add_parameter_respond(self)
