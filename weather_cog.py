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

    @commands.command(name="weather", aliases=["w","clima"], help="Get the weather of a city")
    async def weather(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Porfavor ingresa una ciudad para buscar el clima", delete_after=20)
            return

        self.city = args[0]

        await ctx.send(f"Consiguiendo el clima en {self.city}", delete_after=20)

        url = "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": TOKEN, "q": self.city, "days": 3}  # Specify 2 days of forecast

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()

                location = data["location"]["name"]
                current_temp_c = data["current"]["temp_c"]
                current_condition = data["current"]["condition"]["text"]
                tomorrow_condition = data["forecast"]["forecastday"][1]["day"]["condition"]["text"]
                aftertomorrow_condition = data["forecast"]["forecastday"][2]["day"]["condition"]["text"]
                current_image_url = "http:" + data["current"]["condition"]["icon"]
                tomorrow_image_url = "http:" + data["forecast"]["forecastday"][1]["day"]["condition"]["icon"]
                aftertomorrow_image_url = "http:" + data["forecast"]["forecastday"][2]["day"]["condition"]["icon"]
                today_max_temp_c = data["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
                today_min_temp_c = data["forecast"]["forecastday"][0]["day"]["mintemp_c"]

                # Tomorrow's max temp is at index 1
                tomorrow_max_temp_c = data["forecast"]["forecastday"][1]["day"]["maxtemp_c"]
                tomorrow_min_temp_c = data["forecast"]["forecastday"][1]["day"]["mintemp_c"]
                aftertomorrow_max_temp_c = data["forecast"]["forecastday"][2]["day"]["maxtemp_c"]
                aftertomorrow_min_temp_c = data["forecast"]["forecastday"][2]["day"]["mintemp_c"]

                embed = discord.Embed(
                    title=f"Clima en {location}: {current_condition}",
                    color=discord.Color(0x0D8F9C),
                )
                embed.set_thumbnail(url=current_image_url)
                embed.add_field(name="Temperatura Actual:", value=f"{current_temp_c}°C")
                embed.add_field(name="Máxima:", value=f"{today_max_temp_c}°C")
                embed.add_field(name="Mínima:", value=f"{today_min_temp_c}°C")

                await ctx.send(embed=embed, delete_after=20)

                embed_tomorrow = discord.Embed(
                    title=f"Clima mañana en {location}: {tomorrow_condition}",
                    color=discord.Color(0x0B3B84),
                )
                embed_tomorrow.set_thumbnail(url=tomorrow_image_url)
                embed_tomorrow.add_field(name="Máxima:", value=f"{tomorrow_max_temp_c}°C")
                embed_tomorrow.add_field(name="Mínima:", value=f"{tomorrow_min_temp_c}°C")

                await ctx.send(embed=embed_tomorrow, delete_after=20)

                embed_after_tomorrow = discord.Embed(
                    title=f"Clima pasado mañana en {location}: {aftertomorrow_condition}",
                    color=discord.Color(0x840B82),
                )
                embed_after_tomorrow.set_thumbnail(url=aftertomorrow_image_url)
                embed_after_tomorrow.add_field(name="Maxima:", value=f"{aftertomorrow_max_temp_c}°C")
                embed_after_tomorrow.add_field(name="Mínima:", value=f"{aftertomorrow_min_temp_c}°C")

                await ctx.send(embed=embed_after_tomorrow, delete_after=20)

        # get weather
        # await ctx.send(f'Weather for {self.city} is {weather}')
