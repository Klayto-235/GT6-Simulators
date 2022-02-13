from collections import namedtuple, deque
from itertools import islice
from enum import Enum
from PyQt6.QtGui import QIcon, QAction, QColor, QResizeEvent, QSurfaceFormat
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsItem, QGraphicsScene, QScroller, QScrollerProperties, QSizePolicy
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QEvent, QPoint, QPointF, QTimeLine, QRect
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from Assets import Assets
from Settings import Settings
from Toolbox import ToolType, ToolModifier
from ReactorGridBlock import ReactorGridBlock, ReactorGridButton, ReactorGridBlockEncoder


class ReactorGridEncoder(ReactorGridBlockEncoder):
	pass


GridTarget = namedtuple("GridTarget", ["block", "slot"])


class FillPredicate(Enum):
	Default = 0
	Empty = 1
	ShallowEmpty = 2
	DeepEmpty = 3
	Same = 4
	ShallowSame = 5
	DeepSame = 6
	SameSize = 7


class ZoomingGraphicsView(QGraphicsView):
	def __init__(self, scene, parent=None):
		super().__init__(scene, parent)

		self.currentZoom = 1.0

		self.minzoom = Settings().get_float("MinZoom")
		self.maxzoom = Settings().get_float("MaxZoom")

		self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

		self.zooming = False

		self.num_scheduled_callings = 0

		self.mousePos = QPoint(0, 0)

		self.timeline = QTimeLine(150, self)
		self.timeline.setUpdateInterval(5)
		self.timeline.valueChanged.connect(self.zoom_event)
		self.timeline.finished.connect(self.zooming_finished)

		self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)


	def clear_timeline(self):
		self.timeline.setCurrentTime(0)


	def zoom_event(self):
		testzoomFactor = 1.0 + self.num_scheduled_callings / 100.0

		if self.currentZoom * testzoomFactor > self.maxzoom:
			zoomFactor = self.maxzoom / self.currentZoom
		elif self.currentZoom * testzoomFactor < self.minzoom:
			zoomFactor = self.minzoom / self.currentZoom
		else:
			zoomFactor = testzoomFactor

		if zoomFactor > 1.0:
			refPoint = self.mousePos
		else:
			refPoint = self.rect().center()

		if abs(zoomFactor - 1.0) < 0.0000001:
			return

		self.currentZoom *= zoomFactor

		before = self.mapToScene(refPoint)

		self.scale(zoomFactor, zoomFactor)

		after = self.mapToScene(refPoint)
		delta = after - before
		self.translate(delta.x(), delta.y())

		self.parent().update_scene()


	def wheelEvent(self, event): 
		if not Settings().get_bool("EnableZoom"):
			return

		self.minzoom = Settings().get_float("MinZoom")
		self.maxzoom = Settings().get_float("MaxZoom")

		if Settings().get_bool("SmoothZoom"):
			numDegrees = event.angleDelta().y() // 8
			numSteps = numDegrees // 15

			if self.num_scheduled_callings * numSteps < 0:
				self.num_scheduled_callings = numSteps
			else:
				self.num_scheduled_callings += numSteps

			self.mousePos = event.position().toPoint()

			if self.zooming:
				self.timeline.setCurrentTime(0)
			else:
				self.zooming = True
				self.timeline.start()
		else:
			if event.angleDelta().y() < 0:
				self.num_scheduled_callings = -20
			else:
				self.num_scheduled_callings = 20

			self.mousePos = event.position().toPoint()

			self.zoom_event()
			self.num_scheduled_callings = 0

	def zooming_finished(self):
		self.clear_timeline()
		self.zooming = False
		if (self.num_scheduled_callings > 0):
			self.num_scheduled_callings -= 1
		else:
			self.num_scheduled_callings += 1


	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			self.orig_x = event.position().x()
			self.orig_y = event.position().y()
		super().mousePressEvent(event)


	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.RightButton:
			oldp = self.mapToScene(self.orig_x, self.orig_y);
			newp = self.mapToScene(event.position().toPoint());
			delta_x = newp.x() - oldp.x()
			delta_y = newp.y() - oldp.y()

			self.translate(delta_x, delta_y);

			self.orig_x = event.position().x()
			self.orig_y = event.position().y()
		super().mouseMoveEvent(event)


	def resizeEvent(self, event):
		self.parent().update_scene()


