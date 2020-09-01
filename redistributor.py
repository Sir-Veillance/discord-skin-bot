import requests
import urllib.request
import pickle
from analyzer import get_price

class Item:
	def __init__(self, name, rarity, url, image_url):
		self.name = name
		self.rarity = rarity
		self.url = url
		self.image_url = image_url

pickle_file = open("skins", "rb")
skin_dictionary = pickle.load(pickle_file)
pickle_file.close()

new_dictionary = {}
hold_list = []

for key in skin_dictionary:
	for skin in skin_dictionary[key]:
		hold_list.append((skin, get_price(skin)))

hold_list.sort(key=lambda tup: tup[1])

low_value_bool = False
medium_value_bool = False
high_value_bool = False
veryhigh_value_bool = False
extreme_value_bool = False

for item in hold_list:
	if item[1] >= 2.45 and not(low_value_bool):
		low_value = hold_list.index(item)
		low_value_bool = True
	if item[1] >= 7.50 and not(medium_value_bool):
		medium_value = hold_list.index(item)
		medium_value_bool = True
	if item[1] >= 15.00 and not(high_value_bool):
		high_value = hold_list.index(item)
		high_value_bool = True
	if item[1] >= 100.00 and not(veryhigh_value_bool):
		veryhigh_value = hold_list.index(item)
		veryhigh_value_bool = True

new_dictionary["low"] = hold_list[0:low_value + 1]
new_dictionary["medium"] = hold_list[low_value + 1: medium_value + 1]
new_dictionary["high"] = hold_list[medium_value + 1: high_value + 1]
new_dictionary["veryhigh"] = hold_list[high_value + 1: veryhigh_value + 1]
new_dictionary["extreme"] = hold_list[veryhigh_value + 1: len(hold_list)]

filename = "redistributed"
outfile = open(filename, "wb")
pickle.dump(new_dictionary, outfile)
outfile.close()
print("Distribution complete")

print(len(skin_dictionary["Consumer"]) + len(skin_dictionary["Industrial"]) + len(skin_dictionary["Mil-Spec"]) + len(skin_dictionary["Restricted"]) + len(skin_dictionary["Classified"]) + len(skin_dictionary["Covert"]) + len(skin_dictionary["Knife"]) + len(skin_dictionary["Contraband"]))
print(len(new_dictionary["low"]) + len(new_dictionary["medium"]) + len(new_dictionary["high"]) + len(new_dictionary["veryhigh"]) + len(new_dictionary["extreme"]))
