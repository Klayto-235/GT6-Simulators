from PyQt6.QtWidgets import QMessageBox, QWidget, QDialog, QTabWidget, QLabel, QScrollArea, QLineEdit, QFrame, QGridLayout, QDialogButtonBox, QVBoxLayout, QComboBox, QSizePolicy, QSpacerItem, QHBoxLayout, QCheckBox
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator

from Settings import Settings, Keybinds


class ShortcutTab(QScrollArea):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWidgetResizable(True)

		self.inside = QWidget(self)

		self.layout = QGridLayout(self.inside)

		self.layout.addWidget(QLabel("<b>Action<\b>", self.inside), 0, 0)
		self.layout.addWidget(QLabel("<b>Shortcut<\b>", self.inside), 0, 1)
		line1 = QFrame(self.inside)
		line2 = QFrame(self.inside)
		line1.setGeometry(0, 0, 150, 5)
		line2.setGeometry(0, 0, 100, 5)
		line1.setFrameShape(QFrame.HLine)
		line2.setFrameShape(QFrame.HLine)
		line1.setFrameShadow(QFrame.Sunken)
		line2.setFrameShadow(QFrame.Sunken)
		self.layout.addWidget(line1, 1, 0)
		self.layout.addWidget(line2, 1, 1)
		self.layout.setColumnMinimumWidth(0, 150)
		self.layout.setColumnMinimumWidth(1, 100)

		count = 2
		for k,v in Keybinds().bind.items():
			self.layout.addWidget(QLabel(k, self.inside), count, 0)
			self.layout.addWidget(QLabel(v, self.inside), count, 1)
			count += 1
		
		vspacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		hspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.layout.addItem(vspacer, count, 0, 2, 1)
		self.layout.addItem(hspacer, 0, 2, 1, count)

		self.inside.setLayout(self.layout)

		self.setWidget(self.inside)


	def restore_defaults(self):
		return


	def apply_options(self):
		count = 2
		for k,v in Keybinds().bind.items():
			self.layout.itemAtPosition(count, 0).widget().setText(k)
			self.layout.itemAtPosition(count, 1).widget().setText(v)
			count += 1


