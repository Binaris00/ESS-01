from discord.ext import commands
from discord import app_commands
import random
import discord

class Economy(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.wallet = 0
      self.bank = 0
      self.started = False
      
   @app_commands.command(name="economy_start", description="Start with the economy system!!")
   async def economy_start(self, interaction: discord.Interaction):
      if self.started == False:
         self.wallet = 1000
         embed = discord.Embed(title=f"{interaction.user.name} Start in the economy!!!", 
                               description="You start with 1000 coins in your wallet! Now simple commands you can use to generate more monet",
                               color=0x5773ff)
         embed.add_field(name="/work", value="Generate legal money with cooldown: 5 minutes")
         embed.add_field(name="/crime", value="Participe or make a crime to generate money, may be you can lose money, cooldown: 10 minutes")
         embed.add_field(name="/rob (user)", value="Rob a 30% a 60% from any user wallet, may be you can lose money, cooldown: 1 hour")
         embed.add_field(name="/deposit", value="Deposit money from your wallet for your bank")
         embed.add_field(name="withdraw", value="Withdraw your money from your bank")
         embed.add_field(name="Your wallet:", value=self.wallet)
         await interaction.response.send_message(embed=embed)
      else:
         await interaction.response.send_message("You already started in economy", ephemeral=True)
   
   @app_commands.command(name="work", description="You want to get money with the legal way")
   async def economy_work(self, interaction: discord.Interaction):
      if self.started:
         money_earned = random.randint(100, 300)
         with open("work_messages", "r", encoding="utf8") as file:
            file = file.read()
            file = file.splitlines()
            message = random.choice(file)
            embed = discord.Embed(title="Work", color=0x5773ff, description=f"{message}. You earn: {money_earned}")
      else:
         await interaction.response.send_message("You need to use '/start' to start to work", ephemeral=True)


   