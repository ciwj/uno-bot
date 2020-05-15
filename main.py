import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = "i'm bored as shit"
inLobby = False
playerList = set()
playerListNames = set()


class Error(Exception):
    """Base Error Class"""
    pass


class noLobbyException(Error):
    """Raised when a player tries to interact with a non-existent lobby."""
    pass


class alreadyJoined(Error):
    """Raised when a player tries to join a lobby twice."""


bot = commands.Bot(command_prefix='!', description=description, case_insensitive=True)


@bot.event
async def on_ready():
    print("-------------\nWe're in, bitches\n-------------\n")


@bot.command(pass_context=True)
async def start(ctx):
    global inLobby
    global playerList, playerListNames

    inLobby = True
    playerList.add(ctx.message.author.id)
    playerListNames.add(ctx.message.author.display_name)
    print('Trying to start game.')
    print('user ID ' + str(ctx.message.author.id) + ' added to players.')
    await ctx.send('@here, **' + ctx.message.author.display_name + '** is trying to start a game, type !join to join!')


@bot.command(pass_contest=True)
async def join(ctx):
    try:
        global playerListNames, playerList
        if not inLobby:
            raise noLobbyException
        if ctx.message.author.id in playerList:
            raise alreadyJoined

        playerList.add(ctx.message.author.id)
        playerListNames.add(ctx.message.author.display_name)
        print('user ID ' + str(ctx.message.author.id) + ' added to players.')
        await ctx.send(ctx.message.author.display_name + ' has joined the game!')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried to join a non-existent lobby.')
        await ctx.send('No lobby created!')
    except alreadyJoined:
        print(ctx.message.author.display_name + ' tried to join twice.')
        await ctx.send('Already joined lobby!')


@bot.command(pass_context=True)
async def yeetlobby(ctx):
    try:
        global inLobby, playerList, playerListNames
        if not inLobby:
            raise noLobbyException

        playerListNames = set()
        playerList = set()
        inLobby = False
        print('Yeeting lobby.')
        await ctx.send(ctx.message.author.display_name + ' has yote the lobby!')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried to yeet a non-existent lobby.')
        await ctx.send('No lobby created!')


@bot.command(pass_context=True)
async def players(ctx):
    try:
        if not inLobby:
            raise noLobbyException
        print("Listing players.")
        await ctx.send("Players:")
        for player in playerListNames:
            print(player)
            await ctx.send(player)
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried listing players in a non-existent lobby.')
        await ctx.send('No lobby created!')


bot.run(TOKEN)
