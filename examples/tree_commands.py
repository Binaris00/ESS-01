from discord.ext import commands
from discord import app_commands
import discord

#I use commands like math operations to view how to create tree commands

class Math(app_commands.Group):
   
   
   # A simple command, you need to use self (Because is a class duh), interaction or ctx whatever and any other parameters
   #You can use any other thing to do with commands
   @app_commands.command(name="sum_two", description="Sum 2 numbers")
   async def sum_two(self, interaction: discord.Interaction, one_number: float, two_number: float):
      await interaction.response.send_message(f"Answer: {one_number+two_number}")
   
   
   


async def setup(bot):
   #Now in the bot the command is '/math sum_two 1 2'
   bot.tree.add_command(Math(name="math", description="Basic math operations and others"))