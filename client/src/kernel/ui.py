#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from kernel import abstract
from kernel import wrapper

##################################

class PyMainWindow(abstract.QWindow):

	def refresh(self):
		wrapper.refresh_view(self)

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

	# delButton

	@QtCore.pyqtSlot()
	def on_delButton_clicked(self):
		self.parametersTable.removeRow(self.parametersTable.currentRow())

	# actionDrop menu item

	@QtCore.pyqtSlot()
	def on_actionDrop_triggered(self):
		wrapper.truncate_tables(self)
		wrapper.prepare_main_form(self)


	# componentButton

	@QtCore.pyqtSlot()
	def on_component_button_clicked(self):
		dialog = ComponentWizard('ui/component.ui', self)
#		dialog.setObjectName('Component Wizard')

		dialog.addComponentButton.clicked.connect(self.on_component_created)	#, QtCore.Qt.QueuedConnection)
		dialog.load(self.components)
		dialog.show()

	def on_component_created(self):
		print 'new component'
		wrapper.refresh_view(self)



	# SymbolButton

	@QtCore.pyqtSlot()
	def on_symbol_button_clicked(self):
		dialog = PackageWizard('ui/symbol.ui', self)
#		dialog.setObjectName('Symbol Manager')
		dialog.rewire()
		dialog.show()


	# PackageButton

	@QtCore.pyqtSlot()
	def on_package_button_clicked(self):
		dialog = PackageWizard('ui/package.ui', self)
#		dialog.setObjectName('Package Manager')

		dialog.accepted.connect(self.on_package_dialog_accept, QtCore.Qt.QueuedConnection)

		dialog.rewire()
		dialog.show()

	def on_package_dialog_accept(self, *args):
		print args
		print 'package manager accepted'



	def tet(self, arg):
		print 'tet', arg


	# ModelButton

	@QtCore.pyqtSlot()
	def on_model_button_clicked(self):
		dialog = PackageWizard('ui/model.ui', self)
#		dialog.setObjectName('Model Manager')
		dialog.rewire()
		dialog.show()


	# exportButton

	@QtCore.pyqtSlot()
	def on_export_button_clicked(self):
		wrapper.sync(self)



	@QtCore.pyqtSlot('PyQt_PyObject')
	def on_exportButton_respond(self, data=None):
		wrapper.export_respond(self, data)

	# downloadButton

	@QtCore.pyqtSlot()
	def on_downloadButton_clicked(self):
		wrapper.download_start(self)

	@QtCore.pyqtSlot('PyQt_PyObject')
	def on_downloadButton_respond(self, data=None):
		wrapper.download_respond(self, data)

	# uploadButton

	@QtCore.pyqtSlot()
	def on_uploadButton_clicked(self):
		wrapper.upload_start(self)

	@QtCore.pyqtSlot('PyQt_PyObject')
	def on_uploadButton_respond(self, data=None):
		wrapper.upload_respond(self, data)




class ComponentWizard(abstract.QDialog):

	def init(self):
		pass
#		self.worker = wrapper.PackageWorker()
#		self.worker.load()

	# okButton

	@QtCore.pyqtSlot()
	def on__clicked(self):
		print 'OK'

	@QtCore.pyqtSignature('PyQt_PyObject')
	def on_rejected(self, data=None):
		print 'Cancel'


	def load(self, components={}):
		""" загрузка начальных значений """
		manufacturers = []

		for component in components:
			manufacturers.append(components[component].manufacturer())

		manufacturers = list(set(manufacturers))
		manufacturers.sort()
		manufacturers.insert(0, ' ')

		self.manufacturerBox.addItems(manufacturers)


class PackageWizard(abstract.QDialog):

	accepted = QtCore.pyqtSignal(object)

	def rewire(self):
		self.worker = wrapper.PackageWorker()
		self.worker.load()

		self.buttonBox.accepted.connect(self.success)

	def success(self):
		print 'generating XML'
		self.accepted.emit('new component appeared')
