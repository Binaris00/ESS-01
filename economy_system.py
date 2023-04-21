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
         embed.add_field(name="/rob (user)", value="Rob 30% a 60% from any user wallet, may be you can lose money, cooldown: 1 hour")
         embed.add_field(name="/deposit", value="Deposit money from your wallet for your bank")
         embed.add_field(name="/withdraw", value="Withdraw your money from your bank")
         embed.add_field(name="money", value="See your wallet and bank money")
         embed.add_field(name="Your wallet:", value=self.wallet)
         await interaction.response.send_message(embed=embed)
      else:
         await interaction.response.send_message("You already started in economy", ephemeral=True)
   
   @app_commands.command(name="money", description="See your wallet and bank money")
   async def economy_money(self, interaction: discord.Interaction):
      if self.started:
         embed = discord.Embed(title="Your money", color=0x12d339)
         embed.add_field(name="Wallet", value=self.wallet)
         embed.add_field(name="Bank", value=self.bank)
         
         
   # Thank you ChatGPT for the messages ;-;
   @app_commands.command(name="work", description="You want to get money with the legal way")
   async def economy_work(self, interaction: discord.Interaction):
      if self.started:
         money_earned = random.randint(100, 300)
         with open("work_messages", "r", encoding="utf8") as file:
            file = file.read()
            file = file.splitlines()
            message = random.choice(file)
            self.wallet += money_earned
            embed = discord.Embed(title="Work", color=0x12d339, description=f"{message}. You earn: {money_earned}")
            await interaction.response.send_message(embed=embed)
      else:
         await interaction.response.send_message("You need to use '/economy_start' first to work", ephemeral=True)

   @app_commands.command(name="crime", description="You choice the ilegal way to earn money, maybe you can lose money")
   async def economy_crime(self, interaction: discord.Interaction):
      if self.started:
         if random.random <= 0.6:
            money_earned = random.randint(500, 700)
            self.wallet += money_earned
            with open("crime good messages.txt", "r", encoding="utf8") as file:
               file = file.read()
               file = file.splitlines()
               message = random.choice(file)
               embed = discord.Embed(title="Crime", color=0x12d339, description=f"{message}, You earn: {money_earned}")
               await interaction.response.send_message(embed=embed)
         
         else:
            money_missed = random.randint(300, 500)
            self.wallet -= money_missed
            with open("crime bad messages.txt", "r", encoding="utf8") as file:
               file = file.read()
               file = file.splitlines()
               message = random.choice(file)
               embed = discord.Embed(title="Crime", color=0xd31226, description=f"{message}, You lose: {money_missed}")
               await interaction.response.send_message(embed=embed)
      else:
         await interaction.response.send_message("You need to use '/economy_start' first to do a crime", ephemeral=True)
         
   @app_commands.command(name="deposit", description="Deposit money from your wallet for your bank")
   async def ecoomy_deposit(self, interaction: discord.Interaction, money: int):
      if self.started:
         if self.wallet >= money:
            self.wallet -= money
            self.bank += money
            await interaction.response.send_message(f"You deposit {money} in your bank, now you have {self.bank} in your bank")
         else:
            await interaction.response.send_message("You don't have that money!!", ephemeral=True)
      else:
         await interaction.response.send_message("You need first use '/start'")
   
   @app_commands.command(name="withdraw", description="Withdraw your money from your bank")
   async def economy_withdraw(self, interaction: discord.Interaction, money: int):
      if self.started:
         if self.bank >= money:
            self.bank -= money
            self.wallet += money
            await interaction.response.send_message(f"You withdraw {money} in your wallet, now you have {self.wallet} in your wallet")
         else:
            await interaction.response.send_message("You don't have that money!!", ephemeral=True)
      else:
         await interaction.response.send_message("You need first use '/start'")
   
   @app_commands.command(name="coin_game", description="All or nothing, risk you wallet and win x2 or lose all your money...")
   async def economy_coin(self, interaction: discord.Interaction):
      if self.started:
         if self.wallet != 0:
            if random.random <= 0.5:
               self.wallet = self.wallet*2
               embed = discord.Embed(title="Coin", description=f"You win!!! Now you have {self.wallet}", color=0x12d339)
               await interaction.response.send_message(embed=embed)
               
            else:
               self.wallet = 0
               embed = discord.Embed(title="Coin", description="You lose :c Now you have 0 coins", color=0xd31226)
               await interaction.response.send_message(embed=embed)
               
         else:
            await interaction.response.send_message("You don't have money in your wallet, please use '/withdraw (money)'")
         
      else:
         await interaction.response.send_message("You don't have money to use '/coin_game', use '/economy_start'", ephemeral=True)
   