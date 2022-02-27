from collections import namedtuple
from enum import Enum
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtWidgets import QToolBar, QComboBox, QWidget, QGridLayout, QToolButton, QSizePolicy, QHBoxLayout, QLabel, QCheckBox, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from Assets import Assets
from Settings import Settings, Keybinds


Tool = namedtuple("Tool", ["type", "name", "modifier"])

class ToolType(Enum):
	Default = 0
	Rod = 1
	Coolant = 2
	Shape = 3
	Erase = 4
	Reset = 5


class ToolModifier(Enum):
	Default = 0
	Fill = 1
	FloodFill = 2


class TwinCheckbox(QWidget):
	def __init__(self, label_top, label_bottom, parent=None):
		super().__init__(parent)
		
		self.checkbox_top = QCheckBox(label_top, self)
		self.checkbox_bottom = QCheckBox(label_bottom, self)
		vbox_layout = QVBoxLayout(self)
		vbox_layout.setContentsMargins(0, 0, 0, 0)
		vbox_layout.setSpacing(0)
		vbox_layout.addWidget(self.checkbox_top)
		vbox_layout.addWidget(self.checkbox_bottom)


class TwinButton(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.button_top = QPushButton(self)
		self.button_bot = QPushButton(self)
		vbox_layout = QVBoxLayout(self)
		vbox_layout.setContentsMargins(0, 0, 0, 0)
		vbox_layout.setSpacing(0)
		vbox_layout.addWidget(self.button_top)
		vbox_layout.addWidget(self.button_bot)

		self.button_top.setFixedSize(30, 30)
		self.button_bot.setFixedSize(30, 30)
		self.button_top.setIconSize(QSize(24, 24))
		self.button_bot.setIconSize(QSize(24, 24))


class LabelButtonColumn(QWidget):
	def __init__(self, label_top, label_bottom, parent=None):
		super().__init__(parent)
		
		self.label_top = QLabel(label_top, self)
		self.label_top.setIndent(0)
		self.button_bottom = QPushButton(label_bottom, self)
		vbox_layout = QVBoxLayout(self)
		vbox_layout.setContentsMargins(0, 0, 0, 0)
		vbox_layout.setSpacing(5)
		vbox_layout.addWidget(self.label_top, Qt.AlignmentFlag.AlignHCenter)
		vbox_layout.addWidget(self.button_bottom, Qt.AlignmentFlag.AlignHCenter)
		vbox_layout.addStretch(1)


class ActionWithID(QAction):
	def __init__(self, icon, text, id, bindid, parent=None):
		super().__init__(icon, text, parent)

		self.id = id
		self.bind_id = bindid


class ToolboxTop(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		
		toolbar_left = self.create_toolbar_left()
		toolbar_right = self.create_toolbar_right()
		layout.addWidget(toolbar_left, 0, Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(toolbar_right, 0, Qt.AlignmentFlag.AlignRight)

		self.setMinimumWidth(630)


	def set_size_label(self, width, height):
		self.size_label.setText("".rjust(3 - len(str(width)), ' ') + "   Grid size: " + str(width) + " x " + str(height) + "   " + "".rjust(3 - len(str(height)), ' '))


	def create_toolbar_right(self):
		toolbar_right = QToolBar(self)
		toolbar_right.setMovable(False)
		toolbar_right.setOrientation(Qt.Orientation.Horizontal)
		toolbar_right.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
		toolbar_right.setContentsMargins(0, 0, 0, 0)
		toolbar_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		toolbar_right.setIconSize(QSize(48, 48))
		toolbar_right.setStyleSheet("QToolBar::separator { width: 20px}")
		
		# Autoexpand and Show HU/t or L/t checkboxes
		self.twin_checkbox_grid = TwinCheckbox("Autoexpand", "Show HU/t", self)
		self.twin_checkbox_grid.checkbox_top.setToolTip("Automatically grow reactor grid if anything is placed at the edge.")
		self.twin_checkbox_grid.checkbox_bottom.setToolTip("Toggle between L/t and HU/t display on reactor blocks.")
		self.signal_autoexpand_toggled = self.twin_checkbox_grid.checkbox_top.toggled
		self.signal_show_HUt_Lt_toggled = self.twin_checkbox_grid.checkbox_bottom.toggled
		toolbar_right.addWidget(self.twin_checkbox_grid)
		
		toolbar_right.addSeparator()

		# Autorun and durability penalty stop checkboxes
		self.twin_checkbox_simulation = TwinCheckbox("Autorun", "Penalty Stop", self)
		self.twin_checkbox_simulation.checkbox_top.setToolTip("Automatically rerun the simulation after every change.")
		self.twin_checkbox_simulation.checkbox_bottom.setToolTip("Stop the simulation when a rod incurs durability penalty.")
		self.signal_autorun_toggled = self.twin_checkbox_simulation.checkbox_top.toggled
		self.signal_penalty_stop_toggled = self.twin_checkbox_simulation.checkbox_bottom.toggled
		toolbar_right.addWidget(self.twin_checkbox_simulation)

		# Run simulation
		action = QAction(QIcon(Assets().utility_pixmap["Play"]), "Simulate", self)
		action.setShortcut(Keybinds().get("Run simulation"))
		Keybinds().connect_action("Run simulation", action)
		action.setToolTip(action.toolTip() + " (" + action.shortcut().toString() + ")")
		self.signal_simulate = action.triggered
		toolbar_right.addAction(action)

		return toolbar_right


	def set_checkbox_autorun(self, state):
		self.twin_checkbox_simulation.checkbox_top.setChecked(state)


	def set_checkbox_penalty_stop(self, state):
		self.twin_checkbox_simulation.checkbox_bottom.setChecked(state)


	def set_checkbox_autoexpand(self, state):
		self.twin_checkbox_grid.checkbox_top.setChecked(state)


	def set_checkbox_show_HUt_Lt(self, state):
		self.twin_checkbox_grid.checkbox_bottom.setChecked(state)


	def create_toolbar_left(self):
		toolbar_left = QToolBar(self)
		toolbar_left.setMovable(False)
		toolbar_left.setOrientation(Qt.Orientation.Horizontal)
		toolbar_left.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
		toolbar_left.setContentsMargins(0, 0, 0, 0)
		toolbar_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		toolbar_left.setIconSize(QSize(36, 36))
		toolbar_left.setStyleSheet("QToolBar::separator { width: 20px}")

		# Spacer label
		toolbar_left.addWidget(QLabel("  ", self))

		# Grid size label + shrink to fit button
		temp = LabelButtonColumn("", "Shrink to fit", self)
		self.size_label = temp.label_top
		self.shrink_to_fit_button = temp.button_bottom
		self.shrink_to_fit_button.setToolTip("Clip all empty rows and columns (F4)")
		self.shrink_to_fit_button.setShortcut(Keybinds().get("Shrink to fit"))
		Keybinds().connect_action("Shrink to fit", self.shrink_to_fit_button)
		toolbar_left.addWidget(temp)

		self.signal_shrink_to_fit = temp.button_bottom.pressed

		toolbar_left.addSeparator()

		# Resize buttons
		resize_buttons = []
		temp = [ "left", "right", "top", "bottom" ]
		temptt = [ "Column Left", "Column Right", "Row Top", "Row Bottom" ]
		for i in range(4):
			resize_buttons.append(TwinButton(self))
			top = Assets().rowcol_util[i]
			bot = Assets().rowcol_util[i + 4]
			resize_buttons[i].button_top.setIcon(QIcon(Assets().smaller_utility_pixmap[top]))
			resize_buttons[i].button_bot.setIcon(QIcon(Assets().smaller_utility_pixmap[bot]))
			resize_buttons[i].button_top.setShortcut(Keybinds().get("Increment " + temp[i]))
			resize_buttons[i].button_bot.setShortcut(Keybinds().get("Decrement " + temp[i]))
			Keybinds().connect_action("Increment " + temp[i], resize_buttons[i].button_top)
			Keybinds().connect_action("Decrement " + temp[i], resize_buttons[i].button_bot)
			resize_buttons[i].button_top.setToolTip("Add " + temptt[i] + " (" + resize_buttons[i].button_top.shortcut().toString() + ")")
			resize_buttons[i].button_bot.setToolTip("Remove " + temptt[i] + " (" + resize_buttons[i].button_bot.shortcut().toString() + ")")
			toolbar_left.addWidget(resize_buttons[i])

		self.signal_increment_left = resize_buttons[0].button_top.pressed
		self.signal_decrement_left = resize_buttons[0].button_bot.pressed
		self.signal_increment_right = resize_buttons[1].button_top.pressed
		self.signal_decrement_right = resize_buttons[1].button_bot.pressed
		self.signal_increment_top = resize_buttons[2].button_top.pressed
		self.signal_decrement_top = resize_buttons[2].button_bot.pressed
		self.signal_increment_bottom = resize_buttons[3].button_top.pressed
		self.signal_decrement_bottom = resize_buttons[3].button_bot.pressed

		return toolbar_left


class ToolboxLeft(QWidget):
	signal_tool_type_selected = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

		layout = QGridLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setHorizontalSpacing(0)
		layout.setVerticalSpacing(2)
		
		self.tool_type_action_group = QActionGroup(self)
		self.tool_type_action_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
		self.tool_modifier_action_group = QActionGroup(self)
		self.tool_modifier_action_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
		
		# Coolant selection ComboBox
		self.coolant_combo = QComboBox(self)
		tempcount = 0
		for name,record in Assets().coolant.items():
			self.coolant_combo.addItem(QIcon(record.pixmap), name)
			self.coolant_combo.setItemData(tempcount, Assets().coolant_tooltips[name], Qt.ItemDataRole.ToolTipRole)
			tempcount += 1
		self.coolant_combo.setDisabled(True)
		self.coolant_combo.currentTextChanged.connect(self.on_coolant_change)
		self.coolant_combo.setIconSize(QSize(48, 48))
		self.coolant_combo.hide()

		# Fuel rod selection ComboBox
		self.fuel_rod_combo = QComboBox(self)
		tempcount = 0
		for name,record in Assets().rod.items():
			if name not in ["Ref", "Abs", "Mod"]:
				self.fuel_rod_combo.addItem(QIcon(record.pixmap), name)
				self.fuel_rod_combo.setItemData(tempcount, Assets().rod_tooltips[name], Qt.ItemDataRole.ToolTipRole)
				tempcount += 1
		self.fuel_rod_combo.setDisabled(True)
		self.fuel_rod_combo.currentTextChanged.connect(self.on_fuel_rod_change)
		self.fuel_rod_combo.setIconSize(QSize(48, 48))
		
		layout.addWidget(self.fuel_rod_combo, 0, 0, 1, 2)
		layout.addWidget(self.coolant_combo, 0, 0, 1, 2)
		layout.addWidget(self.create_toolbar_left(), 1, 0)
		layout.addWidget(self.create_toolbar_right(), 1, 1)

		self.setMinimumHeight(700)

		
	def create_toolbar_right(self):
		toolbar_right = QToolBar(self)
		toolbar_right.setMovable(False)
		toolbar_right.setOrientation(Qt.Orientation.Vertical)
		toolbar_right.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
		toolbar_right.setContentsMargins(0, 0, 0, 0)
		toolbar_right.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
		toolbar_right.setIconSize(QSize(48, 48))
		
		toolbar_right.addSeparator()

		# Coolant Actions
		for i in range(4):
			s = Settings().get("Coolant" + str(i + 1))
			coolant = Assets().coolant[s]
			action = ActionWithID(QIcon(coolant.pixmap), s, "Coolant" + str(i + 1), "CoolantBind" + str(i + 1), self)
			action.triggered.connect(lambda checked: self.on_tool_click(checked, ToolType.Coolant))
			action.setActionGroup(self.tool_type_action_group)
			action.setCheckable(True)
			action.setData((ToolType.Coolant, s))
			action.setToolTip(Assets().coolant_tooltips[s])
			action.setShortcut(Keybinds().get("Coolant " + str(i + 1)))
			Keybinds().connect_action("Coolant " + str(i + 1), action)
			toolbar_right.addAction(action)
		toolbar_right.addSeparator()
			
		# Block shape Action
		action = ActionWithID(QIcon(Assets().utility_pixmap["Shape"]), "Shape", None, "ShapeBind", self)
		action.triggered.connect(self.on_tool_click)
		action.setActionGroup(self.tool_type_action_group)
		action.setCheckable(True)
		action.setData((ToolType.Shape, "Shape"))
		action.setShortcut(Keybinds().get("Shape tool"))
		Keybinds().connect_action("Shape tool", action)
		action.setToolTip("Switch between 1x1 and 2x2 reactor blocks (" + action.shortcut().toString() + ")")
		toolbar_right.addAction(action)

		# Block reset Action
		action = ActionWithID(QIcon(Assets().utility_pixmap["Reset"]), "Reset", None, "ResetBind", self)
		action.triggered.connect(self.on_tool_click)
		action.setActionGroup(self.tool_type_action_group)
		action.setCheckable(True)
		action.setData((ToolType.Reset, "Reset"))
		action.setShortcut(Keybinds().get("Reset tool"))
		Keybinds().connect_action("Reset tool", action)
		action.setToolTip("Reset block (" + action.shortcut().toString() + ")")
		toolbar_right.addAction(action)

		# Erase Action
		action = ActionWithID(QIcon(Assets().utility_pixmap["Erase"]), "Erase", None, "EraseBind", self)
		action.triggered.connect(self.on_tool_click)
		action.setActionGroup(self.tool_type_action_group)
		action.setCheckable(True)
		action.setData((ToolType.Erase, "Erase"))
		action.setShortcut(Keybinds().get("Erase tool"))
		Keybinds().connect_action("Erase tool", action)
		action.setToolTip("Clear block contents (" + action.shortcut().toString() + ")")
		toolbar_right.addAction(action)
		toolbar_right.addSeparator()

		# Flood fill Action
		action = ActionWithID(QIcon(Assets().utility_pixmap["Floodfill"]), "Floodfill", None, "FloodfillBind", self)
		action.setActionGroup(self.tool_modifier_action_group)
		action.setCheckable(True)
		action.setData((ToolModifier.FloodFill,))
		action.setShortcut(Keybinds().get("Floodfill tool"))
		Keybinds().connect_action("Floodfill tool", action)
		action.setToolTip("Flood fill (" + action.shortcut().toString() + ")")
		toolbar_right.addAction(action)

		return toolbar_right


	def create_toolbar_left(self):
		toolbar_left = QToolBar(self)
		toolbar_left.setMovable(False)
		toolbar_left.setOrientation(Qt.Orientation.Vertical)
		toolbar_left.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
		toolbar_left.setContentsMargins(0, 0, 0, 0)
		toolbar_left.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
		toolbar_left.setIconSize(QSize(48, 48))
		
		toolbar_left.addSeparator()

		# Fuel rod Actions
		for i in range(4):
			s = Settings().get("Rod" + str(i + 1))
			rod = Assets().rod[s]
			action = ActionWithID(QIcon(rod.pixmap), s, "Rod" + str(i + 1), "RodBind" + str(i + 1), self)
			action.triggered.connect(lambda checked: self.on_tool_click(checked, ToolType.Rod))
			action.setActionGroup(self.tool_type_action_group)
			action.setCheckable(True)
			action.setData((ToolType.Rod, s))
			action.setToolTip(Assets().rod_tooltips[s])
			action.setShortcut(Keybinds().get("Rod " + str(i + 1)))
			Keybinds().connect_action("Rod " + str(i + 1), action)
			toolbar_left.addAction(action)
		toolbar_left.addSeparator()
		
		# Utility rod Actions
		for s in ["Reflector", "Absorber", "Moderator"]:
			rod = Assets().rod[s[0:3]]
			action = ActionWithID(QIcon(rod.pixmap), s, None, s[0:3] + "Bind", self)
			action.triggered.connect(self.on_tool_click)
			action.setActionGroup(self.tool_type_action_group)
			action.setCheckable(True)
			action.setData((ToolType.Rod, s[0:3]))
			action.setToolTip(Assets().rod_tooltips[s[0:3]])
			action.setShortcut(Keybinds().get(s + " rod"))
			Keybinds().connect_action(s + " rod", action)
			toolbar_left.addAction(action)
		toolbar_left.addSeparator()
		
		# Fill Action
		action = ActionWithID(QIcon(Assets().utility_pixmap["Fill"]), "Fill", None, "FillBind", self)
		action.setActionGroup(self.tool_modifier_action_group)
		action.setCheckable(True)
		action.setData((ToolModifier.Fill,))
		
		action.setShortcut(Keybinds().get("Fill tool"))
		Keybinds().connect_action("Fill tool", action)
		action.setToolTip("Fill (" + action.shortcut().toString() + ")")
		toolbar_left.addAction(action)

		return toolbar_left


	def on_coolant_change(self, name):
		if self.coolant_combo.isEnabled():
			action = self.tool_type_action_group.checkedAction()
			action.setIcon(QIcon(Assets().coolant[name].pixmap))
			action.setIconText(name)
			action.setData((ToolType.Coolant, name))
			action.setToolTip(Assets().coolant_tooltips[name])
			Settings().set(action.id, name)


	def on_fuel_rod_change(self, name):
		if self.fuel_rod_combo.isEnabled():
			action = self.tool_type_action_group.checkedAction()
			action.setIcon(QIcon(Assets().rod[name].pixmap))
			action.setIconText(name)
			action.setData((ToolType.Rod, name))
			action.setToolTip(Assets().rod_tooltips[name])
			Settings().set(action.id, name)


	def on_tool_click(self, checked, type=None):
		# type is not None only for the types used in the body of the function (additionally excluding utility rods)
		if checked and type == ToolType.Rod:
			self.coolant_combo.setEnabled(False)
			self.coolant_combo.setCurrentText("None")
			self.coolant_combo.hide()
			self.fuel_rod_combo.show()
			self.fuel_rod_combo.setCurrentText(self.tool_type_action_group.checkedAction().iconText())
			self.fuel_rod_combo.setEnabled(True)
		elif checked and type == ToolType.Coolant:
			self.fuel_rod_combo.setEnabled(False)
			self.fuel_rod_combo.setCurrentText("None")
			self.fuel_rod_combo.hide()
			self.coolant_combo.show()
			self.coolant_combo.setCurrentText(self.tool_type_action_group.checkedAction().iconText())
			self.coolant_combo.setEnabled(True)
		else:
			self.fuel_rod_combo.setEnabled(False)
			self.fuel_rod_combo.setCurrentText("None")
			self.coolant_combo.setEnabled(False)
			self.coolant_combo.setCurrentText("None")

		if checked:
			self.signal_tool_type_selected.emit()


	def get_current_tool(self):
		type_action = self.tool_type_action_group.checkedAction()
		action_data = (ToolType.Default, "") if type_action is None else type_action.data()
		modifier_action = self.tool_modifier_action_group.checkedAction()
		modifier_data = (ToolModifier.Default,) if modifier_action is None else modifier_action.data()
		return Tool(*action_data, *modifier_data)
