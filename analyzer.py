import requests
import urllib.request
from bs4 import BeautifulSoup

class Item:
    def __init__(self, name, rarity, url, image_url):
        self.name = name
        self.rarity = rarity
        self.url = url
        self.image_url = image_url

def get_price(item):
	response = requests.get(item.url)
	skin_scrape = BeautifulSoup(response.text, "html.parser")
	stattrak_check = skin_scrape.find_all("span", class_="pull-left")
	stattrak = False
	souvenir = False
	for element in stattrak_check:
		if element.contents[0] == "StatTrak":
			stattrak = True
		if element.contents[0] == "Souvenir":
			souvenir = True
	prices = skin_scrape.find_all("span", class_="pull-right")
	if len(prices) == 20:
		if stattrak:
			checks = [5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
			for check in checks:
				try:
					price = float(prices[check].contents[0].translate({ord(i):None for i in '$,'}))
					return(price)
				except:
					pass
			return 0
		elif souvenir:
			checks = [0, 10, 1, 11, 2, 12, 3, 13, 4, 14]
			for check in checks:
				try:
					price = float(prices[check].contents[0].translate({ord(i):None for i in '$,'}))
					return(price)
				except:
					pass
			return 0
		else:
			return "Error: full 20 prices but not souvenir/stattrak"
	if len(prices) == 10:
		checks = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
		for check in checks:
			try:
				price = float(prices[check].contents[0].translate({ord(i):None for i in '$,'}))
				return(price)
			except:
				pass
		return 0
	if len(prices) == 4:
		checks = [1, 3]
		for check in checks:
			try:
				price = float(prices[check].contents[0].translate({ord(i):None for i in '$,'}))
				return(price)
			except:
				pass
		return 0
	else:
		return "Error: did not fit existing price-count pattern"
