import os

from random import randrange, choice
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = "i'm bored as shit"
inLobby = False
inGame = False
isReverse = False
toDraw = 0
requiredPlayers = 2
playerIDs = []
playerNames = []
decks = {}
turn = 0
lastCard = []
channels = [
    712763747315220561, 712763764922908794, 712763848133836870, 712763863384457256, 712763878643073065,
    712763898356564048, 712763914747904091, 712763929020858438, 712763945525575700, 712763957852504197
]
cards = [
    ['Red 0', 0, 0], ['Red 1', 0, 1], ['Red 1', 0, 1], ['Red 2', 0, 2], ['Red 2', 0, 2], ['Red 3', 0, 3],
    ['Red 3', 0, 3], ['Red 4', 0, 4], ['Red 4', 0, 4], ['Red 5', 0, 5], ['Red 5', 0, 5], ['Red 6', 0, 6],
    ['Red 6', 0, 6], ['Red 7', 0, 7], ['Red 7', 0, 7], ['Red 8', 0, 8], ['Red 8', 0, 8], ['Red 9', 0, 9],
    ['Red 9', 0, 9], ['Red Draw 2', 0, 10], ['Red Draw 2', 0, 10], ['Red Skip', 0, 11], ['Red Skip', 0, 11],
    ['Red Reverse', 0, 12], ['Red Reverse', 0, 12], ['Green 0', 1, 0], ['Green 1', 1, 1], ['Green 1', 1, 1],
    ['Green 2', 1, 2], ['Green 2', 1, 2], ['Green 3', 1, 3], ['Green 3', 1, 3], ['Green 4', 1, 4], ['Green 4', 1, 4],
    ['Green 5', 1, 5], ['Green 5', 1, 5], ['Green 6', 1, 6], ['Green 6', 1, 6], ['Green 7', 1, 7], ['Green 7', 1, 7],
    ['Green 8', 1, 8], ['Green 8', 1, 8], ['Green 9', 1, 9], ['Green 9', 1, 9], ['Green Draw 2', 1, 10],
    ['Green Draw 2', 1, 10], ['Green Skip', 1, 11], ['Green Skip', 1, 11], ['Green Reverse', 1, 12],
    ['Green Reverse', 1, 12], ['Yellow 0', 2, 0], ['Yellow 1', 2, 1], ['Yellow 1', 2, 1], ['Yellow 2', 2, 2],
    ['Yellow 2', 2, 2], ['Yellow 3', 2, 3], ['Yellow 3', 2, 3], ['Yellow 4', 2, 4], ['Yellow 4', 2, 4],
    ['Yellow 5', 2, 5], ['Yellow 5', 2, 5], ['Yellow 6', 2, 6], ['Yellow 6', 2, 6], ['Yellow 7', 2, 7],
    ['Yellow 7', 2, 7], ['Yellow 8', 2, 8], ['Yellow 8', 2, 8], ['Yellow 9', 2, 9], ['Yellow 9', 2, 9],
    ['Yellow Draw 2', 2, 10], ['Yellow Draw 2', 2, 10], ['Yellow Skip', 2, 11], ['Yellow Skip', 2, 11],
    ['Yellow Reverse', 2, 12], ['Yellow Reverse', 2, 12], ['Blue 0', 3, 0], ['Blue 1', 3, 1], ['Blue 1', 3, 1],
    ['Blue 2', 3, 2], ['Blue 2', 3, 2], ['Blue 3', 3, 3], ['Blue 3', 3, 3], ['Blue 4', 3, 4], ['Blue 4', 3, 4],
    ['Blue 5', 3, 5], ['Blue 5', 3, 5], ['Blue 6', 3, 6], ['Blue 6', 3, 6], ['Blue 7', 3, 7], ['Blue 7', 3, 7],
    ['Blue 8', 3, 8], ['Blue 8', 3, 8], ['Blue 9', 3, 9], ['Blue 9', 3, 9], ['Blue Draw 2', 3, 10],
    ['Blue Draw 2', 3, 10], ['Blue Skip', 3, 11], ['Blue Skip', 3, 11], ['Blue Reverse', 3, 12],
    ['Blue Reverse', 3, 12], ['Wild Card', 4, 13], ['Wild Card', 4, 13], ['Wild Card', 4, 13], ['Wild Card', 4, 13],
    ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14], ['Wild Draw 4', 4, 14]
]
startCards = [
    ['Red 0', 0, 0], ['Red 1', 0, 1], ['Red 1', 0, 1], ['Red 2', 0, 2], ['Red 2', 0, 2], ['Red 3', 0, 3],
    ['Red 3', 0, 3], ['Red 4', 0, 4], ['Red 4', 0, 4], ['Red 5', 0, 5], ['Red 5', 0, 5], ['Red 6', 0, 6],
    ['Red 6', 0, 6], ['Red 7', 0, 7], ['Red 7', 0, 7], ['Red 8', 0, 8], ['Red 8', 0, 8], ['Red 9', 0, 9],
    ['Red 9', 0, 9], ['Green 0', 1, 0], ['Green 1', 1, 1], ['Green 1', 1, 1],
    ['Green 2', 1, 2], ['Green 2', 1, 2], ['Green 3', 1, 3], ['Green 3', 1, 3], ['Green 4', 1, 4], ['Green 4', 1, 4],
    ['Green 5', 1, 5], ['Green 5', 1, 5], ['Green 6', 1, 6], ['Green 6', 1, 6], ['Green 7', 1, 7], ['Green 7', 1, 7],
    ['Green 8', 1, 8], ['Green 8', 1, 8], ['Green 9', 1, 9], ['Green 9', 1, 9],
    ['Yellow 0', 2, 0], ['Yellow 1', 2, 1], ['Yellow 1', 2, 1], ['Yellow 2', 2, 2],
    ['Yellow 2', 2, 2], ['Yellow 3', 2, 3], ['Yellow 3', 2, 3], ['Yellow 4', 2, 4], ['Yellow 4', 2, 4],
    ['Yellow 5', 2, 5], ['Yellow 5', 2, 5], ['Yellow 6', 2, 6], ['Yellow 6', 2, 6], ['Yellow 7', 2, 7],
    ['Yellow 7', 2, 7], ['Yellow 8', 2, 8], ['Yellow 8', 2, 8], ['Yellow 9', 2, 9], ['Yellow 9', 2, 9],
    ['Blue 0', 3, 0], ['Blue 1', 3, 1], ['Blue 1', 3, 1],
    ['Blue 2', 3, 2], ['Blue 2', 3, 2], ['Blue 3', 3, 3], ['Blue 3', 3, 3], ['Blue 4', 3, 4], ['Blue 4', 3, 4],
    ['Blue 5', 3, 5], ['Blue 5', 3, 5], ['Blue 6', 3, 6], ['Blue 6', 3, 6], ['Blue 7', 3, 7], ['Blue 7', 3, 7],
    ['Blue 8', 3, 8], ['Blue 8', 3, 8], ['Blue 9', 3, 9], ['Blue 9', 3, 9]
]
colours = ['red', 'green', 'yellow', 'blue']


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


