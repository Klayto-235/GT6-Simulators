from math import gcd
from Assets import Assets
from time import strftime, gmtime


def divup(a, b):
	return (a + b - 1) // b


def stackify(a):
	if a <= 64:
		return str(a)
	else:
		b = a // 64
		c = a - b * 64
		if c == 0:
			return str(b) + "x64"
		else:
			if b > 1:
				return str(b) + "x64+" + str(c)
			else:
				return "64+" + str(c)


def to_metric(input):
	scale = 0
	while (input > 999):
		input = input / 1000
		scale = scale + 3
	retstr = "{:.2f}".format(input)
	if (scale < 25):
		retstr = retstr + " " + Assets().metric_prefix[scale]
	else:
		while (input >= 10):
			input = input / 10
			scale = scale + 1
		retstr = retstr + "E" + str(scale) + " "
	return retstr


def to_human_readable_time(input):
	return str(input // 86400) + "d " + (strftime("X%Hh X%Mm X%Ss", gmtime(input))).replace("X0", "X").replace("X", "")

def to_whole_materials(format_function, input):
	if type(input) is float:
		return "{:.3f}".format(input / 72)
	temp1 = input // 72
	if input % 72 == 0:
		return format_function(temp1)
	else:
		temp2 = input % 72
		temp3 = gcd(72, temp2)
		if (temp1 == 0):
			return str(temp2 // temp3) + "/" + str(72 // temp3)
		else:
			return format_function(temp1) + "+" + str(temp2 // temp3) + "/" + str(72 // temp3)


def recursive_material_cost(format_function, key, value, raw):
		if key in Assets().material_costs:
			for k,v in Assets().material_costs[key].items():
				value[1][k] = [v * value[0], {}]
				recursive_material_cost(format_function, k, value[1][k], raw)
				value[1][k][0] = format_function(value[1][k][0])
		else:
			for k,v in Assets().raw_materials[key].items():
				value[1][k] = [to_whole_materials(format_function, v * value[0]), {}]
				if k in raw:
					raw[k][0] += v * value[0]
					if key in raw[k][1]:
						raw[k][1][key][0] += value[0]
					else:
						raw[k][1][key] = [value[0], {}]
				else:
					raw[k] = [v * value[0], { key : [value[0], {}] }]


def recursive_string_constructor(level, result, indent, data, key=""):
	if key == "":
		for k,v in sorted(data.items()):
			recursive_string_constructor(level, result, indent, v, k)
	else:
		result.append((level, indent + key + Assets().delim + str(data[0])))
		for k,v in sorted(data[1].items()):
			recursive_string_constructor(level + 1, result, indent + Assets().indent, v, k)


def recursive_dict_sum(output, input):
	for entry in input[1]:
		if entry in output[1]:
			output[1][entry][0] += " + " + input[1][entry][0]
		else:
			output[1][entry] = [ input[1][entry][0], {} ]
		recursive_dict_sum(output[1][entry], input[1][entry])