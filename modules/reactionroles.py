import json
import discord

from discord.ext import commands


class ReactionRolesModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("'Reaction Roles' module loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass


def setup(bot):
    bot.add_cog(ReactionRolesModule(bot))
