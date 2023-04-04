import discord
import aiohttp

class dogs_info(discord.app_commands.Group):
   @discord.app_commands.command(name="random_fact", description="Say a random fact about dogs")
   async def dogs_fact(self, interation: discord.Interaction):
      async with aiohttp.ClientSession() as session:
         async with (session.get("https://dogapi.dog/api/facts")) as response:
            response = await response.json()
            await interation.response.send_message(response["facts"][0])
   
   @discord.app_commands.command(name="random_image", description="Display a random dog image")
   async def dogs_image(self, interation: discord.Interaction):
      async with aiohttp.ClientSession() as session:
         async with (session.get("https://dog.ceo/api/breeds/image/random")) as response:
            response = await response.json()
            await interation.response.send_message(response["message"])

async def setup(bot):
   bot.tree.add_command(dogs_info(name="dogs", description="Facts and images about dogs!!"))