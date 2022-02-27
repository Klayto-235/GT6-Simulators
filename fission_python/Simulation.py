from collections import namedtuple
import math
import datetime

from Assets import Assets
from Settings import Settings
from utility import divup


SimulationData = namedtuple("SimulationData", ["stopped_reason", "total_HU", "total_max_N", "peak_HUt", "exploded", "duration", "current_time", "current_HUt", "coolant_use"])
RodSelectionData = namedtuple("RodSelectionData", ["rod_total_HU", "rod_peak_N", "rod_penalty", "rod_moderated", "current_durability", "current_N_count", "current_N_output", "ref_mult", "rod_total_HUby", "rod_total_N", "HUt_by_rod"])
CellSelectionData = namedtuple("CellSelectionData", ["cell_total_L", "cell_peak_Lt", "cell_exploded", "is_H2O", "current_HUt", "current_Lt"])


class RodResults():
	def __init__(self):
		self.durability_data = [(0, 0)] # Durability(t)
		self.neutron_count_data = [(0, 0)] # NeutronCount(t)
		self.neutron_output_data = [(0, 0)] # NeutronOutput(t)
		self.HUtby_data = [(0, 0)] # HU/t by rod(t)

		self.totalHU = 0 # Total HU on rod (NOT BY ROD)
		self.max_output = 0 # Max neutron output per tick
		self.totalN = 0 # Total N emitted by rod
		self.totalHUby = 0 # Total HU by rod (NOT ON ROD)


	def append_durability(self, data):
		self.durability_data.append(data)


	def append_neutron_count(self, data):
		self.neutron_count_data.append(data)


	def append_neutron_output(self, data):
		self.neutron_output_data.append(data)


	def append_hutby(self, data):
		self.HUtby_data.append(data)


	def set_init_durability(self, data):
		self.durability_data[0] = (0, data)


