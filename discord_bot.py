#dependencies:
#python3 -m pip install -U discord.py
#pip install jikanpy

import json
import shutil
import requests
import os
from random import randrange
import discord
from discord.ext import commands, tasks
from jikanpy import AioJikan

intents = discord.Intents.default()
intents.members = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
ENV_STATIC = os.path.join(APP_ROOT, '.env')

with open(ENV_STATIC) as env_file:
    token = env_file.readline().strip()

bot = commands.Bot("!", intents=intents)

def get_hentai():

    no_valid_tag = True
    #run loop until a valid tag is found
    while no_valid_tag:
        #get random tag to find hentai with
        random_tag = ""
        i = 0
        while i < 4:
            random_tag += str(randrange(10))
            i += 1

        #find hentai id with the random tag
        URL_search_tag = "https://nhentai.net/api/galleries/tagged?tag_id={}".format(random_tag)
        tag = requests.get(url = URL_search_tag)
        tag_data = tag.json()
        if "result" in tag_data.keys():
            no_valid_tag = False

    media_data_list = tag_data["result"]
    media_id_data = media_data_list[randrange(len(media_data_list))]
    id = media_id_data["id"]
    return id

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Helloo!!")
        emoji = "<:Cat4:725330104011587604>"
        await message.add_reaction(emoji)


    if message.content.startswith("!search"):

        aio_jikan = AioJikan()
        search_words = message.content.replace("!search ", "")
        result_dict = await aio_jikan.search("anime", search_words)
        await aio_jikan.close()

        result_list = result_dict.get("results")

        #range tells how many animes from search will be presented
        if len(result_list) == 0:
            return
        for i in range(1):
            serie_dict = result_list[i]

            #delete unwanted info
            keys_to_remove = ["mal_id", "image_url", "members", "rated", "airing"]
            for key in keys_to_remove:
                del serie_dict[key]

            #tells if show is airing or not
            if serie_dict.get("airing") == True:
                air_prompt = "Show is currently airing"
            else:
                air_prompt = "Not currently airing"

            #sends information to discord channel
            anime_str = "```\nTitle: {}\nSynopsis: {}\nType: {}\nEpisodes: {}\nScore: {}\nAiring: {}\nAiring date: {} - {}\n```".format(serie_dict.get("title"), serie_dict.get("synopsis"), serie_dict.get("type"), serie_dict.get("episodes"), serie_dict.get("score"), air_prompt,serie_dict.get("start_date")[0:10],  serie_dict.get("end_date")[0:10])
            await message.channel.send(serie_dict.get("url"))
            await message.channel.send(anime_str)

    if message.content.startswith("!bonk"):

        horny_jail = bot.get_channel(486985950002544641)

        #bonk everyone on the same voice channel
        if message.content == "!bonk":
            for vchannel in message.guild.voice_channels:
                for member in vchannel.members:
                    if (not member.bot):
                        await member.move_to(horny_jail)

        if len(message.mentions) > 0:
            for member in message.mentions:
                await member.move_to(horny_jail)

        with requests.get("http://jaks.fi/bonk", stream=True) as r:
            if r.status_code != 200:
                await message.channel.send("BONK")
                return
            with open("img.png", "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        await message.channel.send(file=discord.File('img.png'))
        os.remove("img.png")

   

            

@bot.event
async def on_guild_channel_delete(channel):
    if channel.guild.id == 484443832856084500:
        channel_to_send = 484696393110519817 #meta
    elif channel.guild.id == 719608860599648286:
        channel_to_send = 719608860599648289 #yeet
    main_channel = bot.get_channel(channel_to_send)
    await main_channel.send("Channel {} was just yeeted".format(channel.name))

@bot.event
async def on_guild_channel_create(channel):
    if channel.guild.id == 484443832856084500:
        channel_to_send = 484696393110519817 #meta
    elif channel.guild.id == 719608860599648286:
        channel_to_send = 719608860599648289 #yeet
    main_channel = bot.get_channel(channel_to_send)
    await main_channel.send("Channel {} was just created. Have fun!".format(channel.name))

bot.run(token)