from enum import Enum
from PyQt6.QtWidgets import QMenuBar, QFileDialog, QDialog, QLineEdit, QLabel, QPushButton, QMessageBox, QGridLayout, QVBoxLayout, QHBoxLayout, QLayout
from PyQt6.QtGui import QAction, QIntValidator, QIcon
from PyQt6.QtCore import pyqtSignal

import json

from ReactorGrid import ReactorGridEncoder
from Assets import Assets
from Settings import Settings, Keybinds
from Materials import MaterialDialog
from Options import OptionsDialog


class DialogResult(Enum):
	Yes = 0
	No = 1
	Cancel = 2


class MenuBar(QMenuBar):
	signal_on_dialog_new_accepted = pyqtSignal(int, int)

	def __init__(self, parent=None):
		super().__init__(parent)

		# File menu
		filemenu = self.addMenu("File")

		file_new_action = QAction("New", filemenu)
		file_new_action.setShortcut(Keybinds().get("New"))
		Keybinds().connect_action("New", file_new_action)
		self.signal_new_state = file_new_action.triggered
		filemenu.addAction(file_new_action)

		file_open_action = QAction("Open", filemenu)
		file_open_action.setShortcut(Keybinds().get("Open"))
		Keybinds().connect_action("Open", file_open_action)
		self.signal_load_state = file_open_action.triggered
		filemenu.addAction(file_open_action)

		file_save_action = QAction("Save", filemenu)
		file_save_action.setShortcut(Keybinds().get("Save"))
		Keybinds().connect_action("Save", file_save_action)
		self.signal_save_state = file_save_action.triggered
		filemenu.addAction(file_save_action)

		file_saveas_action = QAction("Save As", filemenu)
		file_saveas_action.setShortcut(Keybinds().get("Save As"))
		Keybinds().connect_action("Save As", file_saveas_action)
		self.signal_save_state_as = file_saveas_action.triggered
		filemenu.addAction(file_saveas_action)

		filemenu.addSeparator()

		file_exit_action = QAction("Quit", filemenu)
		file_exit_action.setShortcut(Keybinds().get("Quit"))
		Keybinds().connect_action("Quit", file_exit_action)
		self.signal_quit = file_exit_action.triggered
		filemenu.addAction(file_exit_action)

		# Edit menu
		editmenu = self.addMenu("Edit")

		self.edit_undo_action = QAction("Undo", editmenu)
		self.signal_undo = self.edit_undo_action.triggered
		self.edit_undo_action.setShortcut(Keybinds().get("Undo"))
		Keybinds().connect_action("Undo", self.edit_undo_action)
		self.edit_undo_action.setDisabled(True)
		editmenu.addAction(self.edit_undo_action)

		self.edit_redo_action = QAction("Redo", editmenu)
		self.signal_redo = self.edit_redo_action.triggered
		self.edit_redo_action.setDisabled(True)
		self.edit_redo_action.setShortcut(Keybinds().get("Redo"))
		Keybinds().connect_action("Redo", self.edit_redo_action)
		editmenu.addAction(self.edit_redo_action)

		editmenu.addSeparator()

		edit_opts_action = QAction("Options", editmenu)
		edit_opts_action.setShortcut(Keybinds().get("Options"))
		Keybinds().connect_action("Options", edit_opts_action)
		self.signal_options = edit_opts_action.triggered
		editmenu.addAction(edit_opts_action)

		# Tools menu
		toolsmenu = self.addMenu("Tools")
		tool_cost_action = QAction("Material cost", toolsmenu)
		tool_cost_action.setShortcut(Keybinds().get("Material cost"))
		Keybinds().connect_action("Material cost", tool_cost_action)
		self.signal_material_cost = tool_cost_action.triggered
		toolsmenu.addAction(tool_cost_action)

		# Help menu
		helpmenu = self.addMenu("Help")
		help_reme_action = QAction("Readme", helpmenu)
		help_reme_action.setShortcut(Keybinds().get("Readme"))
		Keybinds().connect_action("Readme", help_reme_action)
		self.signal_readme = help_reme_action.triggered
		helpmenu.addAction(help_reme_action)

		help_about_action = QAction("About", helpmenu)
		help_about_action.setShortcut(Keybinds().get("About"))
		Keybinds().connect_action("About", help_about_action)
		self.signal_about = help_about_action.triggered
		helpmenu.addAction(help_about_action)

		# New project dialog
		self.dialog_new = InputDialog()
		self.dialog_new.accepted.connect(self.dialog_new_accepted)

		self.root_dir = Settings().get("RootDir")


	def enable_undo(self):
		self.edit_undo_action.setEnabled(True)


	def enable_redo(self):
		self.edit_redo_action.setEnabled(True)


	def disable_undo(self):
		self.edit_undo_action.setDisabled(True)


	def disable_redo(self):
		self.edit_redo_action.setDisabled(True)


	def readme_window(self):
		qmbox = QMessageBox()
		qmbox.setText(Assets().readme_message)
		qmbox.setWindowTitle("Hello, this is help.")
		qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
		x = qmbox.exec()


	def about_window(self):
		qmbox = QMessageBox()
		qmbox.setText(Assets().about_message)
		qmbox.setWindowTitle("About this wonderful tool.")
		qmbox.setStandardButtons(QMessageBox.StandardButtons.Close)
		x = qmbox.exec()


	def materials_window(self, data):
		matwin = MaterialDialog(data)
		x = matwin.exec()


	def options_window(self):
		optwin = OptionsDialog()
		x = optwin.exec()


	def save_state(self, file_name, data):
		try:
			with open(file_name, 'w') as output:
				json.dump(data, output, cls=ReactorGridEncoder, separators=(',', ':'))
		except OSError:
			return False
		self.change_root_dir(file_name[:file_name.rfind("/")])
		return True


	def prompt_save_file_name(self):
		file_name = QFileDialog.getSaveFileName(None, "Save file", self.root_dir, "JSON files (*.json)")[0]
		if file_name != "":
			if len(file_name) < 5 or file_name[-5:] != ".json":
				file_name += ".json"
			return file_name
		else:
			return None


	def ask_to_save_first(self):
		message_box = QMessageBox()
		message_box.setIcon(QMessageBox.Icon.Question)
		message_box.setText("Save changes to the current project?")
		message_box.setWindowTitle("You have unsaved changes")
		message_box.setStandardButtons(QMessageBox.StandardButtons.Yes | QMessageBox.StandardButtons.No | QMessageBox.StandardButtons.Cancel)
		message_box.setDefaultButton(QMessageBox.StandardButtons.Yes)
		message_box.setEscapeButton(QMessageBox.StandardButtons.Cancel)
		standardButton = message_box.exec()
		if QMessageBox.StandardButtons(standardButton) is QMessageBox.StandardButtons.Yes:
			return DialogResult.Yes
		elif QMessageBox.StandardButtons(standardButton) is QMessageBox.StandardButtons.Cancel:
			return DialogResult.Cancel
		else:
			return DialogResult.No


	def load_state(self):
		open_file_name = ""
		open_file_name = QFileDialog.getOpenFileName(None, "Open file", self.root_dir, "JSON files (*.json)")
		if (len(open_file_name) > 0):
			if ((len(open_file_name[0]) > 5) and (open_file_name[0][-5:] == ".json")):
				self.change_root_dir(open_file_name[0][:open_file_name[0].rfind("/")])
				with open(open_file_name[0], "r") as input:
					return (open_file_name[0], json.load(input))
		return None


	def open_dialog_new_state(self):
		self.dialog_new.open()


	def dialog_new_accepted(self):
		text_width = self.dialog_new.line1.text()
		text_height = self.dialog_new.line2.text()
		width = 0 if text_width == "" else int(text_width)
		height = 0 if text_height == "" else int(text_height)
		if width == 0:
			width = 1
		if height == 0:
			height = 1
		self.signal_on_dialog_new_accepted.emit(width, height)

	def change_root_dir(self, new_root):
		self.root_dir = new_root
		Settings().set("RootDir", self.root_dir)


class InputDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("New project")

		self.validator = QIntValidator(0, 99)

		vbox_layout = QVBoxLayout(self)
		hbox_layout = QHBoxLayout()
		grid_layout = QGridLayout()
		vbox_layout.addLayout(grid_layout)
		vbox_layout.addLayout(hbox_layout)
		vbox_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

		label1 = QLabel(self)
		label1.setText('Width:')
		grid_layout.addWidget(label1, 0, 0)
		self.line1 = QLineEdit(self)
		self.line1.setValidator(self.validator)
		grid_layout.addWidget(self.line1, 0, 1)

		label2 = QLabel(self)
		label2.setText('Height:')
		grid_layout.addWidget(label2, 1, 0)
		self.line2 = QLineEdit(self)
		self.line2.setValidator(self.validator)
		grid_layout.addWidget(self.line2, 1, 1)
		
		button = QPushButton(self)
		button.setDefault(True)
		button.setText("OK")
		button.clicked.connect(self.accept)
		hbox_layout.addWidget(button)
		
		button = QPushButton(self)
		button.setText("Cancel")
		button.clicked.connect(self.reject)
		hbox_layout.addWidget(button)

		self.set_init_value()


	def set_init_value(self):
		self.line1.setText(Settings().get("InitW"))
		self.line2.setText(Settings().get("InitH"))


	def open(self):
		self.set_init_value()
		super().open()