class Rod():
	def __init__(self):
		self.neighbours = [] # Holds neighbours we will exchange neutrons with (do not add empty slots)
		self.neutron_count = 0 # Neutron count at each time, 0-th element should be t=0
		self.durability = 0 # Current rod health, all rods will display this, since in case of boom, all rods in that block will die.
		self.neutron_self = 0 # How much crap are we emitting on to ourselves
		self.neutron_max = 0 # Max neutrons per tick before diminishing returns
		self.neutron_max_raw = 0 # Neutron max of rod without coolant
		self.neutron_emission = 0 # Rod neutron emission
		self.neutron_div = 0 # How much of the crap we get from others are we doing something with, I forget what
		self.max_durability = 0 # Max rod durability, only used to post data to the reactro grid
		self.rod_name = "None" # Name of rod (for query and display purposes)
		self.coolant_name = "None" # Name of coolant (for query and display purposes)
		self.cell_size_factor = 0 # Multiplication factor for Mod rods: 2 if in a 1x1 cell and 1 if in a 2x2 cell
		self.cell_size_small = False # False for large, true for small, this is because LargeToSmall neutron flow needs a factor of 0.5, large->large, small->small and small->large all need 1.0
		self.is_moderated = False # Is this rod moderated?
		self.is_breeder = False # Am I a breeder?
		self.is_mod = False # Am I a Mod?
		self.is_abs = False # Am I an Abs?
		self.is_ref = False # Am I a Ref?
		self.is_fuel = False # Am I fuel?
		self.is_depleted = False # Changes to true if we deplete it.
		self.widget_handle = None # Handle to the widget related to this rod. This may keep widgets alive until the simulation is cleared.
		self.mod_factor = 0 # Moderator rod multiplication factor
		self.real_neutron_emission = 0 # Real neutron emission
		self.total_neutron_output = 0 # Total output
		self.HUt = 0 # Current HUt output (ON ROD)
		self.HUtby = 0 # Current HUt output (BY ROD)
		self.durability_loss = 0 # Durability loss previous second
		self.HU_conversion_factor = 1 # Neutron to HU conversion factor
		self.HU_conversion_divisor = 1 # Neutron to HU conversion divisor
		self.over_neutron_max = False # Do we suffer a durability penalty?
		self.cell_id = None # Cell id of the cell we are in.
		self.results = RodResults() # Results


	def set(self, whandle, rod_id, coolant_id, csf):
		self.rod_name = rod_id
		self.coolant_name = coolant_id
		self.cell_size_factor = csf
		self.widget_handle = whandle
		if csf == 2:
			self.cell_size_small = False
		else:
			self.cell_size_small = True
		if (rod_id == "Ref"):
			self.is_ref = True
		elif (rod_id == "Mod"):
			self.is_mod = True
		elif (rod_id == "Abs"):
			self.is_abs = True
		elif (rod_id == "U-238B" or rod_id == "Th-232B"):
			self.is_breeder = True
		else:
			self.is_fuel = True
		self.max_durability = Assets().rod[rod_id].durability
		self.durability = Assets().rod[rod_id].durability
		if (self.is_fuel):
			self.durability = self.durability * 120000
		if (self.is_abs or self.is_mod or self.is_ref):
			self.durability = 1
		self.neutron_self = divup(Assets().rod[rod_id].neutron_self * Assets().coolant[coolant_id].mod_self[0], Assets().coolant[coolant_id].mod_self[1])
		self.neutron_emission = divup(Assets().rod[rod_id].neutron_emission * Assets().coolant[coolant_id].mod_emission[0], Assets().coolant[coolant_id].mod_emission[1])
		self.neutron_max = divup(Assets().rod[rod_id].neutron_max * Assets().coolant[coolant_id].mod_max[0], Assets().coolant[coolant_id].mod_max[1])
		self.neutron_div = Assets().coolant[coolant_id].mod_div[0](Assets().rod[rod_id].neutron_div, Assets().coolant[coolant_id].mod_div[1])
		self.is_moderated = Assets().coolant[coolant_id].moderates
		self.neutron_max_raw = Assets().rod[rod_id].neutron_max
		if (self.is_mod):
			self.is_moderated = True
		elif not self.is_fuel:
			self.is_moderated = False
		if self.durability <= 0:
			self.is_depleted = True
			self.durability = 0
		self.results.set_init_durability(self.durability)
		if self.is_ref:
			self.mod_factor = 1
		self.neutron_count = self.neutron_self
		self.HU_conversion_factor = Assets().rod[rod_id].HUperN[0]
		self.HU_conversion_divisor = Assets().rod[rod_id].HUperN[1] * Assets().coolant[coolant_id].HU_div
		if (self.is_fuel):
			self.theo_max_HU = 20 * divup(self.durability, 2000) * divup(self.neutron_max, self.HU_conversion_divisor) * self.HU_conversion_factor
		else:
			self.theo_max_HU = 0


	def calculate_real_emission(self, index):
		if (self.is_depleted == False):
			self.real_neutron_emission = self.neutron_emission + divup((self.neutron_count - self.neutron_self), self.neutron_div)
			self.total_neutron_output = self.neutron_self + 4 * self.real_neutron_emission
			if (self.total_neutron_output > self.results.max_output):
				self.results.max_output = self.total_neutron_output
		else:
			self.total_neutron_output = 0
			self.real_neutron_emission = 0
		self.results.append_neutron_output((index, self.total_neutron_output))
		self.results.totalN += self.total_neutron_output * 20


	def add_neighbour(self, nid):
		self.neighbours.append(nid)


	def set_moderated(self, moderated):
		self.is_moderated = moderated


	def reset_neutron_count(self):
		self.neutron_count = self.neutron_self
		if self.is_depleted == False:
			self.HUtby = divup(self.neutron_self * self.HU_conversion_factor, self.HU_conversion_divisor)
		else:
			self.HUtby = 0


	def evaluate_durability_and_HUt(self, index):
		if self.is_depleted == False:
			self.HUt = divup(self.neutron_count * self.HU_conversion_factor, self.HU_conversion_divisor)
			self.results.totalHU += self.HUt * 20
			self.results.totalHUby += self.HUtby * 20
		if self.is_fuel:
			if self.total_neutron_output <= self.neutron_max:
				if self.is_moderated:
					self.durability_loss = 8000
				else:
					self.durability_loss = 2000
			else:
				if self.is_moderated:
					self.durability_loss = 4 * divup(8000 * self.total_neutron_output, self.neutron_max)
				else:
					self.durability_loss = divup(8000 * self.total_neutron_output, self.neutron_max)
				self.over_neutron_max = True
			self.durability -= self.durability_loss
			if self.durability <= 0:
				self.is_depleted = True
				self.durability = 0
				self.real_neutron_emission = 0
		elif self.is_breeder:
			self.durability_loss = self.neutron_count * math.ceil(1.5 ** (self.neutron_count / 500))
			self.durability -= self.durability_loss
			if self.durability <= 0:
				self.is_depleted = True
				self.durability = 0
				self.real_neutron_emission = 0
		self.results.append_durability((index, self.durability))
		self.results.append_neutron_count((index, self.neutron_count))
		self.results.append_hutby((index, self.HUtby))


	def is_active(self):
		#if self.is_fuel == True and self.is_depleted == False:
		if self.is_fuel == True:
			return True
		return False


	def post_rod_data(self, index):
		if self.is_fuel:
			self.widget_handle.set_durability(self.results.durability_data[index][1] / self.max_durability / 120000 * 100.0)
		elif self.is_breeder:
			self.widget_handle.set_durability(100.0 - self.results.durability_data[index][1] / self.max_durability * 100.0)
		if self.is_fuel or self.is_abs or self.is_breeder:
			tempvar = -1
			if self.neutron_max > 0:
				tempvar = self.results.neutron_output_data[index][1] / self.neutron_max * 100.0
			self.widget_handle.set_neutron_count(self.results.neutron_count_data[index][1], tempvar)
		elif self.is_mod or self.is_ref:
			self.widget_handle.set_moderation_factor(self.mod_factor)


	def recall_rod_data(self):
		self.widget_handle.reset_durability()
		self.widget_handle.reset_neutron_count()


