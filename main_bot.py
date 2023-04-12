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
    """When the bot is turning on, load all extensions, load all slash commands and select a descriptions"""
    
    print(f'You connect correctly {bot.user}')
    try:
        #Extensions
        await bot.load_extension("user_info_things")
        await bot.load_extension("animals.animals_cats")
        await bot.load_extension("animals.animals_dogs")
        await bot.load_extension("personal_things") #This is my personal commands and other things
        await bot.load_extension("decoration_roles")
        
        #load all slash commands
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(choice(random_descriptions)))
        
    except Exception as e:
        print(e)



#Basic and simple commands
@bot.tree.command(name="ping", description="Ping Pong")
async def ping(interaction: discord.Interaction):
    """Send a ephemeral message to user saying pong """
    
    await interaction.response.send_message("Pong!", ephemeral=True)

#Example how to make a api request and send, example about a very basic 8ball api
@bot.tree.command(name="8ball", description="say a question and 8ball say your fortune")
@discord.app_commands.describe(message='The member you want to get the joined date from; defaults to the user who uses the command')
async def eightball(interaction: discord.Interaction, message: str):
    """Send a api request to eightball api and send the answer

    Args:
        interation (discord.Interaction): All user information when execute a action
        message (str): user question
    """
    async with aiohttp.ClientSession() as session:
        async with (session.get("https://www.eightballapi.com/api")) as response:
            response = await response.json()
            await interaction.response.send_message(response["reading"])

@bot.tree.command(name="say", description="Type a message that you would like the bot to say.")
async def say(interaction: discord.Interaction, message: str):
    try:
        await interaction.response.send_message(message)
    except:
        await interaction.response.send_message("I don't want to say that!!", ephemeral=True)



# I need to create a message error if the user don't have permissions to use the commands
@bot.tree.command(name="ban", description="Ban any user for your guild")
@discord.app_commands.checks.has_permissions(ban_members=True)
async def guild_ban(interaction: discord.Interaction, user: discord.Member, reason: str=None, delete_message_seconds: int=None): #Don't use delete_message_days
    if delete_message_seconds == None:
        delete_message_seconds = 1
    elif reason == None:
        reason = "No reason"

    await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=delete_message_seconds)
    await interaction.response.send_message(f"{user.name} Banned")

@bot.tree.command(name="kick", description="Kick any user for your guild")
async def guild_kick(interaction: discord.Interaction, user: discord.Member, reason: str=None):
    if reason == None:
        reason = "No reason"
    await interaction.guild.kick(user=user, reason=reason)
    await interaction.response.send_message(f"{user.name} Kicked")



#Logs
@bot.tree.command(name="log_messages", description="Send messages logs on a specific channel")
@discord.app_commands.checks.has_permissions(view_audit_log=True)
async def channel_name_finder(interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
    if confirmation:
        await interaction.response.send_message(f"Now I send the messages logs in {channel.name}")
        
        @bot.event
        async def on_message_edit(before, after):
            embed=discord.Embed(title="Edited Message Log", description=f"From {before.author} in {before.channel.name}", color=0xff0000)
            embed.add_field(name="Before", value=before.content, inline=True)
            embed.add_field(name="After", value=after.content, inline=True)
            await channel.send(embed=embed)
        
        @bot.event
        async def on_message_delete(message):
            embed=discord.Embed(title="Deleted Message Log", description=f"From {message.author} in {message.channel.name}", color=0xff0000)
            embed.add_field(name="Deleted Message:", value=message.content)
            await channel.send(embed=embed)
    else:
        await interaction.response.send_message(f"Now not appear messages logs in {channel.name}")
    
bot.run(TOKEN)