class ReactorGrid(QWidget):
	signal_clicked = pyqtSignal(object)
	signal_grid_resized = pyqtSignal(object, int, int)
	signal_contents_changed = pyqtSignal(object)
	signal_selection_changed = pyqtSignal(object)

	def __init__(self, parent):
		super().__init__(parent)
		
		self.scene = QGraphicsScene(self)
		self.view = ZoomingGraphicsView(self.scene, self)
		self.view.setBackgroundBrush(QColor(248, 248, 248, 255))
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

		#TODO: Implement OpenGL rendering

		# initial state
		self.current_selection = None
		self.grid = deque()
		self.autoexpand_state = True
		self.n_row = 0
		self.n_col = 0
		self.n_row_begin = 0
		self.n_col_begin = 0
		self.n_row_end = 0
		self.n_col_end = 0
		self.n_row_total = 0
		self.n_col_total = 0
		self.row_offset = 0
		self.col_offset = 0
		self.resize_left = False
		self.resize_top = False
		self.resize_right = False
		self.resize_bottom = False


	def resizeEvent(self, event):
		self.view.setGeometry(0, 0, event.size().width(), event.size().height())


	def on_click(self, block, button):
		self.signal_clicked.emit(GridTarget(block, button))


	def get_grid_data(self):
		return [list(islice(self.grid[i], self.n_col_begin, self.n_col_end)) for i in range(self.n_row_begin, self.n_row_end)]


	def check_grid_data(self, data):
		if not (type(data) is list):
			return False

		n_row = len(data)
		if n_row <= 0:
			return False
		if not (type(data[0]) is list):
			return False
		n_col = len(data[0])
		if not (type(n_col) is int):
			return False
		if n_col <= 0: 
			return False

		for i in range(n_row):
			if not (type(data[i]) is list):
				return False
			if len(data[i]) != n_col:
				return False
			for j in range(n_col):
				if not (type(data[i][j]) is list):
					return False
				if len(data[i][j]) != 3:
					return False
				if not (type(data[i][j][1]) is str):
					return False
				if not (data[i][j][1] in Assets().coolant):
					return False
				if not (type(data[i][j][0]) is bool):
					return False
				if data[i][j][0]:
					if len(data[i][j][2]) != 4:
						return False
				else:
					if len(data[i][j][2]) != 1:
						return False
				if not (type(data[i][j][2]) is list):
					return False
				for rodstr in data[i][j][2]:
					if not (type(rodstr) is str):
						return False
					if not (rodstr in Assets().rod):
						return False
		return True


	def set_grid_data(self, data):
		n_row = len(data)
		n_col = len(data[0])
		self.clear_grid(n_row, n_col)

		for i in range(n_row):
			for j in range(n_col):
				block = self.grid[i + self.n_row_begin][j + self.n_col_begin]
				block.set_coolant(data[i][j][1])
				if data[i][j][0]:
					block.toggle_shape()
				buttons = block.get_active_buttons()
				for k in range(len(buttons)):
					buttons[k].set_rod(data[i][j][2][k])

		self.no_resize()


	def clear_grid(self, n_row, n_col): 
		while self.n_row > n_row:
			self.size_decrement_bottom(False)
		while self.n_col > n_col:
			self.size_decrement_right(False)

		for i in range(self.n_row_begin, self.n_row_end):
			for j in range(self.n_col_begin, self.n_col_end):
				self.reset(GridTarget(self.grid[i][j], None), False)

		while self.n_row < n_row:
			if self.n_row_begin > 0:
				self.size_increment_top(False)
			else:
				self.size_increment_bottom(False)
		while self.n_col < n_col:
			if self.n_col_begin > 0:
				self.size_increment_left(False)
			else:
				self.size_increment_right(False)
		
		viewlt = QPoint(0, 0)
		maplt = self.view.mapToScene(viewlt)
		gridlt = QPointF(self.grid[self.n_row_begin][self.n_col_begin].x - 1, self.grid[self.n_row_begin][self.n_col_begin].y - 1)
		deltax = maplt.x() - gridlt.x()
		deltay = maplt.y() - gridlt.y()
		self.view.translate(deltax, deltay)

		self.signal_grid_resized.emit(None, self.n_col, self.n_row)

		self.no_resize()


	def check_auto_resize(self, block):
		if self.autoexpand_state:
			y,x = block.get_position()
			row = y - self.row_offset
			col = x - self.col_offset
			if row == self.n_row_begin:
				self.resize_top = True
			if row == self.n_row_end - 1:
				self.resize_bottom = True
			if col == self.n_col_begin:
				self.resize_left = True
			if col == self.n_col_end - 1:
				self.resize_right = True


	def auto_resize(self):
		if self.resize_top:
			self.size_increment_top()
			self.resize_top = False
		if self.resize_left:
			self.size_increment_left()
			self.resize_left = False
		if self.resize_right:
			self.size_increment_right()
			self.resize_right = False
		if self.resize_bottom:
			self.size_increment_bottom()
			self.resize_bottom = False


	def no_resize(self):
		self.resize_top = False
		self.resize_left = False
		self.resize_right = False
		self.resize_bottom = False


	def shrink_to_fit(self):
		#left
		while (self.n_col > 1):
			empty = True
			for i in range(self.n_row_begin, self.n_row_end):
				if not self.grid[i][self.n_col_begin].is_deep_empty():
					empty = False
					break
			if empty:
				self.size_decrement_left()
			else:
				break
		#right
		while (self.n_col > 1):
			empty = True
			for i in range(self.n_row_begin, self.n_row_end):
				if not self.grid[i][self.n_col_end - 1].is_deep_empty():
					empty = False
					break
			if empty:
				self.size_decrement_right()
			else:
				break
		#top
		while (self.n_row > 1):
			empty = True
			for i in range(self.n_col_begin, self.n_col_end):
				if not self.grid[self.n_row_begin][i].is_deep_empty():
					empty = False
					break
			if empty:
				self.size_decrement_top()
			else:
				break
		#bottom
		while (self.n_row > 1):
			empty = True
			for i in range(self.n_col_begin, self.n_col_end):
				if not self.grid[self.n_row_end - 1][i].is_deep_empty():
					empty = False
					break
			if empty:
				self.size_decrement_bottom()
			else:
				break
		self.no_resize()


	def size_increment_left(self, mark_in_history=True): 
		if self.n_col_begin > 0:
			self.n_col_begin -= 1
			for i in range(self.n_row_begin, self.n_row_end):
				self.scene.addItem(self.grid[i][self.n_col_begin])
		else:
			self.col_offset -= 1
			for i in range(self.n_row_total):
				block = ReactorGridBlock(i + self.row_offset, self.col_offset)
				self.grid[i].appendleft(block)
				if i >= self.n_row_begin and i < self.n_row_end:
					self.scene.addItem(block)
			self.n_col_end += 1
			self.n_col_total += 1
		self.n_col += 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_decrement_left, ()), (self.size_increment_left, ())) if mark_in_history else None, self.n_col, self.n_row)
		

	def size_increment_right(self, mark_in_history=True): 
		if self.n_col_end < self.n_col_total:
			for i in range(self.n_row_begin, self.n_row_end):
				self.scene.addItem(self.grid[i][self.n_col_end])
			self.n_col_end += 1
		else:
			for i in range(self.n_row_total):
				block = ReactorGridBlock(i + self.row_offset, self.col_offset + self.n_col_end)
				self.grid[i].append(block)
				if i >= self.n_row_begin and i < self.n_row_end:
					self.scene.addItem(block)
			self.n_col_end += 1
			self.n_col_total += 1
		self.n_col += 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_decrement_right, ()), (self.size_increment_right, ())) if mark_in_history else None, self.n_col, self.n_row)
		

	def size_increment_top(self, mark_in_history=True): 
		if self.n_row_begin > 0:
			self.n_row_begin -= 1
			for j in range(self.n_col_begin, self.n_col_end):
				self.scene.addItem(self.grid[self.n_row_begin][j])
		else:
			self.row_offset -= 1
			row = deque()
			for j in range(self.n_col_total):
				block = ReactorGridBlock(self.row_offset, j + self.col_offset)
				row.append(block)
				if j >= self.n_col_begin and j < self.n_col_end:
					self.scene.addItem(block)
			self.grid.appendleft(row)
			self.n_row_total += 1
			self.n_row_end += 1
		self.n_row += 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_decrement_top, ()), (self.size_increment_top, ())) if mark_in_history else None, self.n_col, self.n_row)
		

	def size_increment_bottom(self, mark_in_history=True): 
		if self.n_row_end < self.n_row_total:
			for j in range(self.n_col_begin, self.n_col_end):
				self.scene.addItem(self.grid[self.n_row_end][j])
			self.n_row_end += 1
		else:
			row = deque()
			for j in range(self.n_col_total):
				block = ReactorGridBlock(self.row_offset + self.n_row_end, j + self.col_offset)
				row.append(block)
				if j >= self.n_col_begin and j < self.n_col_end:
					self.scene.addItem(block)
			self.grid.append(row)
			self.n_row_total += 1
			self.n_row_end += 1
		self.n_row += 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_decrement_bottom, ()), (self.size_increment_bottom, ())) if mark_in_history else None, self.n_col, self.n_row)
		

	def size_decrement_left(self, mark_in_history=True): 
		if self.n_col == 0:
			return
		for i in range(self.n_row_begin, self.n_row_end):
			self.reset(GridTarget(self.grid[i][self.n_col_begin], None), mark_in_history)
			self.scene.removeItem(self.grid[i][self.n_col_begin])
		self.n_col_begin += 1
		self.n_col -= 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_increment_left, ()), (self.size_decrement_left, ())) if mark_in_history else None, self.n_col, self.n_row)


	def size_decrement_right(self, mark_in_history=True):
		if self.n_col == 0:
			return
		self.n_col_end -= 1
		for i in range(self.n_row_begin, self.n_row_end):
			self.reset(GridTarget(self.grid[i][self.n_col_end], None), mark_in_history)
			self.scene.removeItem(self.grid[i][self.n_col_end])
		self.n_col -= 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_increment_right, ()), (self.size_decrement_right, ())) if mark_in_history else None, self.n_col, self.n_row)


	def size_decrement_top(self, mark_in_history=True):
		if self.n_row == 0:
			return
		for j in range(self.n_col_begin, self.n_col_end):
			self.reset(GridTarget(self.grid[self.n_row_begin][j], None), mark_in_history)
			self.scene.removeItem(self.grid[self.n_row_begin][j])
		self.n_row_begin += 1
		self.n_row -= 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_increment_top, ()), (self.size_decrement_top, ())) if mark_in_history else None, self.n_col, self.n_row)


	def size_decrement_bottom(self, mark_in_history=True): 
		if self.n_row == 0:
			return
		self.n_row_end -= 1
		for j in range(self.n_col_begin, self.n_col_end):
			self.reset(GridTarget(self.grid[self.n_row_end][j], None), mark_in_history)
			self.scene.removeItem(self.grid[self.n_row_end][j])
		self.n_row -= 1
		self.update_scene()
		self.signal_grid_resized.emit(((self.size_increment_bottom, ()), (self.size_decrement_bottom, ())) if mark_in_history else None, self.n_col, self.n_row)


	def update_scene(self):
		if (self.n_col == 0 or self.n_row == 0):
			self.scene.setSceneRect(0, 0, 1, 1)
		else:
			view_size = self.view.size()
			mapped1 = self.view.mapToScene(QPoint(0, 0))
			mapped2 = self.view.mapToScene(QPoint(view_size.width(), view_size.height()))
			mw = mapped2.x() - mapped1.x()
			mh = mapped2.y() - mapped1.y()
			newX = (self.n_col_begin + self.col_offset) * 142 - 17 - mw / 2
			newY = (self.n_row_begin + self.row_offset) * 142 - 17 - mh / 2
			newW = 142 * self.n_col + mw + 34
			newH = 142 * self.n_row + mh + 34
			before = self.view.mapToScene(QPoint(view_size.width() // 2, view_size.height() // 2))
			self.scene.setSceneRect(newX, newY, newW, newH)
			after = self.view.mapToScene(QPoint(view_size.width() // 2, view_size.height() // 2))
			delta = after - before
			self.view.translate(delta.x(), delta.y())


	def tool_click(self, target, tool):
		fill_predicate = FillPredicate.Default

		if (tool.type is ToolType.Rod):
			if tool.modifier == ToolModifier.FloodFill:
				fill_predicate = FillPredicate.ShallowSame
			self.apply_tool(tool.modifier, fill_predicate, target, True, self.set_rod, tool.name)

		elif (tool.type is ToolType.Coolant):
			if tool.modifier == ToolModifier.FloodFill:
				fill_predicate = FillPredicate.ShallowSame
			self.apply_tool(tool.modifier, fill_predicate, target, False, self.set_coolant, tool.name)

		elif (tool.type is ToolType.Shape):
			if (self.current_selection is not None and target.block is self.current_selection.block):
				self.deselect()
			fill_predicate = FillPredicate.SameSize
			self.apply_tool(tool.modifier, fill_predicate, target, False, self.toggle_shape)

		elif (tool.type is ToolType.Erase):
			if tool.modifier == ToolModifier.FloodFill:
				fill_predicate = FillPredicate.Same
			self.apply_tool(tool.modifier, fill_predicate, target, False, self.erase)

		elif (tool.type is ToolType.Reset):
			if tool.modifier == ToolModifier.FloodFill:
				fill_predicate = FillPredicate.Same
			self.apply_tool(tool.modifier, fill_predicate, target, False, self.reset)

		elif (tool.type is ToolType.Default):
			if (self.current_selection is not None and target.slot is self.current_selection.slot):
				self.deselect()
			else:
				if (self.current_selection is not None):
					self.deselect()
				self.select(target)

		self.auto_resize()


	def apply_tool(self, modifier, predicate, target, on_slots, func, *args):
		target_type = ReactorGridButton if on_slots else ReactorGridBlock
		if on_slots:
			target_copy = target.slot.logical_copy()
		else:
			target_copy = target.block.logical_copy()

		if predicate == FillPredicate.Empty:
			predicate_func = target_type.is_empty
		elif predicate == FillPredicate.ShallowEmpty:
			predicate_func = target_type.is_shallow_empty
		elif predicate == FillPredicate.DeepEmpty:
			predicate_func = target_type.is_deep_empty
		elif predicate == FillPredicate.Same:
			predicate_func = target_copy.is_same
		elif predicate == FillPredicate.ShallowSame:
			predicate_func = target_copy.is_shallow_same
		elif predicate == FillPredicate.DeepSame:
			predicate_func = target_copy.is_deep_same
		elif predicate == FillPredicate.SameSize:
			predicate_func = target_copy.is_same_size
		elif predicate == FillPredicate.Default:
			predicate_func = lambda target: True
			
		if modifier == ToolModifier.Fill:
			self.fill(predicate_func, target, on_slots, func, *args)
		elif modifier == ToolModifier.FloodFill:
			self.floodfill(predicate_func, target, on_slots, func, *args)
		elif modifier == ToolModifier.Default:
			func(target, *args)

		del target_copy


	def fill(self, predicate_func, target, on_slots, func, *args):
		for i in range(self.n_row_begin, self.n_row_end):
			for j in range(self.n_col_begin, self.n_col_end):
				block = self.grid[i][j]
				if (on_slots):
					for slot in block.get_active_buttons():
						if predicate_func(slot):
							func(GridTarget(block, slot), *args)
				elif predicate_func(block):
					func(GridTarget(block, None), *args)


	def floodfill(self, predicate_func, target, on_slots, func, *args): 
		if not predicate_func(target.slot if on_slots else target.block):
			return
		position = target.block.get_position()
		i = position[0] - self.row_offset
		j = position[1] - self.col_offset
		stack = []
		if not func(target, *args):
			return
		if on_slots:
			stack.append((i, j, target.slot))
			while len(stack) != 0:
				i, j, slot = stack.pop()
				block = self.grid[i][j]
				if block.is_small():
					ii, jj = slot.get_position()
					if ii == 0:
						if i > self.n_row_begin:
							top = self.grid[i - 1][j]
							if top.is_small():
								if jj == 0:
									if predicate_func(top.button_bottom_left):
										func(GridTarget(top, top.button_bottom_left), *args)
										stack.append((i - 1, j, top.button_bottom_left))
								elif predicate_func(top.button_bottom_right):
									func(GridTarget(top, top.button_bottom_right), *args)
									stack.append((i - 1, j, top.button_bottom_right))
							elif predicate_func(top.button_large):
								func(GridTarget(top, top.button_large), *args)
								stack.append((i - 1, j, top.button_large))
						if jj == 0:
							if predicate_func(block.button_bottom_left):
								func(GridTarget(block, block.button_bottom_left), *args)
								stack.append((i, j, block.button_bottom_left))
						elif predicate_func(block.button_bottom_right):
							func(GridTarget(block, block.button_bottom_right), *args)
							stack.append((i, j, block.button_bottom_right))
					else:
						if i + 1 < self.n_row_end:
							bottom = self.grid[i + 1][j]
							if bottom.is_small():
								if jj == 0:
									if predicate_func(bottom.button_top_left):
										func(GridTarget(bottom, bottom.button_top_left), *args)
										stack.append((i + 1, j, bottom.button_top_left))
								elif predicate_func(bottom.button_top_right):
									func(GridTarget(bottom, bottom.button_top_right), *args)
									stack.append((i + 1, j, bottom.button_top_right))
							elif predicate_func(bottom.button_large):
								func(GridTarget(bottom, bottom.button_large), *args)
								stack.append((i + 1, j, bottom.button_large))
						if jj == 0:
							if predicate_func(block.button_top_left):
								func(GridTarget(block, block.button_top_left), *args)
								stack.append((i, j, block.button_top_left))
						elif predicate_func(block.button_top_right):
							func(GridTarget(block, block.button_top_right), *args)
							stack.append((i, j, block.button_top_right))
					if jj == 0:
						if j > self.n_col_begin:
							left = self.grid[i][j - 1]
							if left.is_small():
								if ii == 0:
									if predicate_func(left.button_top_right):
										func(GridTarget(left, left.button_top_right), *args)
										stack.append((i, j - 1, left.button_top_right))
								elif predicate_func(left.button_bottom_right):
									func(GridTarget(left, left.button_bottom_right), *args)
									stack.append((i, j - 1, left.button_bottom_right))
							elif predicate_func(left.button_large):
								func(GridTarget(left, left.button_large), *args)
								stack.append((i, j - 1, left.button_large))
						if ii == 0:
							if predicate_func(block.button_top_right):
								func(GridTarget(block, block.button_top_right), *args)
								stack.append((i, j, block.button_top_right))
						elif predicate_func(block.button_bottom_right):
							func(GridTarget(block, block.button_bottom_right), *args)
							stack.append((i, j, block.button_bottom_right))
					else:
						if j + 1 < self.n_col_end:
							right = self.grid[i][j + 1]
							if right.is_small():
								if ii == 0:
									if predicate_func(right.button_top_left):
										func(GridTarget(right, right.button_top_left), *args)
										stack.append((i, j + 1, right.button_top_left))
								elif predicate_func(right.button_bottom_left):
									func(GridTarget(right, right.button_bottom_left), *args)
									stack.append((i, j + 1, right.button_bottom_left))
							elif predicate_func(right.button_large):
								func(GridTarget(right, right.button_large), *args)
								stack.append((i, j + 1, right.button_large))
						if ii == 0:
							if predicate_func(block.button_top_left):
								func(GridTarget(block, block.button_top_left), *args)
								stack.append((i, j, block.button_top_left))
						elif predicate_func(block.button_bottom_left):
							func(GridTarget(block, block.button_bottom_left), *args)
							stack.append((i, j, block.button_bottom_left))
				else:
					if i > self.n_row_begin:
						top = self.grid[i - 1][j]
						if top.is_small():
							if predicate_func(top.button_bottom_left):
								func(GridTarget(top, top.button_bottom_left), *args)
								stack.append((i - 1, j, top.button_bottom_left))
							if predicate_func(top.button_bottom_right):
								func(GridTarget(top, top.button_bottom_right), *args)
								stack.append((i - 1, j, top.button_bottom_right))
						elif predicate_func(top.button_large):
							func(GridTarget(top, top.button_large), *args)
							stack.append((i - 1, j, top.button_large))
					if i + 1 < self.n_row_end:
						bottom = self.grid[i + 1][j]
						if bottom.is_small():
							if predicate_func(bottom.button_top_left):
								func(GridTarget(bottom, bottom.button_top_left), *args)
								stack.append((i + 1, j, bottom.button_top_left))
							if predicate_func(bottom.button_top_right):
								func(GridTarget(bottom, bottom.button_top_right), *args)
								stack.append((i + 1, j, bottom.button_top_right))
						elif predicate_func(bottom.button_large):
							func(GridTarget(bottom, bottom.button_large), *args)
							stack.append((i + 1, j, bottom.button_large))
					if j > self.n_col_begin:
						left = self.grid[i][j - 1]
						if left.is_small():
							if predicate_func(left.button_bottom_right):
								func(GridTarget(left, left.button_bottom_right), *args)
								stack.append((i, j - 1, left.button_bottom_right))
							if predicate_func(left.button_top_right):
								func(GridTarget(left, left.button_top_right), *args)
								stack.append((i, j - 1, left.button_top_right))
						elif predicate_func(left.button_large):
							func(GridTarget(left, left.button_large), *args)
							stack.append((i, j - 1, left.button_large))
					if j + 1 < self.n_col_end:
						right = self.grid[i][j + 1]
						if right.is_small():
							if predicate_func(right.button_top_left):
								func(GridTarget(right, right.button_top_left), *args)
								stack.append((i, j + 1, right.button_top_left))
							if predicate_func(right.button_bottom_left):
								func(GridTarget(right, right.button_bottom_left), *args)
								stack.append((i, j + 1, right.button_bottom_left))
						elif predicate_func(right.button_large):
							func(GridTarget(right, right.button_large), *args)
							stack.append((i, j + 1, right.button_large))
		else:
			stack.append((i, j))
			while len(stack) != 0:
				i, j = stack.pop()
				if i > self.n_row_begin and predicate_func(self.grid[i - 1][j]):
					func(GridTarget(self.grid[i - 1][j], None), *args)
					stack.append((i - 1, j))
				if i + 1 < self.n_row_end and predicate_func(self.grid[i + 1][j]):
					func(GridTarget(self.grid[i + 1][j], None), *args)
					stack.append((i + 1, j))
				if j > self.n_col_begin and predicate_func(self.grid[i][j - 1]):
					func(GridTarget(self.grid[i][j - 1], None), *args)
					stack.append((i, j - 1))
				if j + 1 < self.n_col_end and predicate_func(self.grid[i][j + 1]):
					func(GridTarget(self.grid[i][j + 1], None), *args)
					stack.append((i, j + 1))


	def toggle_shape(self, target, mark_in_history=True):
		block = target.block
		for slot in block.get_active_buttons():
			self.set_rod(GridTarget(block, slot), "None")
		block.toggle_shape()
		if mark_in_history:
			self.signal_contents_changed.emit(((self.toggle_shape, (target, )), (self.toggle_shape, (target, ))))
			self.check_auto_resize(block)
		else:
			self.signal_contents_changed.emit(None)
		return True


	def set_rod(self, target, name, mark_in_history=True):
		old_rod_name = target.slot.set_rod(name)
		if old_rod_name is not None:
			if mark_in_history:
				self.signal_contents_changed.emit(((self.set_rod, (target, old_rod_name)), (self.set_rod, (target, name))))
				self.check_auto_resize(target.block)
			else:
				self.signal_contents_changed.emit(None)
			return True


	def set_coolant(self, target, name, mark_in_history=True):
		old_coolant_name = target.block.set_coolant(name)
		if old_coolant_name is not None:
			if mark_in_history:
				self.signal_contents_changed.emit(((self.set_coolant, (target, old_coolant_name)), (self.set_coolant, (target, name))))
				self.check_auto_resize(target.block)
			else:
				self.signal_contents_changed.emit(None)
			return True


	def erase(self, target, mark_in_history=True):
		block = target.block
		changed = self.set_coolant(target, "None", mark_in_history)
		for slot in block.get_active_buttons():
			if self.set_rod(GridTarget(block, slot), "None", mark_in_history):
				changed = True
		return changed


	def reset(self, target, mark_in_history=True):
		changed = self.erase(target, mark_in_history)
		if target.block.is_small():
			self.toggle_shape(target, mark_in_history)
			changed = True
		return changed


	def select(self, target):
		self.current_selection = target
		target.slot.set_selected(True)
		self.signal_selection_changed.emit(self.current_selection)


	def deselect(self):
		if self.current_selection is not None:
			self.current_selection.slot.set_selected(False)
			self.current_selection = None
			self.signal_selection_changed.emit(self.current_selection)


	def get_grid_selection(self):
		return self.current_selection


	def set_autoexpand(self, state):
		self.autoexpand_state = state
		

	def find_material_cost(self, sim_ref):
		result = {}
		for i in range(len(self.grid)):
			row = self.grid[i]
			for j in range(len(row)):
				block = row[j]
				if not block.is_deep_empty():
					if block.is_small():
						result["Nuclear Reactor Core (2x2)"] = result.get("Nuclear Reactor Core (2x2)", 0) + 1
					else:
						result["Nuclear Reactor Core (1x1)"] = result.get("Nuclear Reactor Core (1x1)", 0) + 1
					burns_fuel = False
					for button in block.get_active_buttons():
						if button.rod_name != "None":
							result[button.rod_name] = result.get(button.rod_name, 0) + 1
							if button.rod_name != "Ref" and button.rod_name != "Mod":
								burns_fuel = True
					if burns_fuel and block.coolant_name == "Th":
						result["Th coolant"] = result.get("Th coolant", 0) + sim_ref.cell_data[sim_ref.cell_dict[(i, j)]].results.totalL
		return result