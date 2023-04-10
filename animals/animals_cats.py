import discord
import aiohttp

class cats_info(discord.app_commands.Group):
   @discord.app_commands.command(name="random_fact", description="Say a random fact about cats")
   async def cats_fact(self, interation: discord.Interaction):
      async with aiohttp.ClientSession() as session:
         async with (session.get("https://catfact.ninja/fact")) as response:
            response = await response.json()
            await interation.response.send_message(response["fact"])
   
   @discord.app_commands.command(name="random_image", description="Display a random cat image")
   async def cats_image(self, interation: discord.Interaction):
      async with aiohttp.ClientSession() as session:
         async with (session.get("https://api.thecatapi.com/v1/images/search")) as response:
            response = await response.json()
            await interation.response.send_message(response[0]["url"])

async def setup(bot):
   bot.tree.add_command(cats_info(name="cats", description="Facts and images about cats!!")) 