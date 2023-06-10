import discord
import os
from discord.ext import commands
import json

# AÑADIR FUNCION QUE AÑADA CUMPLEAÑOS 

# Load the Discord API key from credentials.json
with open("credentials.json") as file:
    credentials = json.load(file)
    TOKEN = credentials["discord_api"]

from music_cog import music_cog
from help_cog import help_cog
from birthday_cog import birthday_cog
from weather_cog import weather_cog

intent = discord.Intents.all()

bot = commands.Bot(command_prefix="/", intents=intent)

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(birthday_cog(bot))
    await bot.add_cog(weather_cog(bot))
    await bot.change_presence(activity=discord.Game(name="Dale tu corte chuchetumare!!!"))
    print("Logged in as")
    print(bot.user.name)
    print("Dale tu corte chuchetumare!!!")
    print("------")


bot.run(TOKEN)
