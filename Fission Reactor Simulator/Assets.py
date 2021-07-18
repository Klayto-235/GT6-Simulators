from collections import namedtuple
from operator import add,mul
from PyQt6.QtGui import QPixmap, QColor, QBitmap
from PyQt6.QtCore import Qt

from helpers import Singleton


RodRecord = namedtuple("RodRecord", ["pixmap", "pixmap_top", "durability", "neutron_emission", "neutron_self", "neutron_max", "neutron_div", "HUperN", "full_name"])
CoolantRecord = namedtuple("CoolantRecord", ["pixmap", "color", "capacity", "temperature", "mod_emission", "mod_self", "mod_max", "mod_div", "moderates", "HU_div", "full_name"])


class Assets(metaclass=Singleton):
	"""Contains all application assets."""

	def __init__(self):
		stylesheet_file = open("stylesheet.qss")
		self.stylesheet = stylesheet_file.read()
		stylesheet_file.close()

		# Utility
		utility_images = {
			"Shape" :		"img/shape_tool.png",
			"Select" :		"img/select_tool.png",
			"Erase" :		"img/erase_tool.png",
			"Fill" :		"img/fill_tool.png",
			"Floodfill" :	"img/floodfill_tool.png",
			"Reset" :		"img/reset_tool.png",
			"Plus" :		"img/plus.png",
			"Minus" :		"img/minus.png",
			"Play" :		"img/play.png",
			"Width" :		"img/width.png",
			"Height" :		"img/height.png",
			"AddColLeft" :	"img/add_col_left.png",
			"RemColLeft" :	"img/rem_col_left.png",
			"AddColRight" :	"img/add_col_right.png",
			"RemColRight" :	"img/rem_col_right.png",
			"AddRowTop" :	"img/add_row_top.png",
			"RemRowTop" :	"img/rem_row_top.png",
			"AddRowBot" :	"img/add_row_bot.png",
			"RemRowBot" :	"img/rem_row_bot.png"
		}
		empty_pixmap = QPixmap(48, 48)
		empty_pixmap.fill(QColor(0, 0, 0, 0))
		self.utility_pixmap = {"Empty" : empty_pixmap}
		for name,path in utility_images.items():
			self.utility_pixmap[name] = QPixmap(path)

		self.rowcol_util = [ "AddColLeft", "AddColRight", "AddRowTop", "AddRowBot", "RemColLeft", "RemColRight", "RemRowTop", "RemRowBot" ]
		self.smaller_utility_pixmap = {}
		for name in self.rowcol_util:
			self.smaller_utility_pixmap[name] = self.utility_pixmap[name].copy(6, 6, 36, 36)
		
		# Rods
		rod_images = {
			"Ref" :		"img/rod_reflector.png",
			"Abs" :		"img/rod_absorber.png",
			"Mod" :		"img/rod_moderator.png",
			"U-238" :	"img/rod_U-238.png",
			"U-235" :	"img/rod_U-235.png",
			"U-233" :	"img/rod_U-233.png",
			"Th-232" :	"img/rod_Th-232.png",
			"Co-60" :	"img/rod_Co-60.png",
			"Pu-244" :	"img/rod_Pu-244.png",
			"Pu-243" :	"img/rod_Pu-243.png",
			"Pu-241" :	"img/rod_Pu-241.png",
			"Pu-239" :	"img/rod_Pu-239.png",
			"Am-245" :	"img/rod_Am-245.png",
			"Am-241" :	"img/rod_Am-241.png",
			"Nq-528" :	"img/rod_Nq-528.png",
			"Nq-522" :	"img/rod_Nq-522.png",
			"U-238B" :	"img/rod_U-238B.png",
			"Th-232B" :	"img/rod_Th-232B.png"
		}
		rod_pixmaps = {"None" : self.utility_pixmap["Empty"]}
		for name,path in rod_images.items():
			rod_pixmaps[name] = QPixmap(path)

		top_images = {
			"Ref" :		"img/top_reflector.png",
			"Abs" :		"img/top_absorber.png",
			"Mod" :		"img/top_moderator.png",
			"U-238" :	"img/top_U-238.png",
			"U-235" :	"img/top_U-235.png",
			"U-233" :	"img/top_U-233.png",
			"Th-232" :	"img/top_Th-232.png",
			"Co-60" :	"img/top_Co-60.png",
			"Pu-244" :	"img/top_Pu-244.png",
			"Pu-243" :	"img/top_Pu-243.png",
			"Pu-241" :	"img/top_Pu-241.png",
			"Pu-239" :	"img/top_Pu-239.png",
			"Am-245" :	"img/top_Am-245.png",
			"Am-241" :	"img/top_Am-241.png",
			"Nq-528" :	"img/top_Nq-528.png",
			"Nq-522" :	"img/top_Nq-522.png",
			"U-238B" :	"img/top_U-238B.png",
			"Th-232B" :	"img/top_Th-232B.png"
		}
		top_pixmaps = {"None" : self.utility_pixmap["Empty"]}
		for name,path in top_images.items():
			top_pixmaps[name] = QPixmap(path)
		
		self.rod = { # pixmap, pixmap_top, durability, neutron_emission, neutron_self, neutron_max, neutron_div, HUperN, full_name
			"None" :	RodRecord(	rod_pixmaps["None"],	top_pixmaps["None"],	-1,			0,		0,		0,		0,	(0,1),	"No rod"						),
			"Ref" :		RodRecord(	rod_pixmaps["Ref"],		top_pixmaps["Ref"],		-1,			0,		0,		0,		0,	(0,1),	"Reflector rod"					),
			"Abs" :		RodRecord(	rod_pixmaps["Abs"],		top_pixmaps["Abs"],		-1,			0,		0,		0,		0,	(2,1),	"Absorber rod"					),
			"Mod" :		RodRecord(	rod_pixmaps["Mod"],		top_pixmaps["Mod"],		-1,			0,		0,		0,		0,	(0,1),	"Moderator rod"					),
			"U-238" :	RodRecord(	rod_pixmaps["U-238"],	top_pixmaps["U-238"],	50000,		4,		4 ,		512,	16,	(1,1),	"Uranium 238 fuel rod"			),
			"U-235" :	RodRecord(	rod_pixmaps["U-235"],	top_pixmaps["U-235"],	10000,		32,		32,		2048,	4,	(1,1),	"Uranium 235 fuel rod"			),
			"U-233" :	RodRecord(	rod_pixmaps["U-233"],	top_pixmaps["U-233"],	50000,		32,		32,		2048,	5,	(1,1),	"Uranium 233 fuel rod"			),
			"Th-232" :	RodRecord(	rod_pixmaps["Th-232"],	top_pixmaps["Th-232"],	100000,		2,		2,		128,	32,	(1,1),	"Thorium 232 fuel rod"			),
			"Co-60" :	RodRecord(	rod_pixmaps["Co-60"],	top_pixmaps["Co-60"],	50000,		2,		2,		256,	16,	(1,1),	"Cobalt 60 fuel rod"			),
			"Pu-244" :	RodRecord(	rod_pixmaps["Pu-244"],	top_pixmaps["Pu-244"],	10000,		64,		64,		2048,	4,	(1,1),	"Plutonium 244 fuel rod"		),
			"Pu-243" :	RodRecord(	rod_pixmaps["Pu-243"],	top_pixmaps["Pu-243"],	10000,		128,	128,	4096,	3,	(1,1),	"Plutonium 243 fuel rod"		), 
			"Pu-241" :	RodRecord(	rod_pixmaps["Pu-241"],	top_pixmaps["Pu-241"],	10000,		128,	128,	3072,	4,	(1,1),	"Plutonium 241 fuel rod"		),
			"Pu-239" :	RodRecord(	rod_pixmaps["Pu-239"],	top_pixmaps["Pu-239"],	20000,		128,	128,	4096,	3,	(1,1),	"Plutonium 239 fuel rod"		),
			"Am-245" :	RodRecord(	rod_pixmaps["Am-245"],	top_pixmaps["Am-245"],	10000,		64,		64,		4096,	4,	(1,1),	"Americium 245 fuel rod"		),
			"Am-241" :	RodRecord(	rod_pixmaps["Am-241"],	top_pixmaps["Am-241"],	10000,		128,	128,	4096,	3,	(1,1),	"Americium 241 fuel rod"		),
			"Nq-528" :	RodRecord(	rod_pixmaps["Nq-528"],	top_pixmaps["Nq-528"],	100000,		128,	128,	8192,	4,	(1,1),	"Enriched Naquadah fuel rod"	),
			"Nq-522" :	RodRecord(	rod_pixmaps["Nq-522"],	top_pixmaps["Nq-522"],	100000,		512,	512,	16384,	3,	(1,1),	"Naquadria fuel rod"	),
			"U-238B" :	RodRecord(	rod_pixmaps["U-238B"],	top_pixmaps["U-238B"],	288000000,	0,		0,		0,		0,	(1,2),	"Uranium 238 breeder rod"		),
			"Th-232B" :	RodRecord(	rod_pixmaps["Th-232B"],	top_pixmaps["Th-232B"],	144000000,	0,		0,		0,		0,	(1,2),	"Thorium 232 breeder rod"		)
		}

		self.material_costs = {
			"Ref" : { "Empty Reactor Rod" : 1, "Beryllium Rod" : 1 },
			"Abs" : { "Empty Reactor Rod" : 1, "Cd-In-Ag-Alloy Rod" : 1 },
			"Mod" : { "Empty Reactor Rod" : 1, "Graphite Rod" : 1 },
			"U-238" : { "Empty Reactor Rod" : 1, "Uranium Rod" : 1 },
			"U-235" : { "Empty Reactor Rod" : 1, "Uranium-235 Rod" : 1 },
			"U-233" : { "Empty Reactor Rod" : 1, "Uranium-233 Rod" : 1 },
			"Th-232" : { "Empty Reactor Rod" : 1, "Thorium Rod" : 1 },
			"Co-60" : { "Empty Reactor Rod" : 1, "Cobalt-60 Rod" : 1 },
			"Pu-244" : { "Empty Reactor Rod" : 1, "Plutonium Rod" : 1 },
			"Pu-243" : { "Empty Reactor Rod" : 1, "Plutonium-243 Rod" : 1 },
			"Pu-241" : { "Empty Reactor Rod" : 1, "Plutonium-241 Rod" : 1 },
			"Pu-239" : { "Empty Reactor Rod" : 1, "Plutonium-239 Rod" : 1 },
			"Am-245" : { "Empty Reactor Rod" : 1, "Americium Rod" : 1 },
			"Am-241" : { "Empty Reactor Rod" : 1, "Americium-241 Rod" : 1 },
			"Nq-528" : { "Empty Reactor Rod" : 1, "Enriched Naquadah Rod" : 1 },
			"Nq-522" : { "Empty Reactor Rod" : 1, "Naquadria Rod" : 1 },
			"U-238B" : { "Empty Reactor Rod" : 1, "Uranium Bolt" : 4 },
			"Th-232B" : { "Empty Reactor Rod" : 1, "Thorium Bolt" : 4 },
			"Nuclear Reactor Core (1x1)" : { "Dense Lead Machine Casing" : 1, "Compact Electric Piston (EV)" : 1, "Crystal Processor (Ruby)" : 1 },
			"Nuclear Reactor Core (2x2)" : { "Dense Lead Machine Casing" : 1, "Compact Electric Piston (EV)" : 4, "Crystal Processor (Ruby)" : 4 },
			"Dense Lead Plate" : { "Block of Lead" : 1 },
			"Crystal Circuit (Ruby)" : { "Crystalline Ruby Plate" : 1 },
			"4x Annealed Copper Wire" : { "Annealed Copper Wire" : 4 },
			"Magnetic Neodymium Rod" : { "Neodymium Rod" : 1 },
			"Compact Electric Piston (EV)" : { "Chromium Screw" : 2, "Chromium Plate" : 2, "Chromium Rod" : 2, "Small Chromium Gear" : 1, "Compact Electric Motor (EV)" : 1 },
			"Dense Lead Machine Casing" : { "Dense Lead Plate" : 6, "Long Lead Rod" : 2 },
			"Crystal Processor (Ruby)" : { "Crystal Circuit (Ruby)" : 1 , "Crystal Processor Socket" : 1 },
			"Compact Electric Motor (EV)" : { "1x Aluminium Cable" : 2, "Curved Chromium Plate" : 1, "Chromium Rod" : 1, "4x Annealed Copper Wire" : 4, "Magnetic Neodymium Rod" : 1 },
			"1x Aluminium Cable" : { "Aluminium Wire" : 1, "Rubber Sheet" : 1 },
			"1x Copper Cable" : { "Copper Wire" : 1, "Rubber Sheet" : 1 },
			"Crystal Processor Socket" : { "Circuit Plate (Platinum)" : 1, "Circuit T6 (Ultimate)" : 4, "Helium-Neon Laser Emitter" : 4 },
			"Helium-Neon Laser Emitter" : { "Helium-Neon Gas" : 1, "Circuit T2 (Good)" : 1, "Glass" : 1, "Silver Plate" : 2, "Stainless Steel Screw" : 1, "1x Copper Cable" : 2 },
			"Circuit T6 (Ultimate)" : { "Circuit Plate (Platinum)" : 1, "Molten Soldering Alloy" : 1, "Circuit Part (Ultimate)" : 4 },
			"Circuit T2 (Good)" : { "Circuit Plate (Copper)" : 1, "Molten Tin" : 1, "Circuit Part (Good)" : 4 },
			"Circuit Plate (Copper)" : { "Circuit Plate" : 1, "Circuit Wiring (Copper)" : 1 },
			"Circuit Plate (Platinum)" : { "Circuit Plate" : 1, "Circuit Wiring (Platinum)" : 1 },
			"Circuit Plate" : { "Plastic Sheet" : 1, "Silicon Dioxide Dust" : 1 },
			"Circuit Wiring (Copper)" : { "Copper Foil" : 4 },
			"Circuit Wiring (Platinum)" : { "Platinum Foil" : 4 },
			"Circuit Part (Ultimate)" : { "Fine Platinum Wire" : 1, "Fine Signalum Wire" : 1, "Tiny Crystalline Redstone Alloy Plate" : 1 },
			"Circuit Part (Good)" : { "Fine Copper Wire" : 1, "Fine Red Alloy Wire" : 1, "Tiny Crystalline Silicon Plate" : 1 }
		}

		self.raw_materials = {
			"Empty Reactor Rod" : { "Zirconium" : 1*72  },
			"Beryllium Rod" : { "Beryllium" : 72//2 },
			"Cd-In-Ag-Alloy Rod" : { "Cd-In-Ag-Alloy" : 72//2 },
			"Graphite Rod" : { "Graphite" : 72 },
			"Uranium Rod" : { "Uranium" : 72//2 },
			"Uranium-235 Rod" : { "Uranium-235" : 72//2 },
			"Uranium-233 Rod" : { "Uranium-233" : 72//2 },
			"Thorium Rod" : { "Thorium" : 72//2 },
			"Cobalt-60 Rod" : { "Cobalt-60" : 72//2 },
			"Plutonium Rod" : { "Plutonium" : 72//2 },
			"Plutonium-243 Rod" : { "Plutonium-243" : 72//2 },
			"Plutonium-241 Rod" : { "Plutonium-241" : 72//2 },
			"Plutonium-239 Rod" : { "Plutonium-239" : 72//2 },
			"Americium Rod" : { "Americium" : 72//2 },
			"Americium-241 Rod" : { "Americium-241" : 72//2 },
			"Enriched Naquadah Rod" : { "Enriched Naquadah" : 72//2 },
			"Naquadria Rod" : { "Naquadria" : 72//2 },
			"Uranium Bolt" : { "Uranium" : 72//8 },
			"Thorium Bolt" : { "Thorium" : 72//8 },
			"Chromium Screw" : { "Chromium" : 72//9 },
			"Chromium Plate" : { "Chromium" : 1*72 },
			"Curved Chromium Plate" : { "Chromium" : 1*72 },
			"Chromium Rod" : { "Chromium" : 72//2 },
			"Small Chromium Gear" : { "Chromium" : 1*72 },
			"Block of Lead" : { "Lead" : 9*72 },
			"Long Lead Rod" : { "Lead" : 1*72 },
			"Crystalline Ruby Plate" : { "Ruby" : 1*72 },
			"Annealed Copper Wire" : { "Annealed Copper" : 72//2},
			"Neodymium Rod" : { "Neodymium" : 72//2 },
			"Aluminium Wire" : { "Aluminium" : 72//2 },
			"Rubber Sheet" : { "Rubber" : 1*72 },
			"Copper Wire" : { "Copper" : 72//2 },
			"Silver Plate" : { "Silver" : 1*72 },
			"Stainless Steel Screw" : { "Stainless Steel" : 72//9 },
			"Helium-Neon Gas" : { "Helium-Neon" : 1*72 },
			"Glass" : { "Sand" : 1*72 },
			"Molten Soldering Alloy" : { "Soldering Alloy" : 1*72 },
			"Molten Tin" : { "Tin" : 1*72 },
			"Plastic Sheet" : { "Plastic" : 1*72 },
			"Copper Foil" : { "Copper" : 72//4 },
			"Platinum Foil" : { "Platinum" : 72//4 },
			"Fine Platinum Wire" : { "Platinum" : 72//8 },
			"Fine Signalum Wire" : { "Signalum" : 72//8 },
			"Fine Copper Wire" : { "Copper" : 72//8 },
			"Fine Red Alloy Wire" : { "Red Alloy" : 72//8 },
			"Silicon Dioxide Dust" : { "Silicon Dioxide" : 1*72 },
			"Tiny Crystalline Redstone Alloy Plate" : { "Redstone Alloy (Crystalline)" : 72//9 },
			"Tiny Crystalline Silicon Plate" : { "Silicon (Crystalline)" : 72//9 },
			"Th coolant (L)" : { "Thorium (loss)" : 1*72/9216 } #This is less than 1/72, so we just use a float, cba
		}

		self.rod_tooltips = {}

		for k,v in self.rod.items():
			tempstr = ""
			if k == "None":
				tempstr = "Clear rod slot"
			else:
				tempstr += "Base stats for "
				tempstr += v.full_name
				tempstr += "\n"
				tempstr += "Durability: "
				if v.durability == -1:
					tempstr += "infinite"
				else:
					tempstr += str(v.durability)
				tempstr += "\n"
				tempstr += "Neutron emission: "
				tempstr += str(v.neutron_emission)
				tempstr += "\n"
				tempstr += "Neutron self emission: "
				tempstr += str(v.neutron_self)
				tempstr += "\n"
				tempstr += "Max neutron emission: "
				if v.neutron_max == 0:
					tempstr += "N/A"
				else:
					tempstr += str(v.neutron_max)
				tempstr += "\n"
				tempstr += "Neutron emission factor: "
				if v.neutron_div == 0:
					tempstr += "0"
				else:
					tempstr += "1/" + str(v.neutron_div)
				tempstr += "\n"
				tempstr += "HU per neutron: "
				if v.HUperN[1] == 1:
					tempstr += str(v.HUperN[0])
				else:
					tempstr += str(v.HUperN[0]) + "/" + str(v.HUperN[1])
			self.rod_tooltips[k] = tempstr

		# Coolants
		alpha_value = 64
		coolant_colors = [
			QColor(210, 210, 210, alpha_value),
			QColor(32, 98, 111, alpha_value),
			QColor(23, 23, 148, alpha_value),
			QColor(189, 189, 189, alpha_value),
			QColor(198, 198, 86, alpha_value),
			QColor(177, 177, 138, alpha_value),
			QColor(198, 86, 86, alpha_value),
			QColor(75, 87, 210, alpha_value),
			QColor(123, 123, 123, alpha_value),
			QColor(145, 113, 102, alpha_value),
			QColor(178, 178, 198, alpha_value),
			QColor(46, 52, 46, alpha_value)
		]
		coolant_stencil = QBitmap.fromPixmap(QPixmap("img/coolant_stencil.png", None, Qt.ImageConversionFlags.MonoOnly | Qt.ImageConversionFlags.ThresholdDither))
		coolant_pixmaps = [self.utility_pixmap["Empty"]]
		for color in coolant_colors[1:]:
			tmp = QPixmap(48, 48)
			tmp.fill(color)
			tmp.setMask(coolant_stencil)
			coolant_pixmaps.append(tmp)
			
		self.coolant = { # pixmap, color, capacity, temperature, mod_emission, mod_self, mod_max, mod_div, moderates, HU_div, full_name
			"None" :	CoolantRecord(	coolant_pixmaps[0],		coolant_colors[0],	0,		-1,		( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		False,	1,	"No coolant"				),
			"IC2" :		CoolantRecord(	coolant_pixmaps[1],		coolant_colors[1],	20,		1200,	( 4, 1 ),	( 4, 1 ),	( 1, 1 ),	( mul, 2 ),		False,	1,	"IC2 coolant"				), 
			"Na" :		CoolantRecord(	coolant_pixmaps[2],		coolant_colors[2],	30,		1100,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		False,	6,	"Sodium (Na)"				), 
			"Sn" :		CoolantRecord(	coolant_pixmaps[3],		coolant_colors[3],	40,		2800,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		False,	3,	"Tin (Sn)"					), 
			"D2O" :		CoolantRecord(	coolant_pixmaps[4],		coolant_colors[4],	50,		600,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		True,	1,	"Heavy water (D2O)"			), 
			"DHO" :		CoolantRecord(	coolant_pixmaps[5],		coolant_colors[5],	40,		550,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		True,	1,	"Semiheavy water (DHO)"		), 
			"T2O" :		CoolantRecord(	coolant_pixmaps[6],		coolant_colors[6],	60,		650,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		True,	1,	"Tritiated water (T2O)"		), 
			"H2O" :		CoolantRecord(	coolant_pixmaps[7],		coolant_colors[7],	80,		420,	( 1, 1 ),	( 1, 1 ),	( 1, 1 ),	( mul, 1 ),		True,	1,	"Water (H2O)"				), 
			"CO2" :		CoolantRecord(	coolant_pixmaps[8],		coolant_colors[8],	20,		950,	( 1, 1 ),	( 3, 1 ),	( 1, 1 ),	( add, -1 ),	False,	1,	"Carbon Dioxide (CO2)"		), 
			"He" :		CoolantRecord(	coolant_pixmaps[9],		coolant_colors[9],	30,		1150,	( 1, 2 ),	( 4, 1 ),	( 1, 1 ),	( add, 1 ),		False,	1,	"Helium (He)"				), 
			"LiCl" :	CoolantRecord(	coolant_pixmaps[10],	coolant_colors[10],	15,		1600,	( 1, 2 ),	( 5, 1 ),	( 5, 4 ),	( mul, 1 ),		False,	1,	"Lithium Chloride (LiCl)"	), 
			"Th" :		CoolantRecord(	coolant_pixmaps[11],	coolant_colors[11],	10000,	-1,		( 1, 2 ),	( 0, 1 ),	( 4, 1 ),	( add, -1 )	,	False,	1,	"Thorium salts (Th)"		)
		}

		self.coolant_tooltips = {}

		for k,v in self.coolant.items():
			tempstr = ""
			if k == "None":
				tempstr = "Clear coolant"
			else:
				tempstr += v.full_name
				tempstr += "\nHeat capacity: "
				tempstr += str(v.capacity) + " HU/L"
				tempstr += "\nHeatant temperature: "
				if v.temperature == -1:
					tempstr += "N/A"
				else:
					tempstr += str(v.temperature) + " K"
				tempstr += "\nRod emission factor: "
				if v.mod_emission[1] == 1:
					tempstr += str(v.mod_emission[0])
				else:
					tempstr += str(v.mod_emission[0]) + "/" + str(v.mod_emission[1])
				tempstr += "\nRod self emission factor: "
				if v.mod_self[1] == 1:
					tempstr += str(v.mod_self[0])
				else:
					tempstr += str(v.mod_self[0]) + "/" + str(v.mod_self[1])
				tempstr += "\nRod max neutron emission factor: "
				if v.mod_max[1] == 1:
					tempstr += str(v.mod_max[0])
				else:
					tempstr += str(v.mod_max[0]) + "/" + str(v.mod_max[1])
				tempstr += "\nRod neutron emission factor divisor modifier: "
				if v.mod_div[0] is mul:
					tempstr += "*" + str(v.mod_div[1])
				else:
					if v.mod_div[1] > 0:
						tempstr += "+" + str(v.mod_div[1])
					else:
						tempstr += str(v.mod_div[1])
				tempstr += "\nModerates rods: "
				if v.moderates:
					tempstr += "Yes"
				else:
					tempstr += "No"
				tempstr += "\nHU per neutron factor: "
				if v.HU_div == 1:
					tempstr += "1"
				else:
					tempstr += "1/" + str(v.HU_div)
				if k == "Th":
					tempstr += "\nConsumes 1 unit of Thorium per 9216 L of coolant used."
			self.coolant_tooltips[k] = tempstr

		self.metric_prefix = {
			0 : "",
			3 : "k",
			6 : "M",
			9 : "G",
			12 : "T",
			15 : "P",
			18 : "E",
			21 : "Z",
			24 : "Y"
		}

		self.indent = ""
		self.delim = " :  "
		self.tank_capacity = 64000.0

		#I'm not sure where to put this stuff (see below). Almost belongs in a separate text file but... it's an asset!

		self.about_message = """Gregarious Toolicities presents the state of the art (maybe) simulator for nuclear fission reactors in GT6. 
Forged in the fires of mount "Qt and Python, why did we want to learn these again?", this simulator will help you avoid blowing up your home. 
Alternatively, with a little less luck, it might have a bug and help you get rid of that aging house anyway, there's only one way to find out.

Tested (kind of) for GT6 version 1.7.10-6.14.15, a single trivial test case worked. 

DISCLAIMER: Gregarious Toolicities will take no responsibility if you do end up blowing something up. Why did you ever trust us anyway?"""

		self.readme_message = """Eventually something meaningful might show up here. 
For now you must trust your wits to figure out how this all works, it's pretty straightforward anyway. 
We believe in you!"""