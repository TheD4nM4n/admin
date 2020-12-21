import discord
import json
from discord.ext import commands


class WelcomeMessagesModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("./data/welcomemessages.json") as greetings:
            self.messages = json.load(greetings)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.command()
    async def welcome(self, ctx, *, args):
        """
        TODO: -welcome set #channel: Sets welcome channel for that server
        TODO: -welcome enable/disable: Enables/disables welcome messages for that server
        """

        pass


def setup(bot):
    bot.add_cog(WelcomeMessagesModule(bot))

