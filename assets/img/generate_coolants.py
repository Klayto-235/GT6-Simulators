from PIL import Image
import numpy as np


stencil_outer = np.array(Image.open("coolant_stencil.png").getchannel("R")) == 255
stencil_inner = np.invert(stencil_outer)
alpha_value = 64
coolants = [
#	("None",	(210, 	210, 	210, 	alpha_value)),
	("IC2", 	(32, 	98, 	111, 	alpha_value)),
	("Na", 		(23, 	23, 	148, 	alpha_value)),
	("Sn", 		(189, 	189,	189, 	alpha_value)),
	("D2O", 	(198, 	198,	86, 	alpha_value)),
	("DHO", 	(177, 	177,	138, 	alpha_value)),
	("T2O", 	(198, 	86, 	86, 	alpha_value)),
	("H2O", 	(75, 	87, 	210, 	alpha_value)),
	("CO2", 	(123, 	123, 	123, 	alpha_value)),
	("He",		(145, 	113, 	102, 	alpha_value)),
	("LiCl",	(178, 	178, 	198, 	alpha_value)),
	("Th",		(46,	52, 	46, 	alpha_value))
]
for (label, color) in coolants:
	data = np.zeros((48, 48, 4), np.uint8)
	data[stencil_outer, :] = (0, 0, 0, 0)
	data[stencil_inner, :] = color
	image = Image.fromarray(data, mode="RGBA")
	image.save(f"coolant_{label}.png")
