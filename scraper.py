import requests
import urllib.request
import pickle
from bs4 import BeautifulSoup

class Item:
	def __init__(self, name, rarity, url, image_url):
		self.name = name
		self.rarity = rarity
		self.url = url
		self.image_url = image_url

cz75_auto = "https://csgostash.com/weapon/CZ75-Auto"
desert_eagle = "https://csgostash.com/weapon/Desert+Eagle"
dual_berettas = "https://csgostash.com/weapon/Dual+Berettas"
five_seven = "https://csgostash.com/weapon/Five-SeveN"
glock_18 = "https://csgostash.com/weapon/Glock-18"
p2000 = "https://csgostash.com/weapon/P2000"
p250 = "https://csgostash.com/weapon/P250"
r8_revolver = "https://csgostash.com/weapon/R8+Revolver"
tec_9 = "https://csgostash.com/weapon/Tec-9"
usp_s = "https://csgostash.com/weapon/USP-S"
#---
ak_47 = "https://csgostash.com/weapon/AK-47"
aug = "https://csgostash.com/weapon/AUG"
awp = "https://csgostash.com/weapon/AWP"
famas = "https://csgostash.com/weapon/FAMAS"
gs3g1 = "https://csgostash.com/weapon/G3SG1"
galil_ar = "https://csgostash.com/weapon/Galil+AR"
m4a1_s = "https://csgostash.com/weapon/M4A1-S"
m4a4 = "https://csgostash.com/weapon/M4A4"
scar_20 = "https://csgostash.com/weapon/SCAR-20"
sg_553 = "https://csgostash.com/weapon/SG+553"
ssg_08 = "https://csgostash.com/weapon/SSG+08"
#---
mac_10 = "https://csgostash.com/weapon/MAC-10"
mp5_sd = "https://csgostash.com/weapon/MP5-SD"
mp7 = "https://csgostash.com/weapon/MP7"
mp9 = "https://csgostash.com/weapon/MP9"
pp_bizon = "https://csgostash.com/weapon/PP-Bizon"
p90 = "https://csgostash.com/weapon/P90"
ump_45 = "https://csgostash.com/weapon/UMP-45"
#---
mag_7 = "https://csgostash.com/weapon/MAG-7"
nova = "https://csgostash.com/weapon/Nova"
sawed_off = "https://csgostash.com/weapon/Sawed-Off"
xm1014 = "https://csgostash.com/weapon/XM1014"
m249 = "https://csgostash.com/weapon/M249"
negev = "https://csgostash.com/weapon/Negev"
#---
nomad_knife = "https://csgostash.com/weapon/Nomad+Knife"
skeleton_knife = "https://csgostash.com/weapon/Skeleton+Knife"
survival_knife = "https://csgostash.com/weapon/Survival+Knife"
paracord_knife = "https://csgostash.com/weapon/Paracord+Knife"
classic_knife = "https://csgostash.com/weapon/Classic+Knife"
bayonet = "https://csgostash.com/weapon/Bayonet"
bowie_knife = "https://csgostash.com/weapon/Bowie+Knife"
butterfly_knife = "https://csgostash.com/weapon/Butterfly+Knife"
falchion_knife = "https://csgostash.com/weapon/Falchion+Knife"
flip_knife = "https://csgostash.com/weapon/Flip+Knife"
gut_knife = "https://csgostash.com/weapon/Gut+Knife"
huntsman_knife = "https://csgostash.com/weapon/Huntsman+Knife"
karambit = "https://csgostash.com/weapon/Karambit"
m9_bayonet = "https://csgostash.com/weapon/M9+Bayonet"
navaja_knife = "https://csgostash.com/weapon/Navaja+Knife"
shadow_daggers = "https://csgostash.com/weapon/Shadow+Daggers"
stiletto_knife = "https://csgostash.com/weapon/Stiletto+Knife"
talon_knife = "https://csgostash.com/weapon/Talon+Knife"
ursus_knife = "https://csgostash.com/weapon/Ursus+Knife"

skin_dictionary = {"Consumer": [], "Industrial": [], "Mil-Spec": [], "Restricted": [], "Classified": [], "Covert": [], "Knife": [], "Contraband": []}

weapon_list = [cz75_auto, desert_eagle, dual_berettas, five_seven, glock_18, p2000, p250, r8_revolver,
			   tec_9, usp_s, ak_47, aug, awp, famas, gs3g1, galil_ar, m4a1_s, m4a4, scar_20, sg_553,
			   ssg_08, mac_10, mp5_sd, mp7, mp9, pp_bizon, p90, ump_45, mag_7, nova, sawed_off, xm1014,
			   m249, negev, nomad_knife, skeleton_knife, survival_knife, paracord_knife, classic_knife,
			   bayonet, bowie_knife, butterfly_knife, falchion_knife, flip_knife, gut_knife,
			   huntsman_knife, karambit, m9_bayonet, navaja_knife, shadow_daggers, stiletto_knife,
			   talon_knife, ursus_knife]

for url in weapon_list:
	response = requests.get(url)
	skin_scrape = BeautifulSoup(response.text, "html.parser")
	skin_list = skin_scrape.find_all("div", class_="well result-box nomargin")
	for skin in skin_list:
		links = skin.find_all("a")
		if len(links) == 0:
			continue
		page_link = links[2]['href']
		response = requests.get(page_link)
		weaponscrape = BeautifulSoup(response.text, "html.parser")
		gun = weaponscrape.find_all("div", class_="well result-box nomargin")
		link_pieces = gun[0].find_all("a")
		name = link_pieces[0].contents[0] + " | " + link_pieces[1].contents[0]
		rarity_tag = gun[0].find_all("div", class_="quality")
		rarity_string = rarity_tag[0].p.contents[0].split()
		if rarity_string[1] == "Knife":
			rarity = "Knife"
		else:
			rarity = rarity_string[0]
		image_url = link_pieces[3]['href']
		item = Item(name, rarity, page_link, image_url)
		skin_dictionary[item.rarity].append(item)

filename = "skins"
outfile = open(filename, "wb")
pickle.dump(skin_dictionary, outfile)
outfile.close()
print("Extraction completed")