class GeneralOptionsTab(QScrollArea):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWidgetResizable(True)

		self.inside = QWidget(self)
		
		self.outsideLayout = QGridLayout(self.inside)
		self.layout = QGridLayout()
		self.outsideLayout.addLayout(self.layout, 0, 0)
		self.outsideLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 1, 0)
		self.outsideLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 1)

		templabel = QLabel("Keyboard layout: ", self.inside)
		templabel.setToolTip("Choose preferred keyboard layout.\nThis will modify the keyboard shortcuts accordingly.")
		self.layout.addWidget(templabel, 0, 0)
		self.klayout = QComboBox(self.inside)
		self.klayout.addItem("QWERTY")
		self.klayout.addItem("QWERTZ")
		self.klayout.addItem("AZERTY")
		self.klayout.setToolTip("Choose preferred keyboard layout.\nThis will modify the keyboard shortcuts accordingly.")
		self.klayoutMap = {"QWERTY" : 0, "QWERTZ" : 1, "AZERTY" : 2}
		self.klayout.setCurrentIndex(self.klayoutMap[Settings().get("KeyboardLayout")])
		self.layout.addWidget(self.klayout, 0, 1)

		validator = QDoubleValidator(0.1, 60.0, 6)
		templabel = QLabel("Autorun simulation time limit (s): ", self.inside)
		templabel.setToolTip("Time limit (in seconds) for simulations that run automatically.\nAccepts values between 0.1 and 60.0 with up to microsecond precision.")
		self.layout.addWidget(templabel, 1, 0)
		self.artimelimit = QLineEdit(Settings().get("AutosimTimeout"), self.inside)
		self.artimelimit.setValidator(validator)
		self.artimelimit.setToolTip("Time limit (in seconds) for simulations that run automatically.\nAccepts values between 0.1 and 60.0 with up to microsecond precision.")
		self.layout.addWidget(self.artimelimit, 1, 1)

		ivalidator = QIntValidator(1, 1000)
		templabel = QLabel("Default new grid width: ", self.inside)
		templabel.setToolTip("Default value for new grid width.")
		self.layout.addWidget(templabel, 2, 0)
		self.initw = QLineEdit(Settings().get("InitW"), self.inside)
		self.initw.setValidator(ivalidator)
		self.initw.setToolTip("Default value for new grid width.")
		self.layout.addWidget(self.initw, 2, 1)

		templabel = QLabel("Default new grid height: ", self.inside)
		templabel.setToolTip("Default value for new grid height.")
		self.layout.addWidget(templabel, 3, 0)
		self.inith = QLineEdit(Settings().get("InitH"), self.inside)
		self.inith.setValidator(ivalidator)
		self.inith.setToolTip("Default value for new grid height.")
		self.layout.addWidget(self.inith, 3, 1)

		templabel = QLabel("Enable zoom: ", self.inside)
		templabel.setToolTip("Enables zooming.")
		self.layout.addWidget(templabel, 4, 0)
		self.zoom = QCheckBox(self)
		if Settings().get_bool("EnableZoom"):
			self.zoom.setCheckState(Qt.Checked)
		else:
			self.zoom.setCheckState(Qt.Unchecked)
		self.zoom.setToolTip("Enables zooming.")
		self.layout.addWidget(self.zoom, 4, 1)

		templabel = QLabel("Enable smooth zoom: ", self.inside)
		templabel.setToolTip("Enables smooth zoom, due to Qt reasons this doesn't work very well with larger grids.")
		self.layout.addWidget(templabel, 5, 0)
		self.szoom = QCheckBox(self)
		if Settings().get_bool("SmoothZoom"):
			self.szoom.setCheckState(Qt.Checked)
		else:
			self.szoom.setCheckState(Qt.Unchecked)
		self.szoom.setToolTip("Enables smooth zoom, due to Qt reasons this doesn't work very well with larger grids.")
		self.layout.addWidget(self.szoom, 5, 1)

		templabel = QLabel("Enable antialiasing: ", self.inside)
		templabel.setToolTip("Enables antialiasing, disabling this may improve performance (which because of Qt is abismal anyway).\nREQUIRES RESTART TO TAKE EFFECT.")
		self.layout.addWidget(templabel, 6, 0)
		self.aa = QCheckBox(self)
		if Settings().get_bool_delayed("Antialiasing"):
			self.aa.setCheckState(Qt.Checked)
		else:
			self.aa.setCheckState(Qt.Unchecked)
		self.aa.setToolTip("Enables antialiasing, disabling this may improve performance (which because of Qt is abismal anyway).\nREQUIRES RESTART TO TAKE EFFECT.")
		self.layout.addWidget(self.aa, 6, 1)

		templabel = QLabel("Minimal zoom factor: ", self.inside)
		templabel.setToolTip("Sets the minimal allowed zoom factor.")
		self.layout.addWidget(templabel, 7, 0)
		self.minz = QLineEdit(Settings().get("MinZoom"), self.inside)
		self.minz.setValidator(validator)
		self.minz.setToolTip("Sets the minimal allowed zoom factor.")
		self.layout.addWidget(self.minz, 7, 1)

		templabel = QLabel("Maximal zoom factor: ", self.inside)
		templabel.setToolTip("Sets the maximal allowed zoom factor.")
		self.layout.addWidget(templabel, 8, 0)
		self.maxz = QLineEdit(Settings().get("MaxZoom"), self.inside)
		self.maxz.setValidator(validator)
		self.maxz.setToolTip("Sets the maximal allowed zoom factor.")
		self.layout.addWidget(self.maxz, 8, 1)

		templabel = QLabel("Graphics engine: ", self.inside)
		templabel.setToolTip("Choose preferred graphics engine, the default is a CPU raster engine.\nREQUIRES RESTART TO TAKE EFFECT.")
		self.layout.addWidget(templabel, 9, 0)
		self.gen = QComboBox(self.inside)
		self.gen.addItem("Raster")
		#self.gen.addItem("OpenGL") #TODO: Once OpenGL rendering is implemented again, run this
		self.gen.setToolTip("Choose preferred graphics engine, the default is a CPU raster engine.\nREQUIRES RESTART TO TAKE EFFECT.")
		self.genMap = {"Raster" : 0, "OpenGL" : 1}
		self.gen.setCurrentIndex(self.genMap[Settings().get("GraphicsEngine")])
		self.layout.addWidget(self.gen, 9, 1)

		self.layout.setHorizontalSpacing(10)

		self.setWidget(self.inside)


	def apply_options(self):
		Settings().set("KeyboardLayout", self.klayout.currentText())
		Keybinds().set_layout(Settings().get("KeyboardLayout"))
		if float(self.artimelimit.text()) > 0:
			Settings().set("AutosimTimeout", self.artimelimit.text())
		if int(self.initw.text()) > 0:
			Settings().set("InitW", self.initw.text())
		if int(self.inith.text()) > 0:
			Settings().set("InitH", self.inith.text())
		if self.zoom.checkState() == Qt.Checked:
			Settings().set("EnableZoom", "true")
		else:
			Settings().set("EnableZoom", "false")
		if self.szoom.checkState() == Qt.Checked:
			Settings().set("SmoothZoom", "true")
		else:
			Settings().set("SmoothZoom", "false")
		tempAA = Settings().get_bool_delayed("Antialiasing")
		if self.aa.checkState() == Qt.Checked:
			Settings().set_delayed("Antialiasing", "true")
		else:
			Settings().set_delayed("Antialiasing", "false")
		minz = float(self.minz.text())
		if minz <= 0:
			minz = Settings().get_float("MinZoom")
		maxz = float(self.maxz.text())
		if maxz <= 0:
			maxz = Settings().get_float("MaxZoom")
		if maxz >= minz:
			Settings().set("MinZoom", minz)
			Settings().set("MaxZoom", maxz)
		tempGE = Settings().get_delayed("GraphicsEngine")
		Settings().set_delayed("GraphicsEngine", self.gen.currentText())

		test = False
		test = test or (Settings().get_bool_delayed("Antialiasing") != Settings().get_bool("Antialiasing") and tempAA != Settings().get_bool_delayed("Antialiasing"))
		test = test or (Settings().get_delayed("GraphicsEngine") != Settings().get("GraphicsEngine") and tempGE != Settings().get_delayed("GraphicsEngine"))
		if test:
			qmbox = QMessageBox()
			qmbox.setIcon(QMessageBox.Warning)
			qmbox.setText("Some changes require a restart to take effect.")
			qmbox.setWindowTitle("Warning")
			qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
			x = qmbox.exec()


	def restore_defaults(self):
		self.klayout.setCurrentIndex(self.klayoutMap[Settings().get_default("KeyboardLayout")])


class OptionsDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Options")

		self.tab_widget = QTabWidget(self)
		self.setFixedSize(600, 450)
		self.button_box_widget = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Save | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults )

		self.tabs = []

		self.general_tab = GeneralOptionsTab(self.tab_widget)
		self.tabs.append(self.general_tab)
		self.tab_widget.addTab(self.general_tab, "General")
		self.shortcut_tab = ShortcutTab(self.tab_widget)
		self.tabs.append(self.shortcut_tab)
		self.tab_widget.addTab(self.shortcut_tab, "Keybinds")

		self.tab_widget.setTabToolTip(0, "General options (feel free to edit these)")
		self.tab_widget.setTabToolTip(1, "List of keyboard shortcuts (you can't edit these directly... because reasons)")

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.tab_widget)
		self.layout.addWidget(self.button_box_widget)
		self.setLayout(self.layout)

		self.button_box_widget.clicked.connect(self.on_click)


	def restore_defaults(self):
		for tab in self.tabs:
			tab.restore_defaults()


	def apply_options(self):
		for tab in self.tabs:
			tab.apply_options()


	def on_click(self, button):
		if self.button_box_widget.buttonRole(button) == QDialogButtonBox.AcceptRole:
			self.apply_options()
			self.accept()
		elif self.button_box_widget.buttonRole(button) == QDialogButtonBox.RejectRole:
			self.reject()
		elif self.button_box_widget.buttonRole(button) == QDialogButtonBox.ApplyRole:
			self.apply_options()
		elif self.button_box_widget.buttonRole(button) == QDialogButtonBox.ResetRole:
			self.restore_defaults()