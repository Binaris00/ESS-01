#Essentials modules
from discord.ext import commands
import discord
from asyncio import sleep
#Optional modules and bot token and random descriptions when the bot is turn on
from personal_things import TOKEN, random_descriptions
from random import choice

#For api request (Optional)
import aiohttp



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='ess!', intents=intents)
extensions = ["user_info_things", "animals.animals_cats", "animals.animals_dogs", "personal_things", "guild_logs", "economy_system", "tictactoe_game", "examples.buttons_example", "examples.tree_commands", "examples.select_menu"]

@bot.event
async def on_ready():
    """When the bot is turning on, load all extensions, load all slash commands and select a descriptions"""
    
    print(f'You connect correctly {bot.user}\n')
    try:
        #Loading Extensions 
        for extension in extensions:
            await bot.load_extension(extension)
            print(f"Loaded {extension} correctly")
        
        
        #load all slash commands
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(choice(random_descriptions)))
        
    except Exception as e:
        print(e)













#Basic and simple commands
@bot.tree.command(name="ping", description="Ping Pong")
async def ping(interaction: discord.Interaction):
    """Send a ephemeral embed to user saying pong """
    embed = discord.Embed(title="Ping 🏓", description="Pong 🏓", color=discord.Color.red())
    await interaction.response.send_message(embed=embed, ephemeral=True)


#Example how to make a api request and send and a example about a very basic 8ball api
@bot.tree.command(name="8ball", description="say a question and 8ball say your fortune")
@discord.app_commands.describe(message='Your question to 8ball')
async def eightball(interaction: discord.Interaction, message: str):
    """Send a api request to eightball api and send the answer"""
    async with aiohttp.ClientSession() as session:
        async with (session.get("https://www.eightballapi.com/api")) as response:
            response = await response.json()
            await interaction.response.send_message(response["reading"])

@eightball.error
async def eightball_error(interaction: discord.Interaction, error):
    embed = discord.Embed(title="Eightball Error", description="The Eightball can't hear you, please try again in 5 minutes...")
    await interaction.response.send_message(embed=embed, ephemeral=True)




@bot.tree.command(name="say", description="Type a message that you would like the bot to say.")
@discord.app_commands.describe(message="The message you want I say")
async def say(interaction: discord.Interaction, message: str):
    """User send a message and the bot repeat this message"""
    try:
        await interaction.response.send_message(message)
    except:
        await interaction.response.send_message("I don't want to say that!!", ephemeral=True)




@bot.tree.command(name="ban", description="Ban any user for your guild")
@discord.app_commands.checks.has_permissions(ban_members=True)
@discord.app_commands.describe(user="User to ban for your guild", reason= "If you want write a reason for this ban",  delete_message_seconds="Delete messages for this user")
async def guild_ban(interaction: discord.Interaction, user: discord.Member, reason: str=None, delete_message_seconds: int=None): #Don't use delete_message_days because this not working anymore
    if delete_message_seconds == None:
        delete_message_seconds = 1
    elif reason == None:
        reason = "No reason"

    await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=delete_message_seconds)
    await interaction.response.send_message(f"{user.name} Banned")

@guild_ban.error
async def guild_ban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permissions to do this!!", ephemeral=True)
        
        
        
        
@bot.tree.command(name="kick", description="Kick any user for your guild")
@discord.app_commands.describe(user="User to kick for you guild", reason="If you want write a reason for this kick")
@discord.app_commands.checks.has_permissions(kick_members=True)
async def guild_kick(interaction: discord.Interaction, user: discord.Member, reason: str=None):
    if reason == None:
        reason = "No reason"
    await interaction.guild.kick(user=user, reason=reason)
    await interaction.response.send_message(f"{user.name} Kicked")

@guild_kick.error
async def guild_kick_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permissions to do this!!", ephemeral=True)




#This command only work for bans after invite the bot
@bot.tree.command(name="ban_list", description="See all users banned from your guild")
@discord.app_commands.checks.has_permissions(ban_members=True)
async def guild_ban_list(interaction: discord.Interaction):
    embed = discord.Embed(title="Banned Members", description="Banned Members from this guild", color=discord.Color.red())
    async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.ban):
        embed.add_field(name=f"{entry.user} Banned", value=f"{entry.target}")
    await interaction.response.send_message(embed=embed)

@guild_ban_list.error
async def guild_ban_list(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to do this", ephemeral=True)


@bot.tree.command(name="reminder", description="I remember any thing for you")
async def reminder(interaction: discord.Interaction, reason: str,  seconds: float=None, minutes: float=None, hours: float=None):    
    if seconds == None:
        seconds = 0
    elif minutes != None:
        seconds += minutes * 60
        if hours != None:
            seconds += hours * 3600
    elif seconds == 0 and minutes == None and hours == None:
        await interaction.response.send_message("Please select any second, minute or hour", ephemeral=True)
    embed = discord.Embed(title="Reminder Created", description=f"Reason: {reason}")
    embed.add_field(name="Time", value=seconds)
    await interaction.response.send_message(embed=embed)
    
    await sleep(seconds)
    embed = discord.Embed(title=f"Reminder {interaction.user.display_name}", description=f"Reason: {reason}", color=discord.Color.random)
    await interaction.channel.send(interaction.user.mention)
    await interaction.channel.send(embed=embed)





@bot.tree.command(name="purge", description="Eliminate X messages in channel")
@discord.app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, channel:discord.TextChannel=None, limit: int= 100):
    if channel == None:
        channel = interaction.message.channel
    await interaction.response.send_message("Purge in process", ephemeral=True)
    await channel.purge(limit=limit)

@purge.error
async def purge_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permissions do to this", ephemeral=True)


bot.run(TOKEN)