class CellResults():
	def __init__(self):
		self.HUt_data = [(0, 0)] # HUt(t)
		self.Lt_data = [(0, 0)] # Lt(t)

		self.totalL = 0 # Total L of coolant
		self.totalHU = 0 # Total HU


	def append_HUt(self, data):
		self.HUt_data.append(data)


	def append_Lt(self, data):
		self.Lt_data.append(data)


class Cell():
	def __init__(self):
		self.coolant_name = "None" # Name of coolant (for query and display purposes)
		self.HUt = 0 # HU/t for each time point in the simulation
		self.Lt = 0 # Convert to L/t for each time point in the simulation
		self.LtoHU = 0 # Conversion factor between HU and L of coolant
		self.contained_rods = [] # Stores rod indices of rods in this cell
		self.exploded = False # Will store a nice comment if we go boom. :)
		self.widget_handle = None # Handle of the widget related to this cell, this may keep the widget alive until the simulation is cleared.
		self.Lt_explosion_limit = Assets().tank_capacity # Explode if we reach this (as far as I can tell this is the reactor tank capacity, so this is a hard cap)
		self.results = CellResults() # Results


	def set(self, whandle, coolant_id):
		self.coolant_name = coolant_id
		self.LtoHU = float(Assets().coolant[self.coolant_name].capacity)
		self.widget_handle = whandle


	def evaluate_hutol(self, index):
		if self.HUt > 0:
			self.Lt = self.HUt / self.LtoHU
		else:
			self.Lt = 0.0
		self.results.totalL += 20 * self.Lt
		self.results.totalHU += 20 * self.HUt
		self.results.append_Lt((index, self.Lt))
		self.results.append_HUt((index, self.HUt))
		if (self.Lt > self.Lt_explosion_limit):
			self.exploded = True
			return False
		else:
			return True

		
	def post_cell_data(self, index):
		self.widget_handle.set_coolant_flux("{:.2f}".format(self.results.Lt_data[index][1]), str(self.results.HUt_data[index][1]), self.exploded) 


	def recall_cell_data(self):
		self.widget_handle.reset_coolant_flux()


