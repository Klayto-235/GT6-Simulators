from PyQt6.QtCore import QSettings, QCoreApplication
import os

from helpers import Singleton


class Settings(metaclass=Singleton):
	def __init__(self):
		QSettings.setDefaultFormat(QSettings.IniFormat)
		QCoreApplication.setOrganizationName("Gregarious Toolicities")
		QCoreApplication.setApplicationName("GT6 Fission Reactor Simulator")
		self.data = QSettings()

		self.default_settings = {
			"RootDir" : os.path.expanduser("~/Desktop"),
			"AutoExpand" : "true",
			"AutoRun" : "true",
			"PenaltyStop" : "true",
			"ShowHUtLt" : "false",
			"SizeX" : "100",
			"SizeY" : "100",
			"PosX" : "350",
			"PosY" : "100",
			"IsMaximized" : "false", 
			"Rod1" : "U-238",
			"Rod2" : "U-235", 
			"Rod3" : "Co-60",
			"Rod4" : "None",
			"Coolant1" : "CO2",
			"Coolant2" : "He", 
			"Coolant3" : "H2O",
			"Coolant4" : "None", 
			"KeyboardLayout" : "QWERTY", 
			"AutosimTimeout" : "1.0",
			"InitW" : "4",
			"InitH" : "4",
			"Antialiasing" : "true",
			"SmoothZoom" : "true",
			"EnableZoom" : "true",
			"MinZoom" : "0.25", 
			"MaxZoom" : "2.00", 
			"GraphicsEngine" : "Raster",
			"MaterialStacks" : "False"
		}

		self.delayed_change_settings = {}

		self.was_changed = False
		for key in self.default_settings:
			if not self.data.contains(key):
				self.set(key, self.default_settings[key])

	
	def set(self, key, value):
		strval = ""
		if type(value) is str:
			strval = value
		elif type(value) is bool:
			if value:
				strval = "true"
			else:
				strval = "false"
		else:
			strval = str(value)
		if strval == "True":
			strval = "true"
		if strval == "False":
			strval = "false"
		if (self.data.value(key, str) != strval):
			self.data.setValue(key, value)
			self.was_changed = True


	def get(self, key):
		return str(self.data.value(key, self.get_default(key)))


	def get_default(self, key):
		if key not in self.default_settings:
			return None
		return self.default_settings[key]


	def get_bool(self, key):
		return (self.data.value(key, self.get_default(key)).lower() == "true")


	def get_int(self, key):
		return int(self.data.value(key, self.get_default(key)))


	def get_float(self, key):
		return float(self.data.value(key, self.get_default(key)))


	def setList(self, keyvallist):
		for kv in keyvallist:
			self.set(kv[0], kv[1])


	def set_delayed(self, key, val):
		self.delayed_change_settings[key] = str(val)


	def get_bool_delayed(self, key):
		return self.delayed_change_settings.get(key, self.data.value(key, self.get_default(key))).lower() == "true"


	def get_delayed(self, key):
		return str(self.delayed_change_settings.get(key, self.data.value(key, self.get_default(key))))

		
	def save_to_disk(self):
		for k,v in self.delayed_change_settings.items():
			self.set(k, v)
		if self.was_changed:
			self.data.sync()


class Keybinds(metaclass=Singleton):
	def __init__(self):
		self.bind = {
			"Rod 1" : "Q", 
			"Rod 2" : "W",
			"Rod 3" : "E",
			"Rod 4" : "R",
			"Coolant 1" : "1",
			"Coolant 2" : "2", 
			"Coolant 3" : "3",
			"Coolant 4" : "4",
			"Reflector rod" : "A",
			"Absorber rod" : "S",
			"Moderator rod" : "D",
			"Shape tool" : "Z",
			"Reset tool" : "X",
			"Erase tool" : "C",
			"Fill tool" : "F",
			"Floodfill tool" : "V",
			"Run simulation" : "F5",
			"Shrink to fit" : "F4",
			"Increment left" : "Left",
			"Increment right" : "Right",
			"Increment top" : "Up",
			"Increment bottom" : "Down",
			"Decrement left" : "Ctrl+Left",
			"Decrement right" : "Ctrl+Right",
			"Decrement top" : "Ctrl+Up",
			"Decrement bottom" : "Ctrl+Down",
			"New" : "Ctrl+N",
			"Open" : "Ctrl+O",
			"Save" : "Ctrl+S",
			"Save As" : "Ctrl+Alt+S",
			"Quit" : "",
			"Undo" : "Ctrl+Z",
			"Redo" : "Ctrl+Y",
			"Options" : "",
			"Material cost" : "F6",
			"Readme" : "F1",
			"About" : "F10"
		}
		self.actions = {}
		self.keys = {}
		self.update_keys()

		self.set_layout(Settings().get("KeyboardLayout"))


	def set_layout(self, layout):
		if layout == "QWERTY":
			self.update_bind("Rod 1", "Q")
			self.update_bind("Rod 2", "W")
			self.update_bind("Reflector rod", "A")
			self.update_bind("Shape tool", "Z")
		elif layout == "QWERTZ":
			self.update_bind("Rod 1", "Q")
			self.update_bind("Rod 2", "W")
			self.update_bind("Reflector rod", "A")
			self.update_bind("Shape tool", "Y")
		elif layout == "AZERTY":
			self.update_bind("Rod 1", "A")
			self.update_bind("Rod 2", "Z")
			self.update_bind("Reflector rod", "Q")
			self.update_bind("Shape tool", "W")
		else:
			return False
		return True
		

	def get(self, key):
		return self.bind.get(key, None)


	def update_keys(self):
		self.keys = {}
		for k,v in self.bind.items():
			if v != "":
				self.keys[v] = k


	def connect_action(self, name, action):
		self.actions[name] = action


	def unbind(self, key):
		if key not in self.keys:
			return
		action = self.keys[key]
		self.update_bind(action, "")


	def update_bind(self, action, key):
		if action not in self.bind:
			return False
		if key in self.keys:
			self.unbind(key)
		if self.bind[action] == key:
			return True
		if self.bind[action] in self.keys:
			self.keys.pop(self.bind[action])
		self.bind[action] = key
		if key != "":
			self.keys[key] = action
		if action in self.actions:
			self.actions[action].setShortcut(key)
		return True