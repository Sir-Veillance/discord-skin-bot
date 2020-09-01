import asyncio
import discord
import pickle
import random
import re
import sys
import time
# import PyNaCl
from analyzer import get_price

class Item:
    def __init__(self, name, rarity, url, image_url):
        self.name = name
        self.rarity = rarity
        self.url = url
        self.image_url = image_url

def get_skin(balance_id):
    rarity = random.random() * 100
    if rarity > 99.7442:
        skin = random.choice(skin_dictionary["extreme"])
    elif rarity > 99.1048:
        skin = random.choice(skin_dictionary["veryhigh"])
    elif rarity > 95.9079:
        skin = random.choice(skin_dictionary["high"])
    elif rarity > 79.9229:
        skin = random.choice(skin_dictionary["medium"])
    elif rarity > 0:
        skin = random.choice(skin_dictionary["low"])
    price = round(get_price(skin[0]), 2)
    try:
        user_balances[balance_id] = user_balances[balance_id] + price
    except:
        user_balances[balance_id] = price
    msg = skin[0].image_url + "\n>>> You receive: {}\n  {}".format(skin[0].name, skin[0].rarity) + "\n" + "${:,.2f}".format(price)
    return msg

file = open("token.txt", "r")
TOKEN = file.readline()
file.close()

client = discord.Client()

pickle_file = open("redistributed", "rb")
skin_dictionary = pickle.load(pickle_file)
pickle_file.close()

pickle_file = open("balances", "rb")
user_balances = pickle.load(pickle_file)
pickle_file.close()

users_to_unmute = []

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # this user ID could be replaced by something other than a single user
    if str(message.author.id) == "225105242969210880" and message.content.startswith("-retire"):
        msg = "Disconnecting from the server..."
        await message.channel.send(msg)
        sys.exit()
    # BALANCE
    if message.content == "-balance":
        try:
            msg = "${:,.2f}".format(round(user_balances[message.author.id], 2))
            await message.channel.send(msg)
        except:
            user_balances[message.author.id] = 0.0
            msg = "$0.00"
            await message.channel.send(msg)
    # STORE
    if message.content == "-store":
        msg = "Purchase options:\n-case\n     costs $2.50, rolls a new skin\n-disconnect [user]\n     costs $5.00, disconnects target user\n-mute [user] [duration]\n     costs $.15 per second, maximum of 300 seconds\n-vip [user-optional]\n     costs $100.00, access to vip channels, a user input buys it for another user"
        await message.channel.send(msg)
    # CASE
    if message.content == "-case":
        try:
            b = user_balances[message.author.id]
        except:
            user_balances[message.author.id] = 0.00
            b = 0.00
        if user_balances[message.author.id] >= 2.50:
            user_balances[message.author.id] = user_balances[message.author.id] - 2.50
            msg = get_skin(message.author.id)
            await message.channel.send(msg)
        else:
            msg = "Your balance of ${:,.2f} is not sufficient to purchase a case".format(user_balances[message.author.id])
            await message.channel.send(msg)
    # MUTE
    if message.content.startswith("-mute"):
        pieces = re.findall(r"\[(.*?)\]", message.content)
        try:
            target = 0
            for member in message.channel.members:
                if member.display_name == pieces[0]:
                    target = member
            if target == 0:
                msg = "User not found"
                await message.channel.send(msg)
                return
            duration = round(float(pieces[1]), 2)
            if duration > 300.00:
                duration = 300.00
            if duration < 0:
                msg = "Please use a valid mute duration in seconds"
                await message.channel.send(msg)
                return
            cost = duration * .15
            if cost > user_balances[message.author.id]:
                msg = "Your balance of ${:,.2f} is not sufficient to mute for this duration".format(user_balances[message.author.id])
                await message.channel.send(msg)
                return
            else:
                user_balances[message.author.id] = user_balances[message.author.id] - cost
            await target.edit(mute=True)
            msg = "Muted user " + target.nick + " for " + str(duration) + " seconds"
            await message.channel.send(msg)
            await asyncio.sleep(float(pieces[1]))
            try:
                channel_check = target.voice.channel.id
            except:
                channel_check = 0
            if channel != 0:
                await target.edit(mute=False)
            else:
                users_to_unmute.append(target.id)
        except:
            msg = "Please format your command in this way: -mute [user] [duration]"
            await message.channel.send(msg)
    # AWARD
    if str(message.author.id) == "225105242969210880" and message.content.startswith("-award"):
        pieces = re.findall(r"\[(.*?)\]", message.content)
        try:
            target_id = 0
            for member in message.channel.members:
                if member.display_name == pieces[0]:
                    target_id = member.id
            if target_id == 0:
                msg = "User not found"
                await message.channel.send(msg)
                return
            user_balances[target_id] = user_balances[target_id] + round(float(pieces[1]), 2)
            msg = "Awarded ${:,.2f} to ".format(round(float(pieces[1])), 2) + pieces[0] + "!"
            await message.channel.send(msg)
        except:
            msg = "Command formatted incorrectly"
            await message.channel.send(msg)
    # OLD SKIN COMMAND
    # if message.content == "-skin":
    # 	msg = get_skin()
    # 	await message.channel.send(msg)
    # SAVE
    if message.content == "-save":
        filename = "balances"
        outfile = open(filename, "wb")
        pickle.dump(user_balances, outfile)
        outfile.close()
        msg = "User balance data has been saved"
        await message.channel.send(msg)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        before = before.channel.id
    except:
        before = 0
    try:
        after = after.channel.id
    except:
        after = 0
    if after != 0 and member.id in users_to_unmute:
        await member.edit(mute=False)
    try:
        if after == 525107177065545744 and before != 525107177065545744 and member.id != 525133586047827980:
            channel = member.voice.channel
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio(executable="C:/Program Files (x86)/FFmpeg for Audacity/ffmpeg.exe", source="C:/Users/bmcka/Desktop/welcome.mp3"))
            await asyncio.sleep(3.5)
            await voice.disconnect()
    except:
        pass

client.run(TOKEN)