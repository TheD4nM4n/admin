import discord
from discord.ext import commands
import json
from core import load_configuration, save_configuration


class DevelopmentModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def loaded_message(self):
        print("'Development' module loaded.")


def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
