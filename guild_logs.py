from discord.ext import commands
from discord import app_commands
import discord


class Log_info(commands.Cog):
      def __init__(self, bot, message_channel=None, reaction_channel=None, role_channel=None, thread_channel=None):
            self.bot = bot
            self.message_channel = message_channel
            self.reaction_channel = reaction_channel
            self.role_channel = role_channel
            self.thread_channel = thread_channel
      
      
      #Message Logs
      @commands.Cog.listener()
      async def on_message_edit(self, before, after, channel=None):
            if self.message_channel != None:
                  channel = self.message_channel
                  embed=discord.Embed(title="Edited Message Log", description=f"From {before.author} in {before.channel.name}", color=0xad0000)
                  embed.set_thumbnail(url=before.author.avatar)
                  embed.add_field(name="Before", value=before.content, inline=True)
                  embed.add_field(name="After", value=after.content, inline=True)
                  await channel.send(embed=embed)
                  
      @commands.Cog.listener()
      async def on_message_delete(self, message, channel=None):
            if self.role_channel != None:
                  channel = self.message_channel
                  embed=discord.Embed(title="Deleted Message Log", description=f"From {message.author} in {message.channel.name}", color=0xad0000)
                  embed.thumbnail(message.author.avatar)
                  embed.add_field(name="Deleted Message:", value=message.content)
                  await channel.send(embed=embed)


      #Reaction Logs
      @commands.Cog.listener()
      async def on_reaction_add(self, reaction, user, channel=None):
            if self.reaction_channel != None:
                  channel = self.reaction_channel
                  embed = discord.Embed(title="Reaction added log", description=f"{reaction} from {user.name}", color=0x106eea)
                  embed.add_field(name=f"Channel sent:", value=reaction.message.channel)
                  embed.add_field(name="Message reacted:", value=reaction.message.content)
                  await channel.send(embed=embed)

      @commands.Cog.listener()
      async def on_reaction_remove(self, reaction, user, channel=None):
            if self.reaction_channel != None:
                  channel = self.reaction_channel
                  embed = discord.Embed(title="Reaction deleted log", description=f"{reaction} from {user.name}", color=0x106eea)
                  embed.add_field(name=f"Channel sent", value=reaction.message.channel)
                  embed.add_field(name="Message", value=reaction.message.content)
                  await channel.send(embed=embed)
            

      #Role logs
      @commands.Cog.listener()
      async def on_guild_role_create(self, role, channel=None):
            if self.role_channel != None:
                  channel = self.role_channel
                  embed = discord.Embed(title="Role Created Log", description=f"Created at {discord.utils.format_dt(role.created_at)}", color=0x0df23b)
                  embed.add_field(name="Role Name:", value=role.name)
                  embed.add_field(name="Role Color:", value=role.color)
                  embed.add_field(name="Role ID:", value=role.id)
                  embed.add_field(name="Role Permissions:", value=role.permissions)
                  await channel.send(embed=embed)
            
      @commands.Cog.listener()
      async def on_guild_role_delete(self, role, channel=None):
            if self.role_channel != None:
                  channel = self.role_channel
                  embed = discord.Embed(title="Role Deleted Log", description=f"Name: {role.name}", color=0x0df23b)
                  await channel.send(embed=embed)

      @commands.Cog.listener()
      async def on_guild_role_update(self, role_before, role_after, channel=None):
            if self.role_channel != None:
                  channel = self.role_channel
                  embed = discord.Embed(title="Role Updated Log", color=0x0df23b)
                  embed.add_field(name="Role Before Name:", value=role_before.name)
                  embed.add_field(name="Role After Name:", value=role_after.name)
                        
                  embed.add_field(name="Role Before Color:", value=role_before.color, inline=False)
                  embed.add_field(name="Role After Color:", value=role_after.color, inline=True)
                        
                  embed.add_field(name="Role Before ID:", value=role_before.id, inline=False)
                  embed.add_field(name="Role After ID:", value=role_after.id, inline=True)
                        
                  embed.add_field(name="Role Before Permissions:", value=role_before.permissions, inline=False)
                  embed.add_field(name="Role After Permissions:", value=role_after.permissions, inline=True)
                  
                  embed.add_field(name="Role Before Position:", value=role_before.position, inline=False)
                  embed.add_field(name="Role After Position:", value=role_after.position, inline=True)
                  await channel.send(embed=embed)


      #Thread Logs
      @commands.Cog.listener()
      async def on_thread_create(self, thread, channel=None):
            if self.thread_channel != None:
                  channel = self.thread_channel
                  embed = discord.Embed(title="Thread Created Log", color=0xe6e6e6)
                  embed.add_field(name="Thread Name:", value=thread.name)
                  embed.add_field(name="Thread Owner:", value=thread.owner)
                  embed.add_field(name="Created At:", value=discord.utils.format_dt(thread.created_at))
                  embed.add_field(name="Categorys:", value=thread.category)
                  await channel.send(embed=embed)

      @commands.Cog.listener()
      async def on_thread_delete(self, thread, channel=None):
            if self.thread_channel != None:
                  channel = self.thread_channel
                  embed = discord.Embed(title="Thread Deleted Log", color=0xe6e6e6)
                  embed.add_field(name="Thread Name:", value=thread.name)
                  await channel.send(embed=embed)



class Log(commands.Cog):
      def __init__(self, bot):
            self.bot = bot
      
      @app_commands.command(name="messages_log", description="Send messages logs to a specific channel")
      @app_commands.checks.has_permissions(view_audit_log=True)
      async def messages_log(self, interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
            messagelog = self.bot.get_cog("Log_info")
            if confirmation: 
                  setattr(messagelog, "message_channel", channel)
                  await interaction.response.send_message(f"Now I send the messages logs in {channel.name}")
            else:
                  setattr(messagelog, "message_channel", None)
                  await interaction.response.send_message(f"Not sending messages logs in {channel.name}")
      
      
      @app_commands.command(name="reaction_log", description="Send reaction logs to a specific channel")
      @app_commands.checks.has_permissions(view_audit_log=True)
      async def reaction_log(self, interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
            reactionlog = self.bot.get_cog("Log_info")
            if confirmation:
                  setattr(reactionlog, "reaction_channel", channel)
                  await interaction.response.send_message(f"Now I send the reaction logs in {channel.name}")
            else:
                  setattr(reactionlog, "reaction_channel", None)
                  await interaction.response.send_message(f"Not sending reaction logs in {channel.name}")
                  
      
      @app_commands.command(name="roles_log", description="Send role logs to a specific channel")
      @app_commands.checks.has_permissions(view_audit_log=True)
      async def role_log(self, interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
            rolelog = self.bot.get_cog("Log_info")
            if confirmation:
                  setattr(rolelog, "role_channel", channel)
                  await interaction.response.send_message(f"Now I send the roles logs in {channel.name}")
            else:
                  setattr(rolelog, "role_channel", None)
                  await interaction.response.send_message(f"Not sending roles logs in {channel.name}")
      @app_commands.command(name="thread_log", description="Send thread logs to a specific channel")
      async def thread_log(self, interaction: discord.Interaction, channel: discord.TextChannel, confirmation: bool):
            threadlog = self.bot.get_cog("Log_info")
            if confirmation:
                  setattr(threadlog, "thread_channel", channel)
                  await interaction.response.send_message(f"Now I send thread logs in {channel.name}")
            else:
                  setattr(threadlog, "thread_channel", None)
                  await interaction.response.send_message(f"Now sending thread logs in {channel.name}")
async def setup(bot):
      await bot.add_cog(Log(bot))
      await bot.add_cog(Log_info(bot))