from json import JSONEncoder
from PyQt6.QtGui import QIcon, QResizeEvent, QColor, QPainter, QBrush, QPen, QFont
from PyQt6.QtWidgets import QGridLayout, QWidget, QSizePolicy, QHBoxLayout, QGraphicsSimpleTextItem, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QRect

from Assets import Assets
from Settings import Settings


class ReactorGridBlockEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ReactorGridBlock):
			data = [ obj.shape_small, obj.coolant_name, [button.rod_name for button in obj.get_active_buttons()] ]
			return data
		return super().default(obj)


class AARRectItem(QGraphicsRectItem):
	def __init__(self, x, y, w, h, parent):
		super().__init__(x, y, w, h, parent)

		self.enable_aa = Settings().get_bool("Antialiasing")


	def paint(self, painter, opts, widget=None):
		painter.setPen(self.pen())
		if self.enable_aa:
			painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painter.drawRoundedRect(self.rect(), 1, 1)


class ReactorGridButton(QGraphicsRectItem):
	def __init__(self, x, y, w, h, i, j, parent=None):
		x -= 0.05
		y -= 0.05
		w += 0.1
		h += 0.1
		super().__init__(x, y, w, h, parent) 

		self.enable_aa = Settings().get_bool("Antialiasing")

		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.i = i
		self.j = j
		if self.w > 100:
			self.tsz = 30
			self.ofs = 30
		else:
			self.tsz = 18
			self.ofs = 22
		self.setPen(QPen(Qt.PenStyle.NoPen))
		
		self.progress_bar_green = QGraphicsRectItem(x, y + h - 11, w, 11, self)
		self.progress_bar_green.setBrush(QColor(210, 255, 210, 255))
		self.progress_bar_green.setPen(QPen(Qt.PenStyle.NoPen))
		self.progress_bar_red = QGraphicsRectItem(x + w, y + h - 11, 0, 11, self)
		self.progress_bar_red.setBrush(QColor(255, 210, 210, 255))
		self.progress_bar_red.setPen(QPen(Qt.PenStyle.NoPen))
		self.rod_pixmap = QGraphicsPixmapItem(self)
		self.rod_pixmap.setPos(self.x + self.w / 2 - self.tsz / 2, self.y + self.h / 2 - self.tsz / 2)
		self.line = AARRectItem(x, y, w, h, self)
		self.line.setPen(QPen(QColor(160, 160, 160, 255), 1.2))

		self.labels = [QGraphicsSimpleTextItem(self) for i in range(7)]
		font = self.labels[0].font()
		font.setPixelSize(11) # point size 8
		if not self.enable_aa:
			font.setStyleStrategy(QFont.NoAntialias)
		for label in self.labels:
			label.setFont(font)
		
		self.rod_name = None
		self.set_rod("None")
		self.overmax = False
		self.reset_durability()
		self.reset_neutron_count()

		self.selected = False
		self.hovered = False
		self.setAcceptHoverEvents(True)
		self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)


	def get_position(self):
		return (self.i, self.j)


	def mousePressEvent(self, event):
		self.parentItem().on_click(self)


	def hoverEnterEvent(self, event):
		self.hovered = True
		if not self.selected:
			self.line.setPen(QPen(QColor(155, 170, 212, 255), 1.2))


	def hoverLeaveEvent(self, event):
		self.hovered = False
		if not self.selected:
			self.line.setPen(QPen(QColor(160, 160, 160, 255), 1.2))


	def set_selected(self, val):
		self.selected = val
		if self.selected:
			self.line.setPen(QPen(QColor(77, 108, 191, 255), 1.5))
		else:
			if self.hovered:
				self.line.setPen(QPen(QColor(155, 170, 212, 255), 1.2))
			else:
				self.line.setPen(QPen(QColor(160, 160, 160, 255), 1.2))

		
	def logical_copy(self, parent=None):
		obj = ReactorGridButton(self.x, self.y, self.w, self.h, self.i, self.j, parent)
		obj.rod_name = self.rod_name
		return obj
		

	def is_empty(self):
		return self.rod_name == "None"


	def is_full(self):
		return not self.is_empty()
		
	
	def is_shallow_empty(self):
		return self.rod_name == "None"
	
	
	def is_deep_empty(self):
		return False


	def is_same(self, other):
		return self.rod_name == other.rod_name


	def is_shallow_same(self, other):
		return self.rod_name == other.rod_name


	def is_deep_same(self, other):
		return False


	def is_same_size(self, other):
		return False


	def set_rod(self, name):
		if name == self.rod_name:
			return None
		old_name = self.rod_name
		self.rod_name = name

		self.rod_pixmap.setPixmap(Assets().rod[name].pixmap_top.scaled(self.tsz, self.tsz))
		if name == "None":
			self.set_label_mid_top("")
		else:
			self.set_label_mid_top(name)
		
		return old_name


	def set_durability(self, percent):
		frac = percent / 100
		self.progress_bar_green.setRect(self.x, self.y + self.h - 11, self.w * frac, 11)
		self.progress_bar_red.setRect(self.x + self.w * frac, self.y + self.h - 11, self.w * (1 - frac), 11)
		self.progress_bar_green.show()
		self.progress_bar_red.show()


	def set_neutron_count(self, ncount, noutput_percent):
		self.set_label_bottom_right(str(ncount) + " N")
		if (noutput_percent >= 0):
			if noutput_percent > 100.0000000001:
				if not self.overmax:
					self.overmax = True
					self.labels[5].setBrush(QColor(255, 0, 0, 255))
			else:
				if self.overmax:
					self.overmax = False
					self.labels[5].setBrush(QColor(0, 0, 0, 255))
			self.set_label_bottom_right_2("{:.2f}".format(noutput_percent) + " %")


	def set_moderation_factor(self, factor):
		self.set_label_bottom_right("x" + str(factor))


	def reset_durability(self):
		self.progress_bar_green.hide()
		self.progress_bar_red.hide()

		
	def reset_neutron_count(self):
		self.set_label_bottom_right("")
		self.set_label_bottom_right_2("")

		
	def set_label_top_left(self, text):
		self.labels[0].setText(text)
		self.labels[0].setPos(self.x + 2, self.y)
		

	def set_label_top_right(self, text):
		self.labels[1].setText(text)
		self.labels[1].setPos(self.x + self.w - self.labels[1].boundingRect().width() - 2, self.y)

		
	def set_label_bottom_left(self, text):
		self.labels[2].setText(text)
		self.labels[2].setPos(self.x + 2, self.y + self.h - 14)

		
	def set_label_bottom_right(self, text):
		self.labels[3].setText(text)
		self.labels[3].setPos(self.x + self.w - self.labels[3].boundingRect().width() - 2, self.y + self.h - 14)

		
	def set_label_top_left_2(self, text):
		self.labels[4].setText(text)
		self.labels[4].setPos(self.x + 2, self.y + 11)
		
		
	def set_label_bottom_right_2(self, text):
		self.labels[5].setText(text)
		self.labels[5].setPos(self.x + self.w - self.labels[5].boundingRect().width() - 2, self.y + self.h - 11 - 14)

		
	def set_label_mid_top(self, text):
		self.labels[6].setText(text)
		self.labels[6].setPos(self.x + (self.w - self.labels[6].boundingRect().width()) / 2, self.y + self.h / 2 - self.ofs)


