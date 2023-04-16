import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.message = """
```
!help - Shows this message
!play <song name> - Plays a song
!pause - Pauses the current song
!resume - Resumes the current song
!stop - Stops the current song
!queue - Shows the current song queue
!skip - Skips the current song
!clear - Clears the song queue
```
        """
        self.text_channel_list = []
    commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == 'general':
                    self.text_channel_list = channel
                    await self.text_channel_list.send(self.message)

    @commands.command(name='help', help='Shows this message')
    async def help(self, ctx):
        await ctx.send(self.message)
    