class alreadyInGameException(Error):
    """Raised when a player tries to start a second lobby"""
    pass


class notTurnException(Error):
    """Raised when a player tries running a command when it isn't their turn"""
    pass


bot = commands.Bot(command_prefix='!', description=description, case_insensitive=True)


def randCard():
    cardNum = randrange(0, 108)
    card = cards[cardNum]
    return card


async def stopEverything(ctx):
    global playerIDs, decks, playerNames, inGame, turn, isReverse, lastCard, toDraw
    i = 0
    for playerID in playerIDs:
        i += 1
        member = await commands.MemberConverter().convert(ctx, str(playerID))
        role = get(member.guild.roles, name=("Player " + str(i)))
        await member.remove_roles(role)
    playerIDs = []
    decks = {}
    playerNames = []
    turn = 0
    lastCard = []
    toDraw = 0
    isReverse = False
    inGame = False


def isTurn(ctx):
    return ctx.message.author.id == playerIDs[turn]


async def displayCards(ctx):
    playerNo = playerIDs.index(ctx.author.id)
    channel = bot.get_channel(channels[playerNo])
    await channel.purge(limit=50)
    msg = "**Your cards**:\n"
    i = 1
    for card in decks[ctx.author.id]:
        msg = msg + str(i) + ': ' + card[0] + '\n'
        i += 1
    await channel.send(msg)


