import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = "i'm bored as shit"
inLobby = False
inGame = False
requiredPlayers = 3
playerList = {}


class Error(Exception):
    """Base Error Class"""
    pass


class noLobbyException(Error):
    """Raised when a player tries to interact with a non-existent lobby."""
    pass


class alreadyJoinedException(Error):
    """Raised when a player tries to join a lobby twice."""
    pass


class notEnoughPlayersException(Error):
    """Raised when a player tries to start a game without enough players"""
    pass


class notInGameException(Error):
    """Raised when a command is run while not in game"""
    pass


bot = commands.Bot(command_prefix='!', description=description, case_insensitive=True)


@bot.event
async def on_ready():
    print("-------------\nWe're in, bitches\n-------------\n")


@bot.command(pass_context=True)
async def lobby(ctx):
    global inLobby
    global playerList

    # await ctx.message.delete()
    inLobby = True
    playerList[ctx.message.author.id] = ctx.message.author.display_name
    print('Trying to start game.')
    print('user ID ' + str(ctx.message.author.id) + ' added to players.')
    await ctx.send('@here, **' + ctx.message.author.display_name + '** is trying to start a game, type !join to join!')


@bot.command(pass_contest=True)
async def join(ctx):
    try:
        # await ctx.message.delete()
        global playerList
        if not inLobby:
            raise noLobbyException
        if ctx.message.author.id in playerList:
            raise alreadyJoinedException

        playerList[ctx.message.author.id] = ctx.message.author.display_name
        print('user ID ' + str(ctx.message.author.id) + ' added to players.')
        await ctx.send(ctx.message.author.display_name + ' has joined the game!')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried to join a non-existent lobby.')
        await ctx.send('No lobby created!')
    except alreadyJoinedException:
        print(ctx.message.author.display_name + ' tried to join twice.')
        await ctx.send('Already joined lobby!')


@bot.command(pass_context=True)
async def yeetlobby(ctx):
    try:
        # await ctx.message.delete()
        global inLobby, playerList
        if not inLobby:
            raise noLobbyException

        del playerList
        playerList = {}
        inLobby = False
        print('Yeeting lobby.')
        await ctx.send(ctx.message.author.display_name + ' has yote the lobby!')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried to yeet a non-existent lobby.')
        await ctx.send('No lobby created!')


@bot.command(pass_context=True)
async def players(ctx):
    try:
        # await ctx.message.delete()
        if not inLobby:
            raise noLobbyException
        print("Listing players.")
        await ctx.send("Players:")
        for player in playerList.values():
            print(player)
            await ctx.send(player)
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried listing players in a non-existent lobby.')
        await ctx.send('No lobby created!')


@bot.command(pass_context=True)
async def start(ctx):
    try:
        global inGame, inLobby
        if not inLobby:
            raise noLobbyException
        if len(playerList) < requiredPlayers:
            raise notEnoughPlayersException

        inLobby = False
        inGame = True
        await ctx.send('Starting game!')
        print('Starting game.')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried starting a game without a lobby.')
        await ctx.send('No lobby created!')
    except notEnoughPlayersException:
        print(ctx.message.author.display_name + ' tried starting a game without enough players.')
        await ctx.send('Not enough players!')


@bot.command(pass_context=True)
async def forceStop(ctx):
    try:
        global inGame, playerList
        if not inGame:
            raise notInGameException

        del playerList
        playerList = {}
        inGame = False
        await ctx.send('Stopping game!')
        print('Stopping game.')
    except notInGameException:
        print(ctx.message.author.display_name + ' tried closing a non-existent game.')
        await ctx.send('No game in progress!')


bot.run(TOKEN)
