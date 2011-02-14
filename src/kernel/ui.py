#-*- coding: utf-8 -*-

from PyQt4 import QtCore
# временно
from PyQt4 import QtGui

from kernel import abstract
from kernel import wrapper

##################################

class PyMainWindow(abstract.QWindow):

	def prepare(self):
		wrapper.prepare_main_form(self)


	#
	@QtCore.pyqtSlot()
	def on_Error(self):
		self.parent._exit()


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
		wrapper.add_parameter(self)
#		self.second = AddDialogWindow('ui/parameterdialog.ui', self)
#		self.connect(self.second, QtCore.SIGNAL('add(PyQt_PyObject)'), QtCore.SLOT('on_addButton_respond(PyQt_PyObject)'), QtCore.Qt.QueuedConnection)
#		self.second.show()

#	@QtCore.pyqtSignature('PyQt_PyObject')
#	def on_addButton_respond(self, data=None):
#		wrapper.on_addButton_respond(self, data)


	# delButton

	@QtCore.pyqtSlot()
	def on_delButton_clicked(self):
		self.parametersTable.removeRow(self.parametersTable.currentRow())

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_delButton_respond(self, data=None):
		pass



	# actionDrop menu item

	@QtCore.pyqtSlot()
	def on_actionDrop_triggered(self):
		wrapper.truncate_tables(self)
		wrapper.prepare_main_form(self)



	# addSymbolButton

	@QtCore.pyqtSlot()
	def on_addSymbolButton_clicked(self):
		wrapper.add_symbol(self)

	# addPackageButton

	@QtCore.pyqtSlot()
	def on_addPackageButton_clicked(self):
		wrapper.add_package(self)

	# addModelButton

	@QtCore.pyqtSlot()
	def on_addModelButton_clicked(self):
		wrapper.add_model(self)

	# exportButton

	@QtCore.pyqtSlot()
	def on_exportButton_clicked(self):
		wrapper.export_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_exportButton_respond(self, data=None):
		wrapper.export_respond(self, data)

	# downloadButton

	@QtCore.pyqtSlot()
	def on_downloadButton_clicked(self):
		wrapper.download_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_downloadButton_respond(self, data=None):
		wrapper.download_respond(self, data)

	# uploadButton

	@QtCore.pyqtSlot()
	def on_uploadButton_clicked(self):
		wrapper.upload_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_uploadButton_respond(self, data=None):
		wrapper.upload_respond(self, data)




class AddDialogWindow(abstract.QWindow):

	# okButton

	@QtCore.pyqtSlot()
	def on_okButton_clicked(self):
		wrapper.add_parameter_start(self)

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_okButton_respond(self, data=None):
		wrapper.add_parameter_respond(self)
