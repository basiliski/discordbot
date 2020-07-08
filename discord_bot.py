streamsource_text = "~ twist.moe\n+ muistaa mihin jäi\n+ clean interface\n+ hyvä laatu\n- joskus ruuhkaa ja bufferoi paljon\n\n~ animeultima.to\n+ Jaksot lataa nopeesti ja heti\n+ iso valikoima sarjoja\n- sivu ajoittain alhaalla\n- verkkosivu tosi hidas muuten\n\n~ animeflix.io\n+/- literally animeultima mutta muka hienommalla intefacella :smile:"
help_text = "Konnichiwa!!\n!hello = I'll greet you back\n!streaming = I'll tell you good anime streaming sites\n!search (anime name here) = I'll respond with url to Mal and some information\n!hentai = <:Meguminlewd:725330104065982464>"

import json
import requests
import os
from random import randrange
import discord
from discord.ext import commands
from jikanpy import AioJikan

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
ENV_STATIC = os.path.join(APP_ROOT, '.env')

with open(ENV_STATIC) as env_file:
    token = env_file.readline().strip()

client = discord.Client()

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

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!hentai"):

        id = get_hentai()
        #send hentai url to discord
        hentai_message = await message.channel.send("https://nhentai.net/g/{}/".format(id))
        emojii = "<:AquaThumbsUp:725330104200331334>>"
        await hentai_message.add_reaction(emojii)

    if message.content.startswith("!help"):
        await message.channel.send(help_text)

    if message.content.startswith("!hello"):
        await message.channel.send("Helloo!!")
        emoji = "<:Cat4:725330104011587604>"
        await message.add_reaction(emoji)

    if message.content.startswith("!streaming"):
        await message.channel.send(streamsource_text)

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

@client.event
async def on_guild_channel_delete(channel):
    main_channel = client.get_channel(719608860599648289)
    await main_channel.send("Channel {} was just yeeted".format(channel.name))

@client.event
async def on_guild_channel_create(channel):
    main_channel = client.get_channel(719608860599648289)
    await main_channel.send("Channel {} was just created. Have fun!".format(channel.name))


client.run(token)
