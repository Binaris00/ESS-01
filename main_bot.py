#Essentials modules
from discord.ext import commands
import discord

#Optional modules and bot token and random descriptions when the bot is turn on
from personal_things import TOKEN, random_descriptions
from random import choice

#For api request (Optional)
import aiohttp



intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='ess!', intents=intents)

@bot.event
async def on_ready():
    print(f'You connect correctly {bot.user}')
    try:
        #Extensions
        await bot.load_extension("user_info_things")
        await bot.load_extension("animals.animals_cats")
        await bot.load_extension("animals.animals_dogs")
        await bot.load_extension("personal_things") #This is my personal commands and other things
        #load all slash commands
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(choice(random_descriptions)))
        
    except Exception as e:
        print(e)



#Basic and simple commands
@bot.tree.command(name="ping", description="Basic Ping command")
async def ping(interation: discord.Interaction):
    await interation.response.send_message("Pong!", ephemeral=True)

#Example how to make a api request and send, example about a very basic 8ball api
@bot.tree.command(name="8ball", description="say a question and 8ball say your fortune")
async def eightball(interation: discord.Interaction, message: str):
    async with aiohttp.ClientSession() as session:
        async with (session.get("https://www.eightballapi.com/api")) as response:
            response = await response.json()
            await interation.response.send_message(response["reading"])

@bot.tree.command(name="say", description="Type a message that you would like the bot to say.")
async def say(interation: discord.Interaction, message: str):
    try:
        await interation.response.send_message(message)
    except:
        await interation.response.send_message("I don't want to say that!!")
bot.run(TOKEN)