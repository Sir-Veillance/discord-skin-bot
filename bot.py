import discord
import pickle
import random
import sys
from analyzer import get_price

class Item:
    def __init__(self, name, rarity, url, image_url):
        self.name = name
        self.rarity = rarity
        self.url = url
        self.image_url = image_url

file = open("token.txt", "r")
TOKEN = file.readline()
file.close()

client = discord.Client()

pickle_file = open("skins", "rb")
skin_dictionary = pickle.load(pickle_file)
pickle_file.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # this user ID could be replaced by something other than a single user
    if str(message.author.id) == "225105242969210880" and message.content.startswith("-retire"):
        msg = "Disconnecting from the server..."
        await message.channel.send(msg)
        sys.exit()
    if message.content == "-skin":
    	rarity = random.random() * 100
    	if rarity > 99.99:
    		skin = random.choice(skin_dictionary["Contraband"])
    	elif rarity > 99.7442:
    		skin = random.choice(skin_dictionary["Knife"])
    	elif rarity > 99.1048:
    		skin = random.choice(skin_dictionary["Covert"])
    	elif rarity > 95.9079:
    		skin = random.choice(skin_dictionary["Classified"])
    	elif rarity > 79.9229:
    		skin = random.choice(skin_dictionary["Restricted"])
    	elif rarity > 39.9229:
    		skin = random.choice(skin_dictionary["Mil-Spec"])
    	elif rarity > 30:
    		skin = random.choice(skin_dictionary["Industrial"])
    	elif rarity > 0:
    		skin = random.choice(skin_dictionary["Consumer"])
    	msg = skin.image_url + "\n>>> You receive: {}\n  {}".format(skin.name, skin.rarity) + "\n" + str(get_price(skin))
    	await message.channel.send(msg)


client.run(TOKEN)