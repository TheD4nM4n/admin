import json
from discord.ext import commands


class WelcomeMessagesModule(commands.Cog):

    def __init__(self, bot):
        # Normal discord.py things
        self.bot = bot

        # This fetches serverconfig.json and loads it into a variable.
        with open("./data/serverconfig.json", "r") as config:
            self.config = json.load(config)

        # This loads the preset messages in welcomeconfig.json.
        with open("./data/welcomemessages.json", "r") as messages:
            self.messages = json.load(messages)['messages']

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # This listens for a member to join the server. Once someone does, it runs the code below.
        if self.config[f"{member.guild.id}"]["greetings"]:
            print("test confirmed")

    @commands.command()
    async def welcome(self, ctx, *, args):
        """
        TODO: -welcome set #channel: Sets welcome channel for that server
        TODO: -welcome enable/disable: Enables/disables welcome messages for that server
        """

        pass


def setup(bot):
    bot.add_cog(WelcomeMessagesModule(bot))
