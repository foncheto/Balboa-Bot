import discord
from discord.ext import commands
import asyncio
import aiohttp
import json

with open("credentials.json") as file:
    credentials = json.load(file)
    TOKEN = credentials["weather_key"]

class weather_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.city = None

    @commands.command(name="weather", help="Get the weather of a city")
    async def weather(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please enter a city")
            return

        self.city = args[0]

        await ctx.send(f"Getting weather for {self.city}")

        url = "http://api.weatherapi.com/v1/current.json"
        params = {"key": TOKEN, "q": self.city}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()

                location = data["location"]["name"]
                temp_c = data["current"]["temp_c"]
                condition = data["current"]["condition"]["text"]
                image_url = "http:" + data["current"]["condition"]["icon"]

                embed = discord.Embed(
                    title=f"Clima en {location}",
                    color=discord.Color.blue(),
                )
                embed.set_thumbnail(url=image_url)
                embed.add_field(name="temp_c", value=f"{temp_c}°C")
                embed.add_field(name="Condición", value=f"{condition}")

                await ctx.send(embed=embed)

        # get weather
        # await ctx.send(f'Weather for {self.city} is {weather}')
