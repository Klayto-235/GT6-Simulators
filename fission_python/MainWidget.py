from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox

from Assets import Assets
from Toolbox import ToolboxLeft, ToolboxTop
from ReactorGrid import ReactorGrid
from InfoPanel import InfoPanel
from Simulation import Simulation
from InfoPanel import InfoPanel
from Historian import Historian
from MenuBar import DialogResult
from ReactorGridBlock import ReactorGridBlock
from Settings import Settings


class DuctTape(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.historian = Historian()
		self.main_window = parent
		self.menu_bar = parent.menuBar()

		self.restorePreviousSize()
		self.setStyleSheet(Assets().stylesheet)

		# Main window close event connection
		self.main_window.signal_close.connect(self.on_close_event)

		# Historian calblacks
		self.historian.callback_disable_redo = self.menu_bar.disable_redo
		self.historian.callback_disable_undo = self.menu_bar.disable_undo
		self.historian.callback_enable_redo = self.menu_bar.enable_redo
		self.historian.callback_enable_undo = self.menu_bar.enable_undo

		# Menu bar connections
		self.menu_bar.signal_new_state.connect(self.on_do_new_state)
		self.menu_bar.signal_on_dialog_new_accepted.connect(self.on_dialog_new_accepted)
		self.menu_bar.signal_load_state.connect(self.on_do_load_state)
		self.menu_bar.signal_save_state.connect(self.on_do_save_state)
		self.menu_bar.signal_save_state_as.connect(self.on_do_save_state_as)
		self.menu_bar.signal_quit.connect(self.on_do_quit)
		self.menu_bar.signal_undo.connect(self.on_do_undo)
		self.menu_bar.signal_redo.connect(self.on_do_redo)
		self.menu_bar.signal_options.connect(self.on_do_options)
		self.menu_bar.signal_readme.connect(self.on_do_readme)
		self.menu_bar.signal_about.connect(self.on_do_about)
		self.menu_bar.signal_material_cost.connect(self.on_calculate_material_costs)

		# Widgets
		self.reactor_grid = ReactorGrid(self)
		self.reactor_grid.signal_clicked.connect(self.on_reactor_grid_slot_clicked)
		self.reactor_grid.signal_contents_changed.connect(self.on_reactor_grid_contents_changed)
		self.reactor_grid.signal_grid_resized.connect(self.on_reactor_grid_resized)
		self.reactor_grid.signal_selection_changed.connect(self.on_reactor_grid_selection_changed)

		self.toolbox_left = ToolboxLeft(self)
		self.toolbox_left.signal_tool_type_selected.connect(self.on_tool_type_selected)

		self.toolbox_top = ToolboxTop(self)
		self.toolbox_top.signal_simulate.connect(self.on_do_simulate)
		self.toolbox_top.signal_autorun_toggled.connect(self.on_autorun_toggled)
		self.toolbox_top.signal_penalty_stop_toggled.connect(self.on_penalty_stop_toggled)
		self.toolbox_top.signal_show_HUt_Lt_toggled.connect(self.on_show_HUt_Lt_toggled)
		self.toolbox_top.signal_autoexpand_toggled.connect(self.on_autoexpand_toggled)
		self.toolbox_top.signal_shrink_to_fit.connect(self.on_shrink_to_fit)
		self.toolbox_top.signal_increment_bottom.connect(self.on_increment_bottom)
		self.toolbox_top.signal_increment_top.connect(self.on_increment_top)
		self.toolbox_top.signal_increment_left.connect(self.on_increment_left)
		self.toolbox_top.signal_increment_right.connect(self.on_increment_right)
		self.toolbox_top.signal_decrement_bottom.connect(self.on_decrement_bottom)
		self.toolbox_top.signal_decrement_top.connect(self.on_decrement_top)
		self.toolbox_top.signal_decrement_left.connect(self.on_decrement_left)
		self.toolbox_top.signal_decrement_right.connect(self.on_decrement_right)
		
		self.info_panel = InfoPanel(self)
		self.info_panel.signal_plot_time_selection_shanged.connect(self.on_plot_time_selection_changed)

		# Layout
		self.grid_layout = QGridLayout(self)
		self.grid_layout.addWidget(self.toolbox_left, 0, 0, 2, 1)
		self.grid_layout.addWidget(self.toolbox_top, 0, 1)
		self.grid_layout.addWidget(self.reactor_grid, 1, 1)
		self.grid_layout.addWidget(self.info_panel, 0, 2, 2, 1)
		
		self.grid_layout.setColumnStretch(1, 1)
		self.grid_layout.setRowStretch(1, 1)

		# Simulation object
		self.simulation = Simulation(self.info_panel) # Simulation posts data to info panel and reactor grid

		# Initial state
		self.save_count = 0
		self.sim_count = 0
		self.save_state = True # True, so you can open/exit without extra prompt
		self.sim_state = False
		self.autorun_state = False
		self.prevsim_autorun_timeout = False

		settings = Settings()
		value = settings.get_bool("AutoExpand")
		self.toolbox_top.set_checkbox_autoexpand(value)
		if not value:
			self.on_autoexpand_toggled(False)
		value = settings.get_bool("ShowHUtLt")
		self.toolbox_top.set_checkbox_show_HUt_Lt(value)
		if not value:
			self.on_show_HUt_Lt_toggled(False)
		value = settings.get_bool("PenaltyStop")
		self.toolbox_top.set_checkbox_penalty_stop(value)
		if not value:
			self.on_penalty_stop_toggled(False)
		value = settings.get_bool("AutoRun")
		self.toolbox_top.set_checkbox_autorun(value)
		if not value:
			self.on_autorun_toggled(False)

		self.set_project_name("Unsaved Project")
		self.reactor_grid.clear_grid(Settings().get_int("InitW"), Settings().get_int("InitH"))
		self.check_simulation_autorun()


	def on_increment_left(self):
		self.reactor_grid.size_increment_left()
		self.historian.register_events()
		self.check_simulation_autorun()


	def on_increment_right(self):
		self.reactor_grid.size_increment_right()
		self.historian.register_events()
		self.check_simulation_autorun()


	def on_increment_top(self):
		self.reactor_grid.size_increment_top()
		self.historian.register_events()
		self.check_simulation_autorun()


	def on_increment_bottom(self):
		self.reactor_grid.size_increment_bottom()
		self.historian.register_events()
		self.check_simulation_autorun()


	def on_decrement_left(self):
		if self.reactor_grid.n_col_end - self.reactor_grid.n_col_begin > 1:
			self.reactor_grid.size_decrement_left()
			self.historian.register_events()
			self.check_simulation_autorun()


	def on_decrement_right(self):
		if self.reactor_grid.n_col_end - self.reactor_grid.n_col_begin > 1:
			self.reactor_grid.size_decrement_right()
			self.historian.register_events()
			self.check_simulation_autorun()


	def on_decrement_top(self):
		if self.reactor_grid.n_row_end - self.reactor_grid.n_row_begin > 1:
			self.reactor_grid.size_decrement_top()
			self.historian.register_events()
			self.check_simulation_autorun()


	def on_decrement_bottom(self):
		if self.reactor_grid.n_row_end - self.reactor_grid.n_row_begin > 1:
			self.reactor_grid.size_decrement_bottom()
			self.historian.register_events()
			self.check_simulation_autorun()


	def on_shrink_to_fit(self):
		self.reactor_grid.shrink_to_fit()
		self.revalidate_simulation_state(self.sim_count, True)
		self.historian.register_events()


	def restorePreviousSize(self):
		posx = Settings().get_int("PosX")
		posy = Settings().get_int("PosY")
		sizex = Settings().get_int("SizeX")
		sizey = Settings().get_int("SizeY")
		if sizex > 0 and sizey > 0:
			self.main_window.resize(sizex, sizey)
		self.main_window.move(posx, posy)
		if Settings().get_bool("IsMaximized"):
			self.main_window.showMaximized()


	def on_close_event(self, event):
		if not self.try_save_first():
			event.ignore()
			return
		pos_data = self.main_window.pos()
		size_data = self.main_window.size()
		is_max = self.main_window.isMaximized()
		Settings().set("IsMaximized", is_max)
		if not is_max:
			Settings().setList([ ("PosX", pos_data.x()), ("PosY", pos_data.y()), ("SizeX", size_data.width()), ("SizeY", size_data.height()) ])
		event.accept()


	def on_do_new_state(self):
		if not self.try_save_first():
			return
		self.menu_bar.open_dialog_new_state()


	def on_dialog_new_accepted(self, width, height):
		self.reactor_grid.deselect()
		self.set_project_name("Unsaved Project")
		self.invalidate_simulation_state(False)
		self.simulation.clear_simulation()
		self.reactor_grid.clear_grid(height, width)
		self.historian.clear()
		self.validate_save_state()
		self.check_simulation_autorun()


	def on_do_load_state(self):
		if not self.try_save_first():
			return
		data = self.menu_bar.load_state()
		if data is None:
			qmbox = QMessageBox()
			qmbox.setIcon(QMessageBox.Warning)
			qmbox.setText("Failed to read data from selected file.")
			qmbox.setWindowTitle("Warning")
			qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
			x = qmbox.exec()
			return
		if self.reactor_grid.check_grid_data(data[1]) == False:
			qmbox = QMessageBox()
			qmbox.setIcon(QMessageBox.Warning)
			qmbox.setText("Selected json file is not a valid save file.")
			qmbox.setWindowTitle("Warning")
			qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
			x = qmbox.exec()
			return
		self.reactor_grid.deselect()
		self.validate_save_state()
		self.set_project_name(data[0])
		self.invalidate_simulation_state(False)
		self.simulation.clear_simulation()
		self.reactor_grid.set_grid_data(data[1])
		self.historian.clear()
		self.check_simulation_autorun()


	def on_do_save_state(self):
		if not self.save_state:
			if self.project_name == "Unsaved Project":
				self.on_do_save_state_as()
			else:
				self.save()


	def on_do_save_state_as(self):
		file_name = self.menu_bar.prompt_save_file_name()
		if file_name is None:
			qmbox = QMessageBox()
			qmbox.setIcon(QMessageBox.Warning)
			qmbox.setText("No save name selected, project will not be saved.")
			qmbox.setWindowTitle("Warning")
			qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
			x = qmbox.exec()
			return
		self.set_project_name(file_name)
		self.save()


	def on_do_quit(self):
		if not self.try_save_first():
			return
		QApplication.instance().quit()


	def on_do_undo(self):
		self.historian.undo()
		self.check_simulation_autorun()


	def on_do_redo(self):
		self.historian.redo()
		self.check_simulation_autorun()


	def on_do_options(self):
		self.menu_bar.options_window()


	def on_do_readme(self):
		self.menu_bar.readme_window()


	def on_do_about(self):
		self.menu_bar.about_window()


	def on_calculate_material_costs(self): 
		self.on_do_simulate()
		self.menu_bar.materials_window(self.reactor_grid.find_material_cost(self.simulation))


	def on_reactor_grid_slot_clicked(self, target):
		self.reactor_grid.tool_click(target, self.toolbox_left.get_current_tool())
		self.historian.register_events()
		self.check_simulation_autorun()
		

	def on_reactor_grid_contents_changed(self, history_commit):
		if history_commit is not None:
			self.historian.commit_event(history_commit[0], history_commit[1])
			self.invalidate_save_state(True)
			self.invalidate_simulation_state(True)


	def on_reactor_grid_resized(self, history_commit, width, height):
		if history_commit is not None:
			self.historian.commit_event(history_commit[0], history_commit[1])
			self.invalidate_save_state(True)
		self.toolbox_top.set_size_label(width, height)


	def on_reactor_grid_selection_changed(self, target): 
		if target is not None and target.slot.rod_name != "None":
			self.info_panel.set_selection_stats(target.block.coolant_name, target.slot.rod_name)
		else:
			self.info_panel.reset_selection_stats()
		if self.sim_state:
			if target is not None:
				self.simulation.post_selection_data(self.info_panel.get_plot_selected_time(), target)
			else:
				self.simulation.recall_selection_data()


	def on_tool_type_selected(self):
		self.reactor_grid.deselect()


	def on_do_simulate(self):
		if not self.sim_state or self.prevsim_autorun_timeout:
			self.simulate()


	def on_autorun_toggled(self, checked):
		self.autorun_state = checked
		Settings().set("AutoRun", checked)
		if checked and not self.sim_state:
			self.simulate(True)


	def on_penalty_stop_toggled(self, checked):
		self.simulation.set_stop_on_overmax(checked)
		Settings().set("PenaltyStop", checked)
		if self.autorun_state:
			self.simulate(True)


	def on_show_HUt_Lt_toggled(self, checked):
		ReactorGridBlock.show_HUt_Lt = checked
		Settings().set("ShowHUtLt", checked)
		if self.sim_state:
			time_index = self.info_panel.get_plot_selected_time()
			self.simulation.post_sim_data(time_index)
			target = self.reactor_grid.get_grid_selection()
			if target is not None:
				self.simulation.post_selection_data(time_index, target)


	def on_autoexpand_toggled(self, checked):
		self.reactor_grid.set_autoexpand(checked)
		Settings().set("AutoExpand", checked)


	def on_plot_time_selection_changed(self, index):
		if self.sim_state:
			self.simulation.post_sim_data(index)
			target = self.reactor_grid.get_grid_selection()
			if target is not None:
				self.simulation.post_selection_data(index, target)


	def update_main_window_title(self):
		title = "GT6 Fission Reactor Simulator - " + self.project_name
		if not self.save_state:
			title += "*"
		self.main_window.setWindowTitle(title)
				

	def set_project_name(self, project_name):
		self.project_name = project_name
		self.update_main_window_title()


	def try_save_first(self):
		if not self.save_state:
			result = self.menu_bar.ask_to_save_first()
			if result == DialogResult.Yes:
				self.on_do_save_state()
				if not self.save_state:
					return False
			elif result == DialogResult.Cancel:
				return False
		return True


	def save(self):
		if not self.menu_bar.save_state(self.project_name, self.reactor_grid.get_grid_data()):
			qmbox = QMessageBox()
			qmbox.setIcon(QMessageBox.Warning)
			qmbox.setText("Failed to save data to selected file.")
			qmbox.setWindowTitle("Warning")
			qmbox.setStandardButtons(QMessageBox.StandardButtons.Ok)
			x = qmbox.exec()
			return
		self.save_count += 1
		self.validate_save_state()
		self.historian.insert_commit((self.invalidate_save_state, ()), (self.revalidate_save_state, (self.save_count,)))
		

	def validate_save_state(self):
		if not self.save_state:
			self.save_state = True
			self.update_main_window_title()


	def invalidate_save_state(self, mark_in_history):
		if self.save_state:
			self.save_state = False
			self.update_main_window_title()
			if mark_in_history:
				self.historian.commit_event((self.revalidate_save_state, (self.save_count,)), (self.invalidate_save_state, ()))


	def revalidate_save_state(self, save_id, mark_in_history):
		if save_id == self.save_count:
			self.save_state = True
			self.update_main_window_title()
			

	def simulate(self, autorun=False):
		if not autorun and self.prevsim_autorun_timeout and self.sim_state:
			self.simulation.reason = ""
		else:
			self.simulation.clear_simulation()
			self.simulation.construct_simulation(self.reactor_grid.get_grid_data())
		temp = self.simulation.run_simulation(autorun)
		if autorun:
			self.prevsim_autorun_timeout = not temp
		else:
			self.prevsim_autorun_timeout = False
		self.sim_count = self.sim_count + 1
		self.simulation.post_plot_data()
		self.validate_simulation_state()
		self.historian.insert_commit((self.invalidate_simulation_state, ()), (self.revalidate_simulation_state, (self.sim_count,)))


	def validate_simulation_state(self):
		if not self.sim_state:
			self.sim_state = True
			time_index = self.info_panel.get_plot_selected_time()
			self.simulation.post_sim_data(time_index)
			target = self.reactor_grid.get_grid_selection()
			if target is not None:
				self.simulation.post_selection_data(time_index, target)


	def invalidate_simulation_state(self, mark_in_history):
		self.prevsim_autorun_timeout = False
		if self.sim_state:
			self.sim_state = False
			self.simulation.recall_sim_data()
			self.simulation.recall_selection_data()
			self.info_panel.hide_plot_data()
			if mark_in_history:
				self.historian.commit_event((self.revalidate_simulation_state, (self.sim_count,)), (self.invalidate_simulation_state, ()))


	def revalidate_simulation_state(self, sim_id, mark_in_history):
		if sim_id == self.sim_count:
			self.sim_state = True
			time_index = self.info_panel.get_plot_selected_time()
			self.simulation.post_sim_data(time_index)
			target = self.reactor_grid.get_grid_selection()
			if target is not None:
				self.simulation.post_selection_data(time_index, target)
			self.info_panel.show_plot_data()


	def check_simulation_autorun(self):
		if not self.sim_state and self.autorun_state:
			self.simulate(True)