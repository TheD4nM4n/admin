import json
import discord
from discord.ext import commands
from random import choice


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

    def save_configuration(self):
        with open("./data/serverconfig.json", "w") as stored_config:
            # This writes the configuration with the changes made to the disk.
            json.dump(self.config, stored_config, indent=4)
            stored_config.truncate()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        # Gets the configuration for the server that the user joined
        guild_config = self.config[f"{member.guild.id}"]["greetings"]

        """
                If welcome messages are enabled for the server, send a message from the list.

                Custom messages can be added to welcomemessages.json.
                    Make sure to include the {member} and {guild} "tokens".
                        The {member} token will be replaced with the mention of the member joining.
                        The {guild} token will be replaced with the name of the guild.
        """

        if guild_config["enabled"]:
            welcome_channel = self.bot.get_channel(guild_config["channel"])
            message = choice(self.messages).replace("{member}", member.mention).replace("{guild}", member.guild.name)
            await welcome_channel.send(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, intent=None, channel: discord.TextChannel = None):

        guild_config = self.config[f"{ctx.guild.id}"]["greetings"]

        if intent:
            if intent.lower() == "enable":
                guild_config["enabled"] = True
                self.save_configuration()
            elif intent.lower() == "disable":
                guild_config["enabled"] = False
                self.save_configuration()
            elif intent.lower() == "set":
                if channel:
                    if channel.guild.id == ctx.guild.id:
                        guild_config["channel"] = channel.id
                        self.save_configuration()


def setup(bot):
    bot.add_cog(WelcomeMessagesModule(bot))