class SimResults():
	def __init__(self):
		self.HUt_data = [] # HUt(t)

		self.totalHU = 0 # Total HU produced by the reactor before either depleting a rod or exploding (or stopping due to durability penalty)

		self.coolant_use_data = {}


	def append_HUt(self, data):
		self.HUt_data.append(data)


	def reset(self):
		self.HUt_data = []
		self.totalHU = 0
		self.coolant_use_data = {}


class Simulation():
	def __init__(self, info_panel):

		self.info_panel = info_panel

		self.simulated_time = 0
		self.max_time = 0
		self.exploded = False
		self.has_depleted_rod = False
		self.moderation_changed = False
		self.has_over_max_rod = False

		self.HUt = -100000 # Current HU/t
		self.prev_HUt = -1000000 # HU/t previous step to check if we reached a steady state
		self.max_N_count = 0 # Maximal neutron count, not the same as max HU due to absorber rods, Na/Sn coolants etc

		self.results = SimResults()

		self.rod_dict = {} # Map locations to rod indices in rod_data
		self.rod_data = [] # Holds simulation data for specified rod, i.e. time dependence of everything we care about
		self.cell_dict = {} # Map cell locations to indices in cell_data
		self.cell_data = [] # Maybe we need this to store data for cells, i.e. HU/t for quad cells is a bit trickier, so each rod needs to know what cell it belongs to
		self.fuel_rods = [] # Store indices of fuel rods for simulation to iterate over
		self.mod_rods = [] # Store indices of moderator rods for the simulation to iterate over
		self.button_dict = {} # Maps buttons to rod indices, this will serve to make select work
		self.block_dict = {} # Maps blocks to cell indices, this will serve to make select work in 2x2 blocks if you click and empty button

		self.stop_on_overmax = True # If true the simulation stops when a rod pays durability penalty due to too many neutrons

		self.reason = ""


	def clear_simulation(self):
		self.rod_dict = {}
		self.rod_data = []
		self.cell_dict = {}
		self.cell_data = []
		self.fuel_rods = []
		self.mod_rods = []
		self.simulated_time = 0
		self.max_time = 0
		self.exploded = False
		self.has_depleted_rod = False
		self.moderation_changed = False
		self.has_over_max_rod = False
		self.row_offset = 0
		self.col_offset = 0
		self.results.reset()
		self.results.append_HUt((0, 0))
		self.HUt = -100000
		self.prev_HUt = -1000000
		self.max_N_count = 0
		self.reason = ""


	def push_rod(self, dict_entry, button, cell, fact = 1):
		self.rod_dict[dict_entry] = len(self.rod_data)
		self.rod_data.append(Rod())
		self.rod_data[len(self.rod_data) - 1].set(button, button.rod_name, cell.coolant_name, fact)
		if (self.rod_data[len(self.rod_data) - 1].is_depleted):
			self.has_depleted_rod = True
		if (self.rod_data[-1].is_fuel):
			self.max_N_count = self.max_N_count + self.rod_data[len(self.rod_data) - 1].neutron_max_raw
		self.button_dict[button] = len(self.rod_data) - 1


	def push_cell(self, dict_entry, cell, rods):
		self.cell_data.append(Cell())
		self.cell_data[len(self.cell_data) - 1].set(cell, cell.coolant_name)
		self.cell_dict[dict_entry] = len(self.cell_data) - 1
		self.cell_data[len(self.cell_data) - 1].contained_rods = rods
		for i in rods:
			self.rod_data[i].cell_id = len(self.cell_data) - 1
		if (cell.coolant_name == "None"):
			tempbool = False
			for i in rods:
				if self.rod_data[i].is_fuel or self.rod_data[i].is_abs or self.rod_data[i].is_breeder:
					tempbool = True
			if tempbool:
				self.exploded = True
				self.cell_data[len(self.cell_data) - 1].exploded = True
		self.block_dict[cell] = len(self.cell_data) - 1


	def try_add_neighbour(self, dict_entry):
		if (dict_entry in self.rod_dict):
			tidx = self.rod_dict[dict_entry]
			self.rod_data[tidx].add_neighbour(len(self.rod_data) - 1)
			self.rod_data[len(self.rod_data) - 1].add_neighbour(tidx)


	def construct_simulation(self, grid_data): 
		self.nrod = 0
		nrow = len(grid_data)
		if nrow == 0:
			return
		ncol = len(grid_data[0])
		if ncol == 0:
			return
		for row in range(nrow):
			for col in range(ncol):
				if (grid_data[row][col].shape_small):
					temp_is_empty = True
					temp_rod_ids = []

					if (grid_data[row][col].buttons_small[0].is_full()):
						temp_is_empty = False
						temp_rod_ids.append(len(self.rod_data))
						self.push_rod((row, col, 0), grid_data[row][col].buttons_small[0], grid_data[row][col])
						if (row > 0):
							if (grid_data[row - 1][col].shape_small):
								self.try_add_neighbour((row - 1, col, 2))
							else:
								self.try_add_neighbour((row - 1, col, 5))
						if (col > 0):
							if (grid_data[row][col - 1].shape_small):
								self.try_add_neighbour((row, col - 1, 1))
							else:
								self.try_add_neighbour((row, col - 1, 5))

					if (grid_data[row][col].buttons_small[1].is_full()):
						temp_is_empty = False
						temp_rod_ids.append(len(self.rod_data))
						self.push_rod((row, col, 1), grid_data[row][col].buttons_small[1], grid_data[row][col])
						if (row > 0):
							if (grid_data[row - 1][col].shape_small):
								self.try_add_neighbour((row - 1, col, 3))
							else:
								self.try_add_neighbour((row - 1, col, 5))
						self.try_add_neighbour((row, col, 0))

					if (grid_data[row][col].buttons_small[2].is_full()):
						temp_is_empty = False
						temp_rod_ids.append(len(self.rod_data))
						self.push_rod((row, col, 2), grid_data[row][col].buttons_small[2], grid_data[row][col])
						self.try_add_neighbour((row, col, 0))
						if (col > 0):
							if (grid_data[row][col - 1].shape_small):
								self.try_add_neighbour((row, col - 1, 3))
							else:
								self.try_add_neighbour((row, col - 1, 5))

					if (grid_data[row][col].buttons_small[3].is_full()):
						temp_is_empty = False
						temp_rod_ids.append(len(self.rod_data))
						self.push_rod((row, col, 3), grid_data[row][col].buttons_small[3], grid_data[row][col])
						self.try_add_neighbour((row, col, 1))
						self.try_add_neighbour((row, col, 2))
					if (temp_is_empty == False):
						self.push_cell((row, col), grid_data[row][col], temp_rod_ids)

				else:
					if (grid_data[row][col].button_large.is_full()):
						self.push_rod((row, col, 5), grid_data[row][col].button_large, grid_data[row][col], 2)
						self.push_cell((row, col), grid_data[row][col], [len(self.rod_data) - 1])
						if (row > 0):
							if (grid_data[row - 1][col].shape_small):
								self.try_add_neighbour((row - 1, col, 2))
								self.try_add_neighbour((row - 1, col, 3))
							else:
								self.try_add_neighbour((row - 1, col, 5))
						if (col > 0):
							if (grid_data[row][col - 1].shape_small):
								self.try_add_neighbour((row, col - 1, 1))
								self.try_add_neighbour((row, col - 1, 3))
							else:
								self.try_add_neighbour((row, col - 1, 5))

		self.max_time = 1000000000
		for i in range(len(self.rod_data)):
			if (self.rod_data[i].is_fuel == True):
				self.fuel_rods.append(i)
				if (divup(self.rod_data[i].durability, 2000) < self.max_time):
					self.max_time = divup(self.rod_data[i].durability, 2000) + 1
			if (self.rod_data[i].is_mod == True):
				self.mod_rods.append(i)

		self.max_N_count = self.max_N_count * (self.max_time - 1) * 20


	def run_simulation(self, autorun):
		if (self.simulated_time < self.max_time and self.exploded == False and self.has_depleted_rod == False):
			temp = self.simulate(autorun)
			self.collect_coolant_data()
			return temp
		else:
			self.reason = "No fuel"
		return True


	def simulate(self, autorun):
		if len(self.fuel_rods) == 0:
			self.reason = "No fuel"
			return True
		if autorun:
			starttime = datetime.datetime.now()
		while (self.simulated_time < self.max_time and self.exploded == False and self.has_depleted_rod == False and (abs(self.prev_HUt - self.HUt) > 0 or self.moderation_changed == True)):
			self.prev_HUt = self.HUt
			self.simulation_step(self.simulated_time)
			self.simulated_time = self.simulated_time + 1
			if self.stop_on_overmax and self.has_over_max_rod:
				self.reason = "Durability penalty"
				break
			if autorun:
				currenttime = datetime.datetime.now()
				timediff = currenttime - starttime
				if timediff.total_seconds() > Settings().get_float("AutosimTimeout"):
					self.reason = "Time out"
					return False
		if (self.simulated_time < self.max_time and self.exploded == False and self.has_depleted_rod == False):
			if not (self.stop_on_overmax and self.has_over_max_rod):
				self.extrapolate()
		if self.reason == "":
			if self.exploded:
				self.reason = "Reactor exploded"
			elif self.has_depleted_rod:
				self.reason = "Rod depleted"
			else:
				self.reason = "Unknown, oops"
		return True


	def extrapolate(self):
		temp_maxt = self.max_time
		for i in range(len(self.rod_data)):
			if self.rod_data[i].durability_loss > 0:
				tempt = divup(self.rod_data[i].durability, self.rod_data[i].durability_loss)
				if (tempt < temp_maxt):
					temp_maxt = tempt
		self.simulated_time = self.simulated_time + temp_maxt
		self.results.totalHU += self.HUt * temp_maxt * 20
		for i in range(len(self.rod_data)):
			self.rod_data[i].durability -= self.rod_data[i].durability_loss * temp_maxt
			if self.rod_data[i].durability <= 0:
				self.rod_data[i].is_depleted = True
				self.has_depleted_rod = True
				self.rod_data[i].durability = 0
			self.rod_data[i].results.append_durability((self.simulated_time, self.rod_data[i].durability))
			self.rod_data[i].results.append_neutron_count((self.simulated_time, self.rod_data[i].neutron_count))
			self.rod_data[i].results.append_neutron_output((self.simulated_time, self.rod_data[i].total_neutron_output))
			self.rod_data[i].results.append_hutby((self.simulated_time, self.rod_data[i].HUtby))
			self.rod_data[i].results.totalHU += self.rod_data[i].HUt * 20 * temp_maxt
			self.rod_data[i].results.totalN += self.rod_data[i].total_neutron_output * 20 * temp_maxt
			self.rod_data[i].results.totalHUby += self.rod_data[i].HUtby * 20 * temp_maxt
		self.results.append_HUt((self.simulated_time, self.HUt))
		for i in range(len(self.cell_data)):
			self.cell_data[i].results.append_Lt((self.simulated_time, self.cell_data[i].Lt))
			self.cell_data[i].results.totalL += self.cell_data[i].Lt * 20 * temp_maxt
			self.cell_data[i].results.append_HUt((self.simulated_time, self.cell_data[i].HUt))
			self.cell_data[i].results.totalHU += self.cell_data[i].HUt * 20 * temp_maxt


	def cell_update_step(self, current_time):
		self.HUt = 0
		for i in range(len(self.cell_data)):
			self.cell_data[i].HUt = 0
			for j in self.cell_data[i].contained_rods:
				self.cell_data[i].HUt += self.rod_data[j].HUt
				if (self.rod_data[j].is_depleted):
					self.has_depleted_rod = True
			self.HUt += self.cell_data[i].HUt
			tempbool = self.cell_data[i].evaluate_hutol(current_time)
			if tempbool == False:
				self.exploded = True
		self.results.append_HUt((current_time, self.HUt))
		self.results.totalHU += 20 * self.HUt


	def rod_update_step(self, current_time):
		# Calculates real emission from previous neutron count
		for i in self.fuel_rods:
			self.rod_data[i].calculate_real_emission(current_time)
		# Resets own neutron count to self emission
		for i in range(len(self.rod_data)):
			self.rod_data[i].reset_neutron_count()
		# Calculates new neutron counts on all rods
		for i in self.fuel_rods:
			for j in self.rod_data[i].neighbours:
				if self.rod_data[j].is_fuel or self.rod_data[j].is_abs:
					if self.rod_data[i].cell_size_small == False:
						if self.rod_data[j].cell_size_small == False:
							self.rod_data[j].neutron_count += 2 * divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(2 * divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
						else:
							self.rod_data[j].neutron_count += divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
					else:
						self.rod_data[j].neutron_count += self.rod_data[i].real_neutron_emission
						self.rod_data[i].HUtby += divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
				elif self.rod_data[j].is_mod:
					if self.rod_data[i].cell_size_small == False:
						if self.rod_data[j].cell_size_small == False:
							self.rod_data[i].neutron_count += 2 * divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor, 2)
							self.rod_data[i].HUtby += divup(2 * divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor, 2) * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
						else:
							self.rod_data[i].neutron_count += divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor, 2)
							self.rod_data[i].HUtby += divup(divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor, 2) * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
					else:
						self.rod_data[i].neutron_count += self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor
						self.rod_data[i].HUtby += divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].mod_factor * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
				elif self.rod_data[j].is_ref:
					if self.rod_data[i].cell_size_small == False:
						if self.rod_data[j].cell_size_small == False:
							self.rod_data[i].neutron_count += 2 * divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(2 * divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
						else:
							self.rod_data[i].neutron_count += divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
					else:
						self.rod_data[i].neutron_count += self.rod_data[i].real_neutron_emission
						self.rod_data[i].HUtby += divup(self.rod_data[i].real_neutron_emission * self.rod_data[i].HU_conversion_factor, self.rod_data[i].HU_conversion_divisor)
				elif self.rod_data[j].is_breeder and self.rod_data[i].is_moderated == False:
					if self.rod_data[i].cell_size_small == False:
						if self.rod_data[j].cell_size_small == False:
							self.rod_data[j].neutron_count += 2 * divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(2 * divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
						else:
							self.rod_data[j].neutron_count += divup(self.rod_data[i].real_neutron_emission, 2)
							self.rod_data[i].HUtby += divup(divup(self.rod_data[i].real_neutron_emission, 2) * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
					else:
						self.rod_data[j].neutron_count += self.rod_data[i].real_neutron_emission
						self.rod_data[i].HUtby += divup(self.rod_data[i].real_neutron_emission * self.rod_data[j].HU_conversion_factor, self.rod_data[j].HU_conversion_divisor)
		# Calculates rod HUt and durability loss
		for i in range(len(self.rod_data)):
			self.rod_data[i].evaluate_durability_and_HUt(current_time)
			if self.rod_data[i].over_neutron_max:
				self.has_over_max_rod = True
		# Calculates moderator rod factors based on active rods
		for i in self.mod_rods:
			self.rod_data[i].mod_factor = 0
			for j in self.rod_data[i].neighbours:
				if self.rod_data[j].is_active():
					if self.rod_data[i].cell_size_factor == 2:
						self.rod_data[i].mod_factor += self.rod_data[j].cell_size_factor
					else:
						self.rod_data[i].mod_factor += 1


	def moderation_update_step(self, current_time):
		if (self.moderation_changed):
			self.moderation_changed = False
		temp_rod_set = set()
		for i in range(len(self.rod_data)):
			if self.rod_data[i].is_moderated:
				temp_rod_set.add(i)
		for i in temp_rod_set:
			for j in self.rod_data[i].neighbours:
				if self.rod_data[j].is_fuel:
					if (self.rod_data[j].is_moderated == False):
						self.moderation_changed = True
					self.rod_data[j].set_moderated(True)


	def simulation_step(self, prev_time_step):
		current_time = prev_time_step + 1

		# Neutron calculations
		self.rod_update_step(current_time)
		# Moderation spreading
		self.moderation_update_step(current_time)
		# Cell HU/t and L/t calculations
		self.cell_update_step(current_time)


	def collect_coolant_data(self):
		for i in range(len(self.cell_data)):
			self.results.coolant_use_data[self.cell_data[i].coolant_name] = self.results.coolant_use_data.get(self.cell_data[i].coolant_name, 0) + self.cell_data[i].results.Lt_data[-1][1]


	def post_plot_data(self):
		self.info_panel.set_plot_data(self.results.HUt_data)


	def post_sim_data(self, index): 
		self.info_panel.set_simulation_data(SimulationData(self.reason, self.results.totalHU, self.max_N_count, self.results.HUt_data[-1][1], self.exploded, self.simulated_time, self.results.HUt_data[index][0], self.results.HUt_data[index][1], self.results.coolant_use_data))
		for i in range(len(self.rod_data)):
			self.rod_data[i].post_rod_data(index)
		for i in range(len(self.cell_data)):
			self.cell_data[i].post_cell_data(index)
		

	def recall_sim_data(self):
		self.info_panel.reset_simulation_data()
		for i in range(len(self.rod_data)):
			self.rod_data[i].recall_rod_data()
		for i in range(len(self.cell_data)):
			self.cell_data[i].recall_cell_data()


	def post_selection_data(self, index, target): 
		rod_id = self.button_dict.get(target.slot)
		if rod_id is not None:
			trod = self.rod_data[rod_id]
			tcell = self.cell_data[trod.cell_id] 
			if trod.is_fuel:
				tempstr = "{:.3f}".format(trod.results.durability_data[index][1] / 120000) + "/" + str(Assets().rod[trod.rod_name].durability)
			elif trod.is_breeder:
				tempstr = str(trod.results.durability_data[index][1]) + "/" + str(Assets().rod[trod.rod_name].durability)
			else:
				tempstr = "infinite"
			if trod.is_fuel:
				tstroutput = str(trod.results.neutron_output_data[index][1]) + "/" + str(trod.neutron_max)
			else:
				tstroutput = "0"
			rdata = RodSelectionData(trod.results.totalHU, trod.results.max_output, trod.over_neutron_max, trod.is_moderated, tempstr, trod.results.neutron_count_data[index][1], tstroutput, trod.mod_factor, trod.results.totalHUby, trod.results.totalN, trod.results.HUtby_data[index][1])
			cdata = CellSelectionData(tcell.results.totalL, tcell.results.Lt_data[-1][1], tcell.exploded, tcell.coolant_name == "H2O", tcell.results.HUt_data[index][1], tcell.results.Lt_data[index][1])
			self.info_panel.set_selection_data(rdata, cdata)
			return
		cell_id = self.block_dict.get(target.block)
		if cell_id is not None:
			tcell = self.cell_data[cell_id]
			cdata = CellSelectionData(tcell.results.totalL, tcell.results.Lt_data[-1][1], tcell.exploded, tcell.coolant_name == "H2O", tcell.results.HUt_data[index][1], tcell.results.Lt_data[index][1])
			self.info_panel.set_selection_data(None, cdata)
		else:
			self.recall_selection_data()


	def recall_selection_data(self):
		self.info_panel.reset_selection_data()


	def set_stop_on_overmax(self, value):
		self.stop_on_overmax = value