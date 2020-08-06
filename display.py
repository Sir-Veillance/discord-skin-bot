import pickle

class Item:
	def __init__(self, name, rarity, url, image_url):
		self.name = name
		self.rarity = rarity
		self.url = url
		self.image_url = image_url

pickle_file = open("skins", "rb")
skin_dictionary = pickle.load(pickle_file)

for key in skin_dictionary:
	for skin in skin_dictionary[key]:
		print("{} - {}".format(skin.name, skin.rarity))