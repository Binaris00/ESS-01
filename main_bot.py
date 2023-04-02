import discord
from token_pass import TOKEN, random_descriptions
from discord.ext import commands

#optional modules
import random
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='ess!', intents=intents)

@bot.event
async def on_ready():
    print(f'You connect correctly {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Commands loaded correctly: {len(synced)}")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(random.choice(random_descriptions)))
        
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Basic Ping command")
async def ping(interation: discord.Interaction):
    await interation.response.send_message("Pong!", ephemeral=True)


@bot.tree.command(name="simple_calculator", description="Use a operation and get a answer")
async def calculator(interation: discord.Interaction, operation: str):
    """Just a simple calculator with eval()

    Args:
        interation (discord.Interaction): .
        operation (str): Operation to do
    """
    try:
        result = eval(operation)
        await interation.response.send_message(result)
    except:
        await interation.response.send_message("Syntax Error!")

@bot.tree.command(name="user", description="display the user info")
async def calculator(interation: discord.Interaction, user: discord.Member= None):
    if user is None:
        data = interation.user.name
    else:
        data = user.name
    await interation.response.send_message(data)

@bot.tree.command(name="no_context", description="Display a phrase without context (Joke command)")
async def no_context(interation: discord.Interaction):
   with open("no_context_messages.txt", "r", encoding="utf8") as file:
      file = file.read()
      file = file.splitlines()
      await interation.response.send_message(random.choice(file))
      
if __name__ == "__main__":
    bot.run(TOKEN)