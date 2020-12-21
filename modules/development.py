import discord
from discord.ext import commands
import json


class DevelopmentModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("./data/rr.json", "r") as rr:
            self.links = json.load(rr)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

            
def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
