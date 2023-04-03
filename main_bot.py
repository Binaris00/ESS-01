#Essentials modules
from discord.ext import commands
import discord

#Optional modules and bot token and random descriptions when the bot is turn on
from token_pass import TOKEN, random_descriptions
from random import choice





intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='ess!', intents=intents)

@bot.event
async def on_ready():
    print(f'You connect correctly {bot.user}')
    try:
        #Extensions
        await bot.load_extension("user_info_things")
        
        #load all slash commands
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(choice(random_descriptions)))
        
    except Exception as e:
        print(e)



#Basic and simple commands
@bot.tree.command(name="ping", description="Basic Ping command")
async def ping(interation: discord.Interaction):
    await interation.response.send_message("Pong!", ephemeral=True)


#No Copy this command (It's only a joke with friends)
@bot.tree.command(name="no_context", description="Display a phrase without context (Joke command)")
async def no_context(interation: discord.Interaction):
   with open("no_context_messages.txt", "r", encoding="utf8") as file:
      file = file.read()
      file = file.splitlines()
      await interation.response.send_message(choice(file))


bot.run(TOKEN)