class ReactorGridBlockHeader(QGraphicsRectItem):
	def __init__(self, x, y, w, h, parent=None):
		super().__init__(x, y, w, h, parent)

		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.enable_aa = Settings().get_bool("Antialiasing")
		
		self.label_left = QGraphicsSimpleTextItem(self)
		self.label_right = QGraphicsSimpleTextItem(self)

		font = self.label_left.font()
		font.setPixelSize(11) # point size 8
		if not self.enable_aa:
			font.setStyleStrategy(QFont.NoAntialias)
		self.label_left.setFont(font)
		self.label_right.setFont(font)

		self.setPen(QPen(Qt.PenStyle.NoPen))

		self.large_head = QGraphicsRectItem(x, y, w, h, self)
		self.small_head_left = QGraphicsRectItem(x, y, (w - 4) / 2, h, self)
		self.small_head_right = QGraphicsRectItem(x + (w + 4) / 2, y, (w - 4) / 2, h, self)
		self.large_head.setPen(QPen(Qt.PenStyle.NoPen))
		self.small_head_left.setPen(QPen(Qt.PenStyle.NoPen))
		self.small_head_right.setPen(QPen(Qt.PenStyle.NoPen))
		self.large_head.setBrush(QColor(150, 150, 150, 70))
		self.small_head_left.setBrush(QColor(150, 150, 150, 70))
		self.small_head_right.setBrush(QColor(150, 150, 150, 70))

		self.small_head_left.hide()
		self.small_head_right.hide()

		self.large_head.setZValue(-1)
		self.small_head_left.setZValue(-1)
		self.small_head_right.setZValue(-1)


	def set_small(self):
		self.small_head_left.show()
		self.small_head_right.show()
		self.large_head.hide()


	def set_large(self):
		self.small_head_left.hide()
		self.small_head_right.hide()
		self.large_head.show()

	
	def set_label_left(self, text):
		self.label_left.setText(text)
		self.label_left.setPos(self.x + 2, self.y - 1)


	def set_label_right(self, text):
		self.label_right.setText(text)
		self.label_right.setPos(self.x + self.w - self.label_right.boundingRect().width() - 2, self.y - 1)


