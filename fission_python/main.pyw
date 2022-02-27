import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCloseEvent

from MainWidget import DuctTape
from MenuBar import MenuBar
from Settings import Settings


class RealMainWindow(QMainWindow):
	signal_close = pyqtSignal(QCloseEvent)

	def __init__(self):
		super().__init__()

		# Menu bar
		self.setMenuBar(MenuBar(self))

		# Central widget
		main_widget = DuctTape(self)
		self.setCentralWidget(main_widget)


	def closeEvent(self, event):
		self.signal_close.emit(event)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setOverrideCursor(Qt.CursorShape.ArrowCursor)
	app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)
	window = RealMainWindow()
	window.show()
	retval = app.exec()
	Settings().save_to_disk()
	sys.exit(retval)
