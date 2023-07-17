import discord
from discord import app_commands
from discord.ext import commands
import os

import hackathons as h

from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix = "!", case_insensitive = True, intents=discord.Intents.all())

discord_token = os.getenv('BOT_TOKEN')

if discord_token is None:
    print("Bot token not found")
    exit()

def hackathonString(hack):
    hString = f"**{hack.name}**, {hack.location} (*{hack.start_string} - {hack.end_string}*) : __{hack.status}__\n{hack.link}\n\n"
    return hString  

@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commmand(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello", description="Say hello to Dog the Bird!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}! 👋")

@bot.tree.command(name="bye", description="Say bye to Dog the Bird!")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bye, {interaction.user.mention}! 👋")

@bot.tree.command(name="crazy", description="Crazy?")
async def crazy(interaction: discord.Interaction):
    await interaction.response.send_message(f"Crazy?\nI was crazy once...\nThey locked me in a room.\nA rubber room.\nA rubber room with rats.\nAnd rats make me crazy..")

@bot.tree.command(name="hackathons", description="View some of MLH's 2024 Season Hackathons!")
@app_commands.describe(specifier = "Some specifier. Ex: upcoming, ongoing, ended, online, or a city or state")
# TODO : add more args soon
# @app_commands.describe(number_of_hackathons = "The maximum number of hackathons you want the bot to output. Set to 15 by default. The highest is 12.")
async def hackathons(interaction: discord.Interaction, specifier:str = ""):
    stringToSend = ""
    hackathonCount = 0
    cities = set()
    states = set()
    for hackathon in h.hackathons:
        cities.add((hackathon.city))
        states.add((hackathon.state))

    acceptedArgs = ["", "upcoming", "ongoing", "ended", "online"] + list(cities) + list(states)

    # convert all args to lower case and remove spaces
    acceptedArgs = [(argument.lower()).replace(" ", "") for argument in acceptedArgs]

    # makings arg case insensitive and removing spaces
    specifier = specifier.lower().replace(" ", "")
    if specifier not in acceptedArgs:
        await interaction.response.send_message("Invalid specifier")
        return
    
    for hackathon in h.hackathons:
        # if no arg was provided display the upto 15 soonest hackathons (Displays both upcoming and ongoing)
        if specifier == "" and hackathon.status != "Hackathon has ended.":
            stringToSend += hackathonString(hackathon)
            hackathonCount += 1
        # if arg is upcoming display upto 15 soonest hackathons (Only display upcoming)
        elif specifier == "upcoming" and hackathon.status != "Hackathon has ended." and hackathon.status != "Hackathon is ongoing!":
            stringToSend += hackathonString(hackathon)
            hackathonCount += 1
        # if arg is ongoing display upto 15 soonest hackathons (Only display ongoing)
        elif specifier == "ongoing" and hackathon.status == "Hackathon is ongoing!":
            stringToSend += hackathonString(hackathon)
            hackathonCount += 1
        # if arg is ended display upto 15 ended hackathons
        elif specifier == "ended" and hackathon.status == "Hackathon has ended.":
            stringToSend += hackathonString(hackathon)
            hackathonCount += 1
        # if arg is online display upto 15 hackathons that are online only
        elif specifier == "online" and hackathon.location == "Everywhere, Worldwide":
            stringToSend += hackathonString(hackathon)
            hackathonCount += 1
        else:
            if (hackathon.city.lower().replace(" ", "")) == specifier or (hackathon.state.lower().replace(" ", "")) == specifier:
                stringToSend += hackathonString(hackathon)
                hackathonCount += 1

        if hackathonCount == 15:
            break
        
    if stringToSend == "":
        hackathonEmbed = discord.Embed(
            title="😵‍💫",
            description="No hackathons found that fit your specifications.",
            color=0xe33939
        )

    else:
        hackathonEmbed = discord.Embed(
            title="🎉",
            description=stringToSend,
            color=0x79AEFE,
            url="https://mlh.io/seasons/2024/events"
        )
        
    hackathonEmbed.set_footer(text="View the full list of MLH's 2024 Season Hackathons here : https://mlh.io/seasons/2024/events")
    await interaction.response.send_message(embed=hackathonEmbed)

@bot.tree.command(name="help", description="Get help on how to use Dog the Bird's commands")
async def help(interaction: discord.Interaction):

    helpEmbed = discord.Embed(
        title="Help 📖",
        description="**Help Commands -**",
        color=0x79AEFE
    )

    helpEmbed.add_field(name="**/hackathons**", value="View up to 15 upcoming and/or ongoing hackathons.", inline=False)
    helpEmbed.add_field(name="**/hackathons some_specifier**", value="Replace some specifier with ongoing, upcoming, ended, online, or a location to view hackathons of that specific type. For example, `/hackathons upcoming` will show you upcoming hackathons.", inline=False)
    helpEmbed.add_field(name="**/hello**", value="Say hello to Dog the Bird!", inline=False)
    helpEmbed.add_field(name="**/bye**", value="Say bye to Dog the Bird!", inline=False)
    helpEmbed.add_field(name="**/crazy**", value="Crazy?", inline=False)

    avatar_url = getattr(interaction.user.avatar, 'url', None)
    
    helpEmbed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url)

    await interaction.response.send_message(embed=helpEmbed)
bot.run(discord_token)