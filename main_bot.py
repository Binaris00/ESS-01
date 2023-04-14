#Essentials modules
from discord.ext import commands
import discord

#Optional modules and bot token and random descriptions when the bot is turn on
from personal_things import TOKEN, random_descriptions
from random import choice

#For api request (Optional)
import aiohttp



intents = discord.Intents.all()
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
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(choice(random_descriptions)))
        
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

@bot.tree.command(name="ban_list", description="See all users banned from your guild")
async def guild_ban_list(interaction: discord.Interaction):
    embed = discord.Embed(title="Banned Members", description="Banned Members from this guild")
    async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.ban):
        embed.add_field(name=f"{entry.user} Banned", value=f"{entry.target}")
    await interaction.response.send_message(embed=embed)


#Logs
@bot.tree.command(name="log_messages", description="Send messages logs to a specific channel")
@discord.app_commands.checks.has_permissions(view_audit_log=True)
async def messages_log(interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
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


@bot.tree.command(name="log_reactions", description="Send reaction logs to a specific channel")
@discord.app_commands.checks.has_permissions(view_audit_log=True)
async def reaction_log(interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
    if confirmation:
        await interaction.response.send_message(f"Now I send the reaction logs in {channel.name}")
        
        @bot.event
        async def on_reaction_add(reaction, user):
            embed = discord.Embed(title="Reaction added log", description=f"{reaction} from {user.name}", color=0x106eea)
            embed.add_field(name=f"Channel sent", value=reaction.message.channel)
            embed.add_field(name="Message", value=reaction.message.content)
            await channel.send(embed=embed)
        
        @bot.event
        async def on_reaction_remove(reaction, user):
            embed = discord.Embed(title="Reaction deleted log", description=f"{reaction} from {user.name}", color=0x106eea)
            embed.add_field(name=f"Channel sent", value=reaction.message.channel)
            embed.add_field(name="Message", value=reaction.message.content)
            await channel.send(embed=embed)

@bot.tree.command(name="log_roles", description="Send role logs to a specific channel")
@discord.app_commands.checks.has_permissions(view_audit_log=True)
async def role_log(interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
    if confirmation:
        await interaction.response.send_message(f"Now I send the roles log in {channel.name}")
        
        @bot.event
        async def on_guild_role_create(role):
            embed = discord.Embed(title="Role Created Log", description=f"Created at {discord.utils.format_dt(role.created_at)}", color=0x0df23b)
            embed.add_field(name="Role Name:", value=role.name)
            embed.add_field(name="Role Color:", value=role.color)
            embed.add_field(name="Role ID:", value=role.id)
            embed.add_field(name="Role Permissions:", value=role.permissions)
            await channel.send(embed=embed)
        
        @bot.event
        async def on_guild_role_delete(role):
            embed = discord.Embed(title="Role Deleted Log", description=f"Name: {role.name}", color=0x0df23b)
            await channel.send(embed=embed)
        
        @bot.event
        async def on_guild_role_update(role_before, role_after):
            embed = discord.Embed(title="Role Deleted Log", color=0x0df23b)
            embed.add_field(name="Role Before Name:", value=role_before.name)
            embed.add_field(name="Role After Name:", value=role_after.name)
            
            embed.add_field(name="Role Before Color:", value=role_before.color)
            embed.add_field(name="Role After Color:", value=role_after.color)
            
            embed.add_field(name="Role Before ID:", value=role_before.id)
            embed.add_field(name="Role After ID:", value=role_after.id)
            
            embed.add_field(name="Role Before Permissions:", value=role_before.permissions)
            embed.add_field(name="Role After Permissions:", value=role_after.permissions)
            await channel.send(embed=embed)
    else:
        await interaction.response.send_message(f"Now not appear roles logs in {channel.name}")

@bot.tree.command(name="thread_logs", description=f"Send thread logs to a specific channel")
@discord.app_commands.checks.has_permissions(view_audit_log=True)
async def thread_logs(interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
    if confirmation:
        await interaction.response.send_message(f"Now I send the thread logs in {channel.name}")
    
    @bot.event
    async def on_thread_create(thread):
        embed = discord.Embed(title="Thread Created Log", color=0xe6e6e6)
        embed.add_field(name="Thread Name:", value=thread.name)
        embed.add_field(name="Thread Owner:", value=thread.owner)
        embed.add_field(name="Created At:", value=thread.created_at)
        embed.add_field(name="Categorys:", value=thread.category)
    
    @bot.event
    async def on_thread_delete(thread):
        embed = discord.Embed(title="Thread Deleted Log", color=0xe6e6e6)
        embed.add_field(name="Thread Name:", value=thread.name)
    
    
bot.run(TOKEN)