import discord
class user_info(discord.app_commands.Group):
    @discord.app_commands.command(name="name", description="display the user name")
    async def user_name(self, interation: discord.Interaction, user: discord.Member= None):
        if user is None:
            data = interation.user.name
        else:
            data = user.name
        await interation.response.send_message(data)
    @discord.app_commands.command(name="avatar", description="display the user avatar")
    async def user_avatar(self, interation: discord.Interaction, user: discord.Member= None):
        if user is None:
            data = interation.user.avatar
        else:
            data = user.avatar
        await interation.response.send_message(data)
    @discord.app_commands.command(name="id", description="display the user id")
    async def user_id(self, interation: discord.Interaction, user: discord.Member= None):
        if user is None:
            data = interation.user.id
        else:
            data = user.id
        await interation.response.send_message(data)
async def setup(bot):
   bot.tree.add_command(user_info(name="user", description="Display al user information"))