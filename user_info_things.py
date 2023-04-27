import discord

class user_info(discord.app_commands.Group):

    @discord.app_commands.command(name="name", description="display the user name")
    async def user_name(self, interaction: discord.Interaction, user: discord.Member= None):
        if user == None:
            data = interaction.user.name
        else:
            data = user.name
        await interaction.response.send_message(data)

    @discord.app_commands.command(name="avatar", description="display the user avatar")
    async def user_avatar(self, interaction: discord.Interaction, user: discord.Member= None):
        if user == None:
            data = interaction.user
        else:
            data = user
        embed = discord.Embed(title=f"{data.name} Avatar")
        embed.set_image(url=data.avatar)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="id", description="display the user id")
    async def user_id(self, interaction: discord.Interaction, user: discord.Member= None):
        if user == None:
            data = interaction.user.id
        else:
            data = user.id
        await interaction.response.send_message(data)
    @discord.app_commands.command(name="user_info", description="Display all the user info in a embed")
    async def user_info_all(self, interaction: discord.Interaction, user: discord.Member=None):
        if user == None:
            data = interaction.user
        else:
            data = user
        embed = discord.Embed(title=f"{data.name} Info")
        embed.set_thumbnail(url=data.avatar)
        embed.add_field(name="Name:", value=data.name)
        embed.add_field(name="Nick", value=data.nick)
        embed.add_field(name="id", value=data.id)
        embed.add_field(name="Joined at", value=discord.utils.format_dt(data.joined_at))
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
   bot.tree.add_command(user_info(name="user", description="Display all user information"))