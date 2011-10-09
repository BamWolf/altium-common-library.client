#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from kernel import abstract
from kernel import wrapper

##################################

class PyMainWindow(abstract.QWindow):

	def refresh(self):
		wrapper.refresh_view(self)

	def rewire(self):
		""" подключение сигналов """
		self.actionSettings.triggered.connect(self.on_settings_menu)
		self.actionExit.triggered.connect(self.application.exit)

		self.newButton.clicked.connect(self.on_new_button_clicked)
		self.editButton.clicked.connect(self.on_edit_button_clicked)
		self.saveButton.clicked.connect(self.on_save_button_clicked)
		self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

		self.symbolButton.clicked.connect(self.on_symbol_button_clicked)
		self.packageButton.clicked.connect(self.on_package_button_clicked)
		self.modelButton.clicked.connect(self.on_model_button_clicked)

		self.addButton.clicked.connect(self.on_add_button_clicked)
		self.delButton.clicked.connect(self.on_del_button_clicked)

		self.exportButton.clicked.connect(self.on_export_button_clicked)

		self.componentList.currentItemChanged.connect(self.on_item_changed)
		self.componentList.itemDoubleClicked.connect(self.on_item_doubleclicked)

		self.linkButton.clicked.connect(self.on_link_button_clicked)

		self.settings = self.appconfig()

		wrapper.refresh_view(self)


	# обработчики сигналов
	def on_settings_menu(self):
		import os
		os.system('settings.ini')

	def on_item_changed(self, current, previous):
		if current:
			self.editButton.setEnabled(True)
			wrapper.show_component(self, current)

		else:
			self.editButton.setEnabled(False)

	def on_item_doubleclicked(self, current):
			wrapper.show_component(self, current)
			wrapper.edit_component(self)

	# newButton
	def on_new_button_clicked(self):
		wrapper.create_component(self)

	# editButton
	def on_edit_button_clicked(self):
		wrapper.edit_component(self)

	# saveButton
	def on_save_button_clicked(self):
		wrapper.save_component(self)

	# cancelButton
	def on_cancel_button_clicked(self):
		wrapper.cancel_component(self)

	# addButton
	def on_add_button_clicked(self):
		wrapper.add_parameter(self)

	# delButton
	def on_del_button_clicked(self):
		wrapper.del_parameter(self)

	# symbolButton
	def on_symbol_button_clicked(self):
		dialog = SymbolManager('ui/symbol.ui', self)
		dialog.accepted.connect(self.on_symbol_dialog_accept, QtCore.Qt.QueuedConnection)
		dialog.load()
		dialog.rewire()
		dialog.show()

	def on_symbol_dialog_accept(self, data=None):
		wrapper.refresh_symbolbox(self)

	# packageButton
	def on_package_button_clicked(self):
		dialog = PackageManager('ui/package.ui', self)
		dialog.accepted.connect(self.on_package_dialog_accept, QtCore.Qt.QueuedConnection)
		dialog.load()
		dialog.rewire()
		dialog.show()

	def on_package_dialog_accept(self, *args):
		wrapper.refresh_packagebox(self)

	# modelButton
	def on_model_button_clicked(self):
		dialog = ModelManager('ui/model.ui', self)
		dialog.accepted.connect(self.on_model_dialog_accept, QtCore.Qt.QueuedConnection)
		dialog.load()
		dialog.rewire()
		dialog.show()

	def on_model_dialog_accept(self, data=None):
		wrapper.refresh_modelbox(self)

	# component link
	def on_link_button_clicked(self):
		wrapper.open_component_link(self)

	# on new component signal
	def on_component_created(self):
		wrapper.refresh_view(self)



	# exportButton
	def on_export_button_clicked(self):
		wrapper.sync(self)



class SymbolManager(abstract.QDialog):

	def success(self):
		print 'generating Symbol XML'
		self.accepted.emit('new symbol appeared')

	def load(self):
		wrapper.load_symbols(self)

#	def refresh(self):
#		wrapper.load_symbols(self)

	def rewire(self):
		""" подключение сигналов """
		self.newButton.clicked.connect(self.on_new_button_clicked)
		self.editButton.clicked.connect(self.on_edit_button_clicked)
		self.saveButton.clicked.connect(self.on_save_button_clicked)
		self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

		self.symbolList.currentItemChanged.connect(self.on_item_changed)

		self.openButton.clicked.connect(self.on_open_button_clicked)

#		wrapper.prepare_view(self)

	# обработчики сигналов
	def on_item_changed(self, current, previous):
#		if current:
#			self.editButton.setEnabled(True)
		wrapper.show_symbol(self, current)

#		else:
#			self.editButton.setEnabled(False)

	def on_new_button_clicked(self):
		wrapper.create_symbol(self)

	def on_edit_button_clicked(self):
		wrapper.edit_symbol(self)

	def on_save_button_clicked(self):
		wrapper.save_symbol(self)

	def on_cancel_button_clicked(self):
		wrapper.cancel_symbol(self)

	def on_open_button_clicked(self):
		wrapper.open_symbol(self)


class PackageManager(abstract.QDialog):

	def success(self):
		print 'generating Package XML'
		self.accepted.emit('new package appeared')

	def load(self):
		wrapper.load_packages(self)

	def rewire(self):
		""" подключение сигналов """
		self.newButton.clicked.connect(self.on_new_button_clicked)
		self.editButton.clicked.connect(self.on_edit_button_clicked)
		self.saveButton.clicked.connect(self.on_save_button_clicked)
		self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

		self.packageList.currentItemChanged.connect(self.on_item_changed)

		self.openButton.clicked.connect(self.on_open_button_clicked)
		self.openButton2.clicked.connect(self.on_open_button_2_clicked)
		self.openButton3.clicked.connect(self.on_open_button_3_clicked)

	# обработчики сигналов
	def on_item_changed(self, current, previous):
		if current:
			self.editButton.setEnabled(True)
			wrapper.show_package(self, current)

		else:
			self.editButton.setEnabled(False)

	def on_new_button_clicked(self):
		wrapper.create_package(self)

	def on_edit_button_clicked(self):
		wrapper.edit_package(self)

	def on_save_button_clicked(self):
		wrapper.save_package(self)

	def on_cancel_button_clicked(self):
		wrapper.cancel_package(self)

	def on_open_button_clicked(self):
		wrapper.open_package(self)

	def on_open_button_2_clicked(self):
		wrapper.open_package_2(self)

	def on_open_button_3_clicked(self):
		wrapper.open_package_3(self)


class ModelManager(abstract.QDialog):

	def success(self):
		print 'generating Model XML'
		self.accepted.emit('new model appeared')

	def load(self):
		wrapper.load_models(self)

	def rewire(self):
		""" подключение сигналов """
		self.newButton.clicked.connect(self.on_new_button_clicked)
		self.editButton.clicked.connect(self.on_edit_button_clicked)
		self.saveButton.clicked.connect(self.on_save_button_clicked)
		self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

		self.modelList.currentItemChanged.connect(self.on_item_changed)

	# обработчики сигналов
	def on_item_changed(self, current, previous):
		if current:
			self.editButton.setEnabled(True)
			wrapper.show_model(self, current)

		else:
			self.editButton.setEnabled(False)

	def on_new_button_clicked(self):
		wrapper.create_model(self)

	def on_edit_button_clicked(self):
		wrapper.edit_model(self)

	def on_save_button_clicked(self):
		wrapper.save_model(self)

	def on_cancel_button_clicked(self):
		wrapper.cancel_model(self)

	def on_open_button_clicked(self):
		wrapper.open_model(self)
