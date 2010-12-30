#-*- coding: utf-8 -*-

from PyQt4 import QtCore

from kernel import abstract
from kernel import wrapper

##################################

class PyMainWindow(abstract.QWindow):

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
		self.second = AddDialogWindow('ui/parameterdialog.ui')
		self.second.show()

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_addButton_respond(self, data=None):
		pass




class AddDialogWindow(abstract.QWindow):

	@QtCore.pyqtSlot()
	def on_okButton_clicked(self):
		print 'cool'

