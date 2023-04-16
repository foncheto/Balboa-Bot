import discord
import os
from discord.ext import commands

from music_cog import music_cog
from help_cog import help_cog

intent = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intent)

bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    print('Logged in as')
    print(bot.user.name)
    print("Dale tu corte chuchetumare!!!")
    print('------')

bot.run('token')



