from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from pyqtgraph import PlotWidget, InfiniteLine, setConfigOption, mkPen

from Assets import Assets

setConfigOption("foreground", 'k')


class HairyPlotter(PlotWidget):
	signal_plot_time_selection_shanged = pyqtSignal(int)

	def __init__(self, parent=None):
		super().__init__(parent)

		self.setToolTip("Reactor HU/t output with respect to time.\nThe bottom axis shows time in seconds, except perhaps for the final point.\nIf a steady state is reached the final point will be extrapolated.\nAs a result it may correspond to a much later time.")

		self.setTitle("Reactor total HU/t output")
		self.setLabel('left', "HU/t", color='k')
		self.setLabel('bottom', "t [time point index]")
		self.setBackground((255, 255, 255, 128))
		self.getPlotItem().setContentsMargins(3,0,10,10)
		self.getPlotItem().setMenuEnabled(False)

		self.setMouseEnabled(x=False, y=False)

		self.selector = InfiniteLine()
		self.selector.setAngle(90)
		self.selector.setMovable(True)
		self.selector.setValue(1)
		self.selector.setBounds((0, 2))
		self.selector.setPen((0, 150, 0, 255), width=1)
		self.selector.setHoverPen((250, 0, 0, 255), width=1)
		self.selector.sigPositionChanged.connect(self.inf_line_moved)

		self.addItem(self.selector)

		self.setXRange(-0.04, 2.04, padding=0)
		self.setYRange(-0.02, 1.02, padding=0)

		self.plot_data_item = self.plot([0], [0])

		self.hide_storage = ([0], [0])
		self.scale = 0
		self.old_index = 1

		self.hideButtons()

		
	def mousePressEvent(self, event):
		self.selector.setValue(self.getPlotItem().vb.mapSceneToView(event.position()).x())
		super().mousePressEvent(event)


	def plot_data(self, data):
		xdata = list(range(len(data)))
		ydata = list(map(list, zip(*data)))[1]
		self.hide_storage = (xdata, ydata)
		self.internal_plot(xdata, ydata)

	
	def internal_plot(self, xdata, ydata):
		tscale = ydata[-1]
		self.scale = 0
		tempscale = 1
		while (tscale > 1999):
			self.scale = self.scale + 3
			tscale = tscale / 1000
			tempscale = tempscale * 1000
		for i in range(len(ydata)):
			ydata[i] = ydata[i] / tempscale
		self.set_y_label()
		self.plot_data_item.setData(xdata, ydata, symbol='x', symbolBrush=(200, 30, 30, 255), pen=mkPen((75, 75, 150, 255), width=1))
		if len(ydata) == 1:
			self.setXRange(-0.104, 0.104, padding=0)
			self.setYRange(-0.04, 1.04, padding=0)
		else:
			self.setXRange(-(len(ydata)) * 0.04, (len(ydata) - 1) * 1.04, padding=0)
			self.setYRange(-ydata[-1] * 0.04, ydata[-1] * 1.04, padding=0)
		self.selector.setBounds((0, len(xdata) - 1))
		self.selector.setValue(len(xdata) - 1)


	def set_y_label(self):
		if self.scale in Assets().metric_prefix:
			self.setLabel('left', Assets().metric_prefix[self.scale] + "HU/t")
		else:
			self.setLabel('left', "HU/t [10^" + str(self.scale) + "]")


	def reset_y_label(self):
		self.setLabel('left', "HU/t")


	def clear_data(self):
		self.setXRange(-0.05, 2.05, padding=0)
		self.setYRange(-0.02, 1.02, padding=0)
		self.reset_y_label()
		self.scale = 0
		self.plot_data_item.setData([0], [0])
		self.selector.setBounds((0, 2))


	def hide_data(self):
		self.clear_data()


	def show_data(self):
		self.internal_plot(self.hide_storage[0], self.hide_storage[1])


	def inf_line_moved(self):
		temppos = round(self.selector.value())
		if (temppos != self.old_index):
			self.old_index = temppos
			self.signal_plot_time_selection_shanged.emit(temppos)


	def get_selected_time(self):
		return round(self.selector.value())


	def sizeHint(self):
		return QSize(350, 250)


	def minimumSizeHint(self):
		return QSize(350, 250)