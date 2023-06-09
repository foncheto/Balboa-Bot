import discord
from discord.ext import commands, tasks
import datetime
import pymongo
import os

import certifi
ca = certifi.where()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import json

with open("credentials.json", "r") as f:
    credentials = json.load(f)
    TOKEN = credentials["mongo_uri"]


class birthday_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_client = None
        self.db = None
        self.collection = None
        self.connect_to_mongodb()  # Establish the MongoDB connection
        self.check_birthdays.start()  # Start the background task

    @commands.command(name="set_birthday", aliases=["bday", "cumple"], help="Set your birthday.")
    async def set_birthday(self, ctx, date):
        """Set your birthday."""
        try:
            # Parse the provided date string into a datetime object
            birthday = datetime.datetime.strptime(date, "%Y-%m-%d").date()

            # Save the birthday date for the user
            self.save_birthday(ctx.author.id, birthday)

            await ctx.send("Cumpleaños agregado exitosamente!")
        except ValueError:
            await ctx.send("Formato de fecha incorrecto. Por favor usa YYYY-MM-DD.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("BirthdayCog is ready.")
        self.connect_to_mongodb()
        self.check_birthdays.start()

    def connect_to_mongodb(self):
        # Set up MongoDB connection

        mongo_uri = TOKEN  # Replace with your MongoDB URI
        self.mongo_client = pymongo.MongoClient(mongo_uri, tlsCAFile=ca)
        self.db = self.mongo_client["BalboaBot"]
        self.collection = self.db["Birthdays"]

    def save_birthday(self, user_id, birthday):
        # Check if the user already exists in the collection
        user_data = self.collection.find_one({"user_id": user_id})

        if user_data:
            # Update the existing user's birthday
            self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"birthday": birthday.strftime("%Y-%m-%d")}},
            )
        else:
            # Add a new user and their birthday
            user_data = {"user_id": user_id, "birthday": birthday.strftime("%Y-%m-%d")}
            self.collection.insert_one(user_data)

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        # Get the current date without the year
        current_date = datetime.datetime.now().date().replace(year=1900)

        channel = self.bot.get_channel(852779059234340894)

        # Find all users with a birthday today

        birthday_users = list(
            self.collection.find(
                {
                    "birthday": {
                        "$regex": f"{current_date.month:02d}-{current_date.day:02d}"
                    }
                }
            )
        )

        birthday_count = len(birthday_users)  # Get the count of documents

        if birthday_count == 0:
            await channel.send("Nadie está de cumpleaños hoy")
        else:
            message = ""
            for user_data in birthday_users:
                user = self.bot.get_user(user_data["user_id"])
                if user:
                    message += f"¡Feliz Cumpleaños {user.mention}!\n"
            await channel.send(message)

    @commands.command(name="check", help="Check for birthdays today.")
    async def check(self, ctx):
        # Get the current date without the year
        current_date = datetime.datetime.now().date().replace(year=1900)

        # Find all users with a birthday today
        try:
            birthday_users = list(
                self.collection.find(
                    {
                        "birthday": {
                            "$regex": f"{current_date.month:02d}-{current_date.day:02d}"
                        }
                    }
                )
            )
        except ServerApi.ServerSelectionTimeoutError:
            await ctx.send("Error connecting to MongoDB.")
            return

        birthday_count = len(birthday_users)  # Get the count of documents

        if birthday_count == 0:
            await ctx.send("No hay cumpleaños hoy :(")
        else:
            message = "Cumpleaños Hoy:\n"
            for user_data in birthday_users:
                user = self.bot.get_user(user_data["user_id"])
                if user:
                    message += f"- {user.mention}\n"

            await ctx.send(message)

    @commands.command(name="display", aliases=['mostrar'], help="Display all registered birthdays.")
    async def display_birthdays(self, ctx):
        # Get all registered birthdays
        birthday_users = list(self.collection.find())

        if len(birthday_users) == 0:
            await ctx.send("No existen cumpleaños registrados.")
        else:
            message = "Cumpleaños Registrados:\n"
            for user_data in birthday_users:
                user_id = user_data.get("user_id")
                if user_id:
                    user = self.bot.get_user(user_id)
                    if user:
                        birthday = datetime.datetime.strptime(
                            user_data["birthday"], "%Y-%m-%d"
                        ).date()
                        message += f"- {user.name} ~ {birthday.strftime('%B %d')}\n"

            await ctx.send(message)
