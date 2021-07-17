from PyQt6.QtWidgets import QWidget, QDialog, QTabWidget, QLabel, QCheckBox, QVBoxLayout, QDialogButtonBox, QScrollArea, QLineEdit, QGridLayout, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt, QObject
from math import ceil


from utility import recursive_string_constructor, recursive_material_cost, to_whole_materials, recursive_dict_sum
from Assets import Assets


class MaterialTab(QWidget):
	def __init__(self, data, name, parent=None):
		super().__init__(parent)

		self.tabname = name

		self.layout = QVBoxLayout(self)

		self.construct_tree(data)

		self.setLayout(self.layout)


	def clear_tree(self):
		self.layout.removeWidget(self.inside)


	def construct_tree(self, data):
		self.inside = QTreeWidget(self)
		self.inside.setColumnCount(1)
		self.inside.setHeaderHidden(True)
		tempstack = []

		for i in range(len(data)):
			tempitem = QTreeWidgetItem(None, [data[i][1]])
			tempitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
			tempitem.setCheckState(0, Qt.Unchecked)
			if data[i][0] == 0:
				self.inside.addTopLevelItem(tempitem)
			else:
				tempstack[data[i][0] - 1].addChild(tempitem)
			if len(tempstack) > data[i][0]:
				tempstack[data[i][0]] = tempitem
			else:
				tempstack.append(tempitem)

		iterator = QTreeWidgetItemIterator(self.inside)
		while iterator.value():
			item = iterator.value()
			self.inside.itemClicked.connect(self.checked_change)
			iterator += 1

		if self.tabname == "Reactor recipes":
			for i in range(self.inside.topLevelItemCount()):
				self.inside.topLevelItem(i).setExpanded(True)

		self.layout.insertWidget(0, self.inside)


	def checked_change(self, item, col):
		temp = item.parent()
		while temp != None:
			self.check_own_state(temp)
			temp = temp.parent()
		stack = []
		for i in range(item.childCount()):
			stack.append(item.child(i))
		while len(stack) > 0:
			iteem = stack.pop()
			iteem.setCheckState(0, item.checkState(0))
			for i in range(iteem.childCount()):
				stack.append(iteem.child(i))


	def check_own_state(self, item):
		has_checked = False
		has_unchecked = False
		has_semichecked = False
		for i in range(item.childCount()):
			if item.child(i).checkState(0) == Qt.Unchecked:
				has_unchecked = True
			elif item.child(i).checkState(0) == Qt.Checked:
				has_checked = True
			else:
				has_semichecked = True
		if has_semichecked:
			item.setCheckState(0, Qt.PartiallyChecked)
		else:
			if has_checked and has_unchecked:
				item.setCheckState(0, Qt.PartiallyChecked)
			elif has_checked:
				item.setCheckState(0, Qt.Checked)
			else:
				item.setCheckState(0, Qt.Unchecked)


class InputLine(QLineEdit):
	def __init__(self, name, data, parent=None):
		super().__init__(parent)

		self.setFixedWidth(100)
		self.key = name
		self.setValidator(QIntValidator(0, 999999999, self))
		self.setText(str(data))


class InputTab(QScrollArea):
	def __init__(self, indata, parent=None):
		super().__init__(parent)

		self.dialog = parent
		self.data = indata

		self.inside = QWidget(self)

		self.layout = QGridLayout(self.inside)
		self.layout.setColumnStretch(0, 0)
		self.layout.setColumnStretch(1, 0)
		self.layout.setColumnStretch(2, 1)

		self.inputs = []

		self.layout.addWidget(QLabel("<b>RODS" + Assets().delim + "<\b>", self.inside), 0, 0)
		count = 1
		for key in Assets().rod:
			if key != "None":
				self.layout.addWidget(QLabel(key + Assets().delim, self.inside), count, 0)
				temp = InputLine(key, self.data.get(key, 0), self.inside)
				self.layout.addWidget(temp, count, 1)
				self.inputs.append([key, temp])
				count += 1
		self.layout.addWidget(QLabel(" ", self.inside), count, 0)
		self.layout.addWidget(QLabel("<b>BLOCKS" + Assets().delim + "<\b>", self.inside), count + 1, 0)
		count += 2
		for key in [ "Nuclear Reactor Core (1x1)", "Nuclear Reactor Core (2x2)" ]:
			self.layout.addWidget(QLabel(key + Assets().delim, self.inside), count, 0)
			temp = InputLine(key, self.data.get(key, 0), self.inside)
			self.layout.addWidget(temp, count, 1)
			self.inputs.append([key, temp])
			count += 1
		self.inside.setLayout(self.layout)

		self.setWidget(self.inside)


