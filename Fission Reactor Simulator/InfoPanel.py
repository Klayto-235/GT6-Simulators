from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from math import gcd

from Plot import HairyPlotter
from Assets import Assets
from utility import to_metric, to_human_readable_time, divup


class InfoPanel(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		vbox_layout = QVBoxLayout(self)
		vbox_layout.setContentsMargins(4,0,0,0)
		vbox_layout.setSpacing(8)
		
		self.plot = HairyPlotter(self)
		self.plot.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		self.signal_plot_time_selection_shanged = self.plot.signal_plot_time_selection_shanged
		
		scroll_area = QScrollArea(self)
		scroll_area.setWidgetResizable(True)
		self.scroll_area_inside = QWidget(self)
		scroll_area.setWidget(self.scroll_area_inside)
		label_layout = QVBoxLayout(self.scroll_area_inside)
		label_layout.setSpacing(10)

		self.label_rod = QLabel(self)
		self.label_cell = QLabel(self)
		self.label_simulation = QLabel(self)
		self.label_coolants = QLabel(self)
		self.label_stats = QLabel(self)

		self.label_rod.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.label_cell.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.label_simulation.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.label_coolants.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.label_stats.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

		vbox_layout.addWidget(self.plot)
		vbox_layout.addWidget(scroll_area)
		label_layout.addWidget(self.label_simulation, 0)
		label_layout.addWidget(self.label_coolants, 1)
		label_layout.addWidget(self.label_cell, 2)
		label_layout.addWidget(self.label_rod, 3)
		label_layout.addWidget(self.label_stats, 4)
		label_layout.setStretch(0, 0)
		label_layout.setStretch(1, 0)
		label_layout.setStretch(2, 0)
		label_layout.setStretch(3, 0)
		label_layout.setStretch(4, 1)
		
		# Initial state
		self.reset_selection_data()
		self.reset_simulation_data()
		self.reset_selection_stats()
		

	def get_plot_selected_time(self):
		return self.plot.get_selected_time()


	def show_plot_data(self):
		self.plot.show_data()


	def hide_plot_data(self):
		self.plot.hide_data()


	def set_plot_data(self, data):
		self.plot.plot_data(data)


	def set_selection_stats(self, coolant, rod):
		statstring = "<b>SELECTED ROD STATS:</b>"
		temp = Assets().rod[rod].durability
		if temp > 0:
			tempstr = str(temp)
		else:
			tempstr = "infinite"
		statstring += "<br>Durability: " + tempstr
		temp = Assets().rod[rod].neutron_emission
		tempc = Assets().coolant[coolant].mod_emission
		tempr = divup(temp * tempc[0], tempc[1])
		tempstr = str(tempr) + " (" + str(temp) + ")"
		statstring += "<br>Neutron emission: " + tempstr
		temp = Assets().rod[rod].neutron_self
		tempc = Assets().coolant[coolant].mod_self
		tempr = divup(temp * tempc[0], tempc[1])
		tempstr = str(tempr) + " (" + str(temp) + ")"
		statstring += "<br>Neutron self emission: " + tempstr
		temp = Assets().rod[rod].neutron_max
		tempc = Assets().coolant[coolant].mod_max
		tempr = divup(temp * tempc[0], tempc[1])
		tempstr = str(tempr) + " (" + str(temp) + ")"
		if temp == 0:
			tempstr = "0 (0)"
		statstring += "<br>Neutron max: " + tempstr
		temp = Assets().rod[rod].neutron_div
		tempc = Assets().coolant[coolant].mod_div
		tempr = tempc[0](temp, tempc[1])
		tempstr = "1/" + str(tempr) + " (" + "1/" + str(temp) + ")"
		if temp == 0:
			tempstr = "0 (0)"
		statstring += "<br>Neutron emission factor: " + tempstr
		temp = Assets().rod[rod].HUperN
		tempc = Assets().coolant[coolant].HU_div
		tempr = (temp[0], temp[1] * tempc)
		if tempr[1] == 1 or tempr[0] == 0:
			tempstr = str(tempr[0])
		else:
			divfact = gcd(*tempr)
			tempstr = str(tempr[0] // divfact) + "/" + str(tempr[1] // divfact)
		tempstr += " ("
		if temp[1] == 1 or temp[0] == 0:
			tempstr += str(temp[0])
		else:
			divfact = gcd(*temp)
			tempstr += str(temp[0] // divfact) + "/" + str(temp[1] // divfact)
		tempstr += ")"
		statstring += "<br>HU per neutron: " + tempstr
		self.label_stats.setText(statstring)


	def set_selection_data(self, rdata, cdata):
		if rdata is not None:
			rodstring = "<b>SELECTED ROD DATA:</b>"
			rodstring += "<br>Total HU on rod: " + to_metric(rdata.rod_total_HU) + "HU"
			rodstring += "<br>Total HU by rod: " + to_metric(rdata.rod_total_HUby) + "HU"
			rodstring += "<br>Total N emitted: " + to_metric(rdata.rod_total_N) + "N"
			rodstring += "<br>Peak neutron emission: " + str(rdata.rod_peak_N) + " N/t"
			rodstring += "<br>Durability penalty: "
			if rdata.rod_penalty:
				rodstring += "Yes"
			else:
				rodstring += "No"
			rodstring += "<br>Gets moderated: "
			if rdata.rod_moderated:
				rodstring += "Yes"
			else:
				rodstring += "No"
			rodstring += "<br>Reflection multiplier: " + str(rdata.ref_mult)
			rodstring += "<br><br>Current durability: " + str(rdata.current_durability)
			rodstring += "<br>Current neutron count: " + str(rdata.current_N_count) + " N"
			rodstring += "<br>Current neutron output: " + str(rdata.current_N_output) + " N/t"
			rodstring += "<br>Current HU/t by rod: " + str(rdata.HUt_by_rod) + " HU/t"
			self.label_rod.setText(rodstring)
		else:
			self.label_rod.setText("<b>SELECTED ROD DATA:</b><br>No data to show.")

		cellstring = "<b>SELECTED BLOCK DATA:</b>"
		if (cdata.is_H2O):
			cellstring += "<br>Total L in: " + to_metric(cdata.cell_total_L) + "L"
			cellstring += "<br>Peak L/t in: " + "{:.2f}".format(cdata.cell_peak_Lt) + " L/t"
			cellstring += "<br>Total L out: " + to_metric(cdata.cell_total_L * 160) + "L"
			cellstring += "<br>Peak L/t out: " + "{:.2f}".format(cdata.cell_peak_Lt * 160) + " L/t"
		else:
			cellstring += "<br>Total L: " + to_metric(cdata.cell_total_L) + "L"
			cellstring += "<br>Peak L/t: " + "{:.2f}".format(cdata.cell_peak_Lt) + " L/t"
		cellstring += "<br>Exploded: "
		if cdata.cell_exploded:
			cellstring += "Yes"
		else:
			cellstring += "No"
		cellstring += "<br><br>Current HU/t: " + str(cdata.current_HUt) + " HU/t"
		if cdata.is_H2O:
			cellstring += "<br>Current L/t in: " + "{:.2f}".format(cdata.current_Lt) + " L/t"
			cellstring += "<br>Current L/t out: " + "{:.2f}".format(cdata.current_Lt * 160) + " L/t"
		else:
			cellstring += "<br>Current L/t: " + "{:.2f}".format(cdata.current_Lt) + " L/t"
		self.label_cell.setText(cellstring)


	def set_simulation_data(self, data):
		tempstring = "<b>SIMULATION DATA:</b>"
		tempstring += "<br>Simulation end reason: " + data.stopped_reason
		tempstring += "<br><br>Base max neutron emission: " + to_metric(data.total_max_N) + "N"
		tempstring += "<br>Total HU produced: " + to_metric(data.total_HU) + "HU"
		if data.total_max_N != 0:
			tempstring += "<br>Relative efficiency: " + ("{:.6f}".format((data.total_HU / data.total_max_N) * 100.0)) + "%"
		else:
			tempstring += "<br>Relative efficiency: N/A"
		tempstring += "<br>Peak HU/t: " + str(data.peak_HUt) + " HU/t"
		tempstring += "<br>Total distilled water loss: " + to_metric(data.total_HU / (80 * 20)) + "L"
		tempstring += "<br>Peak distilled water loss: " + to_metric(data.peak_HUt / (80 * 20)) + "L/t"
		tempstring += "<br>Exploded: "
		if (data.exploded):
			tempstring += "Yes<br>"
		else:
			tempstring += "No<br>"
		tempstring += "Total duration: " + to_human_readable_time(data.duration)
		tempstring += "<br>"
		tempstring += "<br>Current time: " + to_human_readable_time(data.current_time)
		tempstring += "<br>Current HU/t: " + to_metric(data.current_HUt) + "HU/t"
		tstr = "<b>COOLANT DATA:</b>"
		for k,v in data.coolant_use.items():
			if k != "None":
				tstr += "<br>" + k + ": " + "{:.3f}".format(v) + " L/t"
		if tstr == "<b>COOLANT DATA:</b>":
			tstr += "<br>No data to show."
		self.label_simulation.setText(tempstring)
		self.label_coolants.setText(tstr)

	def reset_selection_data(self):
		self.label_rod.setText("<b>SELECTED ROD DATA:</b><br>No data to show.")
		self.label_cell.setText("<b>SELECTED BLOCK DATA:</b><br>No data to show.")


	def reset_selection_stats(self):
		self.label_stats.setText("<b>SELECTED SLOT STATS:</b><br>No stats to show.")


	def reset_simulation_data(self):
		self.label_simulation.setText("<b>SIMULATION DATA:</b><br>No data to show.")
		self.label_coolants.setText("<b>COOLANT DATA</b><br>No data to show.")