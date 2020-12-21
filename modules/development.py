import discord
from discord.ext import commands
import json


class DevelopmentModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("./data/rr.json", "r") as rr:
            self.links = json.load(rr)

            
def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