@bot.event
async def on_ready():
    print("-------------\nWe're in, bitches\n-------------\n")


@bot.command(pass_context=True)
async def lobby(ctx):
    try:
        global inLobby, playerIDs, playerNames

        if inLobby or inGame:
            raise alreadyInGameException
        inLobby = True
        playerIDs.append(ctx.message.author.id)
        playerNames.append(ctx.message.author.display_name)
        print('Trying to start game.')
        print('user ID ' + str(ctx.message.author.id) + ' added to players.')
        await ctx.send(
            '@here, **' + ctx.message.author.display_name + '** is trying to start a game, type !join to join!')
    except alreadyInGameException:
        await ctx.send("There's already a lobby you bastard")
    except Exception as e:
        print(e)


@bot.command(pass_contest=True)
async def join(ctx):
    try:
        global playerIDs, playerNames

        if not inLobby:
            raise noLobbyException
        if ctx.message.author.id in playerIDs:
            raise alreadyJoinedException

        playerIDs.append(ctx.message.author.id)
        playerNames.append(ctx.message.author.display_name)
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
        global inLobby, playerIDs, playerNames
        if not inLobby:
            raise noLobbyException

        playerIDs = []
        playerNames = []
        inLobby = False
        print('Yeeting lobby.')
        await ctx.send(ctx.message.author.display_name + ' has yote the lobby!')
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried to yeet a non-existent lobby.')
        await ctx.send('No lobby created!')


@bot.command(pass_context=True)
async def players(ctx):
    try:
        if not inLobby and not inGame:
            raise noLobbyException
        print("Listing players.")
        await ctx.send("Players:")
        for player in playerNames:
            print(player)
            await ctx.send(player)
    except noLobbyException:
        print(ctx.message.author.display_name + ' tried listing players in a non-existent lobby.')
        await ctx.send('No lobby created!')


@bot.command(pass_context=True)
async def start(ctx):
    try:
        global inGame, inLobby, decks, lastCard
        if not inLobby:
            raise noLobbyException
        if len(playerIDs) < requiredPlayers:
            raise notEnoughPlayersException

        inLobby = False
        inGame = True
        await ctx.send('Starting game!')
        print('Starting game.')
        i = 0

        for playerID in playerIDs:
            # Give role
            i += 1
            member = await commands.MemberConverter().convert(ctx, str(playerID))
            role = get(member.guild.roles, name=("Player " + str(i)))

            # Deal cards
            channel = bot.get_channel(channels[i - 1])
            await channel.purge(limit=50)

            await member.add_roles(role)
            decks[playerID] = []
            msg = '**Your cards**:\n'
            for x in range(7):
                card = randCard()
                decks[playerID].append(card)
                msg = msg + str(x + 1) + ': ' + card[0] + '\n'
            await channel.send(msg)

        lastCard = choice(startCards)
        await ctx.send('**First Card**:')
        await ctx.send(lastCard[0])

    except noLobbyException:
        print(ctx.message.author.display_name + ' tried starting a game without a lobby.')
        await ctx.send('No lobby created!')
    except notEnoughPlayersException:
        print(ctx.message.author.display_name + ' tried starting a game without enough players.')
        await ctx.send('Not enough players!')


