streamsource_text = "~ twist.moe\n+ muistaa mihin jäi\n+ clean interface\n+ hyvä laatu\n- joskus ruuhkaa ja bufferoi paljon\n\n~ animeultima.to\n+ Jaksot lataa nopeesti ja heti\n+ iso valikoima sarjoja\n- sivu ajoittain alhaalla\n- verkkosivu tosi hidas muuten\n\n~ animeflix.io\n+/- literally animeultima mutta muka hienommalla intefacella :smile:"
help_text = "Konnichiwa!!\n!hello = I'll greet you back\n!streaming = I'll tell you good anime streaming sites\n!search (anime name here) = I'll respond with url to Mal and some information\n!hentai = <:Meguminlewd:725330104065982464>"

import json
import requests
import os
from random import randrange
import discord
from discord.ext import commands, tasks
from jikanpy import AioJikan

bot = commands.Bot("!")

def get_covid():

    url = "https://api.covid19api.com/total/country/finland"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = response.text.encode('utf8')
    response = json.loads(response_json)
    latest_info = response[-1]
    yesterdays_info = response[-2]
    return latest_info, yesterdays_info

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

    if "@valocunts" in message.content:
        await message.add_reaction("<:valorant:711969962066968596>")

    if "weebs = pedos" in message.content.lower():
        await message.delete()

    if message.content.startswith("!covid"):

        latest_info, yesterdays_info = get_covid()
        await message.channel.send("PÄIVÄN KORONASETIT KOTIMAASSA\n```diff\n- {} uutta tapausta```\n```Confirmed: {}\nDeaths: {}\nRecovered: {}\nActive: {}\n```".format(latest_info["Confirmed"] - yesterdays_info["Confirmed"], latest_info["Confirmed"], latest_info["Deaths"], latest_info["Recovered"], latest_info["Active"]))

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

    if message.content.startswith("!bonk"):

        horny_jail = bot.get_channel(486985950002544641)

        #bonk everyone on the same voice channel
        if message.content == "!bonk":
            for vchannel in message.guild.voice_channels:
                for member in vchannel.members:
                    await member.move_to(horny_jail)

        users_to_bonk = message.content.replace("!bonk ", "")
        if len(message.mentions) > 0:
            for member in message.mentions:
                await member.move_to(horny_jail)
        
        await message.channel.send("BONK")

            

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

@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = bot.get_channel(484696393110519817)
    print(f"Got channel {message_channel}")
    latest_info, yesterdays_info = get_covid()
    await message_channel.send("PÄIVÄN KORONASETIT KOTIMAASSA\n```diff\n- {} uutta tapausta```\n```Confirmed: {}\nDeaths: {}\nRecovered: {}\nActive: {}\n```".format(latest_info["Confirmed"] - yesterdays_info["Confirmed"], latest_info["Confirmed"], latest_info["Deaths"], latest_info["Recovered"], latest_info["Active"]))

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


called_once_a_day.start()
bot.run(os.environ['DC_TOKEN'])