class ReactorGridBlock(QGraphicsRectItem):
	show_HUt_Lt = False

	def __init__(self, yp, xp, parent=None):
		x = xp * 142.0 + 1
		y = yp * 142.0 + 1
		w = 140.0
		h = 140.0
		super().__init__(x, y, w, h, parent)

		self.xp = xp
		self.yp = yp

		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.buttons_small = [ReactorGridButton(self.x + 2, self.y + 2, (self.w - 8) / 2, (self.w - 8) / 2, 0, 0, self), 
						ReactorGridButton(self.x + 6 + (self.w - 8) / 2, self.y + 2, (self.w - 8) / 2, (self.w - 8) / 2, 0, 1, self), 
						ReactorGridButton(self.x + 2, self.y + 6 + (self.w - 8) / 2, (self.w - 8) / 2, (self.w - 8) / 2, 1, 0, self), 
						ReactorGridButton(self.x + 6 + (self.w - 8) / 2, self.y + 6 + (self.w - 8) / 2, (self.w - 8) / 2, (self.w - 8) / 2, 1, 1, self)]
		
		self.button_top_left = self.buttons_small[0]
		self.button_top_right = self.buttons_small[1]
		self.button_bottom_left = self.buttons_small[2]
		self.button_bottom_right = self.buttons_small[3]

		self.button_large = ReactorGridButton(self.x + 2, self.y + 2, (self.w - 4), (self.w - 4), -1, -1, self)
		
		self.button_large.hide()

		self.header = ReactorGridBlockHeader(self.x + 2, self.y + 2, self.w - 4, 13, self)

		self.shape_small = True
		self.coolant_name = None
		self.set_coolant("None")
		self.expcolor = False
		self.reset_coolant_flux()

		self.setPen(QPen(Qt.PenStyle.NoPen))


	def get_position(self):
		return (self.yp, self.xp)


	def on_click(self, button):
		self.scene().parent().on_click(self, button)

		
	def logical_copy(self, parent=None):
		obj = ReactorGridBlock(self.xp, self.yp, parent)
		obj.coolant_name = self.coolant_name
		if self.shape_small:
			obj.toggle_shape()
		for a,b in zip(self.get_active_buttons(), obj.get_active_buttons()):
			b.rod_name = a.rod_name
		return obj


	def reset(self):
		self.set_coolant("None")
		self.button_large.set_rod("None")
		for button in self.buttons_small:
			button.set_rod("None")
		if self.shape_small:
			self.toggle_shape()


	def get_active_buttons(self):
		if self.shape_small:
			return self.buttons_small
		else:
			return [self.button_large]

	
	def is_empty(self):
		empty = self.coolant_name == "None"
		for button in self.get_active_buttons():
			if not button.is_empty():
				empty = False
				break
		return empty
	

	def is_shallow_empty(self):
		return self.coolant_name == "None"
	

	def is_deep_empty(self):
		empty = True
		for button in self.get_active_buttons():
			if not button.is_empty():
				empty = False
				break
		return empty


	def is_small(self):
		return self.shape_small
	

	def is_same(self, other):
		same = self.coolant_name == other.coolant_name and self.shape_small == other.shape_small
		for a,b in zip(self.get_active_buttons(), other.get_active_buttons()):
			if not a.is_same(b):
				same = False
				break
		return same


	def is_shallow_same(self, other):
		return self.coolant_name == other.coolant_name


	def is_deep_same(self, other):
		same = self.shape_small == other.shape_small
		for a,b in zip(self.get_active_buttons(), other.get_active_buttons()):
			if not a.is_same(b):
				same = False
				break
		return same


	def is_same_size(self, other):
		return self.shape_small == other.shape_small
		

	def toggle_shape(self):
		self.shape_small = not self.shape_small
		if self.shape_small:
			self.button_large.hide()
			self.header.set_small()
			for button in self.buttons_small:
				button.show()
		else:
			for button in self.buttons_small:
				button.hide()
			self.button_large.show()
			self.header.set_large()


	def set_coolant(self, name):
		if name == self.coolant_name:
			return None
		old_name = self.coolant_name
		self.coolant_name = name

		if name == "None":
			self.header.hide()
		else:
			self.header.set_label_left(name)
			self.header.show()
		for button in [*self.buttons_small, self.button_large]:
			button.setBrush(QColor(Assets().coolant[name].color))

		return old_name
		

	def set_coolant_flux(self, Lt, HUt, exp):
		self.set_exploded(exp)
		if ReactorGridBlock.show_HUt_Lt:
			self.header.set_label_right(HUt + " HU/t")
		else:
			self.header.set_label_right(Lt + " L/t")
		

	def reset_coolant_flux(self):
		self.set_exploded(False)
		self.header.label_right.setText("")


	def sizeHint(self):
		return self.button_large.size()


	def minimumSizeHint(self):
		return self.button_large.size()


	def set_exploded(self, value):
		if value != self.expcolor:
			self.expcolor = value
			if value:
				self.header.label_right.setBrush(QColor(255, 0, 0, 255))
			else:
				self.header.label_right.setBrush(QColor(0, 0, 0, 255))