@bot.command(pass_context=True)
async def play(ctx, cardNo: int):
    try:
        global decks, lastCard, turn, playerIDs, colours, toDraw, isReverse
        if not isTurn(ctx):
            raise notTurnException
        # If card is valid
        if decks[ctx.author.id][cardNo - 1][1] == lastCard[1] or decks[ctx.author.id][cardNo - 1][2] == lastCard[2] or \
                decks[ctx.author.id][cardNo - 1][1] == 4:

            await ctx.send('Card played: ' + decks[ctx.author.id][cardNo - 1][0])
            lastCard = decks[ctx.author.id][cardNo - 1]

            # Set card abilities
            if decks[ctx.author.id][cardNo - 1][2] == 10:
                toDraw = 2
                if isReverse:
                    turn -= 1
                else:
                    turn += 1
            elif decks[ctx.author.id][cardNo - 1][2] == 11:
                if isReverse:
                    turn -= 2
                else:
                    turn += 2
            elif decks[ctx.author.id][cardNo - 1][2] == 12:
                isReverse = not isReverse
                if isReverse:
                    turn -= 1
                else:
                    turn += 1
            elif decks[ctx.author.id][cardNo - 1][2] == 14:
                toDraw = 4
                if isReverse:
                    turn -= 1
                else:
                    turn += 1
            else:
                if isReverse:
                    turn -= 1
                else:
                    turn += 1

            # Deal with wildcards
            if decks[ctx.author.id][cardNo - 1][1] == 4:
                await ctx.send('What colour should be played next?')

                def check(author):
                    def innerCheck(message):
                        return message.content.lower() in colours and message.author == author

                    return innerCheck

                msg = await bot.wait_for('message', check=check(ctx.author))
                lastCard[1] = colours.index(msg.content.lower())
                await ctx.send('Next card should now be: **' + str(colours[lastCard[1]]).capitalize() + '**')

            # Check turns
            if turn < 0:
                turn += len(playerIDs)
            if turn > (len(playerIDs) - 1):
                turn -= len(playerIDs)

            del decks[ctx.author.id][cardNo - 1]
            await displayCards(ctx)
            
            # Check win condition
            if len(decks[ctx.author.id]) == 0:
                member = ctx.author
                role = get(member.guild.roles, name="Uno God")
                last_member = role.members[0]
                await last_member.remove_roles(role)
                await member.add_roles(role)
                await ctx.send('**' + str(ctx.author) + ' got the winner winner chicken dinner and is the uno God!**')
                await ctx.send('Type !lobby to start another game.')
                await stopEverything(ctx)

            # Draw cards
            if toDraw != 0:
                for x in range(toDraw):
                    card = randCard()
                    decks[playerIDs[turn]].append(card)
                channel = bot.get_channel(channels[turn])
                await channel.purge(limit=50)
                msg = "**Your cards**:\n"
                i = 1
                for card in decks[playerIDs[turn]]:
                    msg = msg + str(i) + ': ' + card[0] + '\n'
                    i += 1
                await channel.send(msg)
                print(str(toDraw) + ' cards drawn for ' + str(playerIDs[turn]))
                if isReverse:
                    turn -= 1
                else:
                    turn += 1
                toDraw = 0

                # Check turns
                if turn < 0:
                    turn += len(playerIDs)
                if turn > (len(playerIDs) - 1):
                    turn -= len(playerIDs)

            member = await commands.MemberConverter().convert(ctx, str(playerIDs[turn]))
            await ctx.send("It's now " + member.display_name + "'s turn!")

        else:
            print('Card cannot be played.')
            await ctx.send('Try another card, basard')
    except notTurnException:
        await ctx.send("It's not your turn, greedy bitchard")
        print('Not correct turn.')
    except Exception as e:
        print(e)


@bot.command(pass_context=True)
async def draw(ctx):
    try:
        global decks, channels, playerIDs
        if not isTurn(ctx):
            raise notTurnException
        print(str(ctx.author.id) + " is drawing a card")
        card = randCard()
        decks[ctx.author.id].append(card)
        await displayCards(ctx)
    except notTurnException:
        await ctx.send("It's not your turn, greedy bitchard")
        print('Not correct turn.')
    except Exception as e:
        print(e)


@bot.command(pass_context=True)
async def forceStop(ctx):
    try:
        global inGame, playerNames, playerIDs, decks
        if not inGame:
            raise notInGameException

        await stopEverything(ctx)

        await ctx.send('Stopping game!')
        print('Stopping game.')
    except notInGameException:
        print(ctx.message.author.display_name + ' tried closing a non-existent game.')
        await ctx.send('No game in progress!')


bot.run(TOKEN)