class MaterialDialog(QDialog):
	def __init__(self, material_objects, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Material costs")

		self.data = material_objects

		self.calculate()

		tab_widget = QTabWidget(self)
		tab_widget.setMinimumSize(630, 670)
		button_box_widget = QDialogButtonBox(QDialogButtonBox.Close)
		self.rod_widget = MaterialTab(self.rod_data, "Fuel recipes", tab_widget)
		self.raw_rod_widget = MaterialTab(self.raw_rod_data, "Raw fuel materials", tab_widget)
		self.reactor_widget = MaterialTab(self.reactor_data, "Reactor recipes", tab_widget)
		self.raw_reactor_widget = MaterialTab(self.raw_reactor_data, "Raw reactor materials", tab_widget)

		self.input_widget = InputTab(self.data, tab_widget)
		tab_widget.addTab(self.input_widget, "Required parts")
		for wgt in [self.rod_widget, self.raw_rod_widget, self.reactor_widget, self.raw_reactor_widget]:
			tab_widget.addTab(wgt, wgt.tabname)

		layout = QVBoxLayout(self)
		layout.addWidget(tab_widget)
		layout.addWidget(button_box_widget)
		self.setLayout(layout)

		button_box_widget.rejected.connect(self.reject)

		for line in self.input_widget.inputs:
			x = line[0]
			line[1].textEdited.connect(lambda input, x=x: self.input_change(input, x))


	def input_change(self, inputval, key):
		self.data[key] = int(inputval)
		self.calculate()
		self.refresh_material_tabs()


	def refresh_material_tabs(self):
		self.rod_widget.clear_tree()
		self.raw_rod_widget.clear_tree()
		self.reactor_widget.clear_tree()
		self.raw_reactor_widget.clear_tree()

		self.rod_widget.construct_tree(self.rod_data)
		self.raw_rod_widget.construct_tree(self.raw_rod_data)
		self.reactor_widget.construct_tree(self.reactor_data)
		self.raw_reactor_widget.construct_tree(self.raw_reactor_data)


	def calculate(self):
		self.rod_materials = {}
		self.raw_rod_materials = {}
		self.reactor_materials = {}
		self.raw_reactor_materials = {}

		self.rod_data = []
		self.raw_rod_data = []
		self.reactor_data = []
		self.raw_reactor_data = []

		for key,val in self.data.items():
			if key == "Nuclear Reactor Core (2x2)" or key == "Nuclear Reactor Core (1x1)":
				self.reactor_materials[key] = [val, {}]
				recursive_material_cost(key, self.reactor_materials[key], self.raw_reactor_materials)
			elif key == "Ref" or key == "Abs" or key == "Mod":
				tkey = Assets().rod[key].full_name
				self.reactor_materials[tkey] = [val, {}]
				recursive_material_cost(key, self.reactor_materials[tkey], self.raw_reactor_materials)
			elif key == "Th coolant":
				tkey = "Th coolant (L)"
				self.rod_materials[tkey] = [val, {}]
				recursive_material_cost(tkey, self.rod_materials[tkey], self.raw_rod_materials)
			else:
				tkey = Assets().rod[key].full_name
				self.rod_materials[tkey] = [val, {}]
				recursive_material_cost(key, self.rod_materials[tkey], self.raw_rod_materials)
		for key,val in self.raw_rod_materials.items():
			self.raw_rod_materials[key][0] = to_whole_materials(val[0])
		for key,val in self.raw_reactor_materials.items():
			self.raw_reactor_materials[key][0] = to_whole_materials(val[0])

		#Deal with excess decimals for thorium coolant litres
		if "Th coolant (L)" in self.rod_materials:
			temp = self.rod_materials["Th coolant (L)"][0]
			self.rod_materials["Th coolant (L)"][0] = ceil(temp * 1000) / 1000
		if "Thorium (loss)" in self.raw_rod_materials:
			temp = self.raw_rod_materials["Thorium (loss)"][1]["Th coolant (L)"][0]
			self.raw_rod_materials["Thorium (loss)"][1]["Th coolant (L)"][0] = ceil(temp * 1000) / 1000

		#Merge both nuclear reactor block costs since they are so similar, makes life easier
		if "Nuclear Reactor Core (1x1)" in self.reactor_materials and "Nuclear Reactor Core (2x2)" in self.reactor_materials:
			tempstr = "Nuclear Reactor Core (1x1)" + Assets().delim + str(self.reactor_materials["Nuclear Reactor Core (1x1)"][0]) + "\n" + "Nuclear Reactor Core (2x2)"
			self.reactor_materials[tempstr] = [self.reactor_materials["Nuclear Reactor Core (2x2)"][0], {}]
			recursive_dict_sum(self.reactor_materials[tempstr], self.reactor_materials["Nuclear Reactor Core (1x1)"])
			recursive_dict_sum(self.reactor_materials[tempstr], self.reactor_materials["Nuclear Reactor Core (2x2)"])
			self.reactor_materials.pop("Nuclear Reactor Core (1x1)")
			self.reactor_materials.pop("Nuclear Reactor Core (2x2)")
		
		recursive_string_constructor(0, self.rod_data, "", self.rod_materials)
		recursive_string_constructor(0, self.raw_rod_data, "", self.raw_rod_materials)
		recursive_string_constructor(0, self.reactor_data, "", self.reactor_materials)
		recursive_string_constructor(0, self.raw_reactor_data, "", self.raw_reactor_materials)