from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import discord

class Select_Menu(View):
   def __init__(self, *, timeout: float | None = 180):
      super().__init__(timeout=timeout)
      self.new = "I don't have more ideas to create a good new"
      
      
   @discord.ui.select(
      placeholder="Example Select Menu",
      options=[
         discord.SelectOption(label="Rules", value="1", description="See the rules for this server"),
         discord.SelectOption(label="Your info", value="2", description="see your user info"),
         discord.SelectOption(label="Normal Message", value="3", description="Normal string message"),
         discord.SelectOption(label="Embed Messages", value="4", description="Normal embed message"),
         discord.SelectOption(label="Server news", value="5", description="If the server have any new change you can see here"),
      ]
   )
   async def select_callback(self, interaction, select):
      select.disabled=True
      if select.values[0] == "1":
         embed = discord.Embed(title="Rules (Joke)", description="1-`📗` Don't be racist \n2-`📘`Don't send any message in discord\n3-`📙`Don't talk with any staff", color=discord.Color.dark_blue())
         await interaction.response.send_message(embed=embed, ephemeral=True)
      elif select.values[0] == "2":
         data = interaction.user
         embed = discord.Embed(title=f"{data.name} Info")
         embed.set_thumbnail(url=data.avatar)
         embed.add_field(name="Name:", value=data.name)
         embed.add_field(name="Nick", value=data.nick)
         embed.add_field(name="id", value=data.id)
         embed.add_field(name="Joined at", value=discord.utils.format_dt(data.joined_at))
         
         await interaction.response.send_message(embed=embed, ephemeral=True)
      elif select.values[0] == "3":
         await interaction.response.send_message("omg this is a message :O", ephemeral=True)
      elif select.values[0] == "4":
         embed = discord.Embed(title="Normal Embed", description="Omg this is just a normal embed aaaaa", color=discord.Color.dark_blue())
         await interaction.response.send_message(embed=embed, ephemeral=True)
      elif select.values[0] == "5":
         await interaction.response.send_message(self.new, ephemeral=True)

class Select_menu_cog(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
   
   @app_commands.command(name="select_menu_example", description="Example")
   async def select_menu(self, interaction: discord.Interaction):
      view = Select_Menu()
      await interaction.response.send_message("You can use a normal message and embed message :D", view=view)

      
async def setup(bot):
      await bot.add_cog(Select_menu_cog(bot))