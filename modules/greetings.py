import json
from discord import TextChannel, File, Embed
from discord.ext import commands
from random import choice
from core import admin


class GreetingsModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("'Greetings' module loaded.")

        # This loads the preset messages in greetings.json.
        with open("./data/greetings.json", "r") as messages:
            self.messages = json.load(messages)['messages']

    @commands.Cog.listener('on_member_join')
    async def send_greeting(self, member):

        # Gets the configuration for the server that the user joined
        guild_config = admin.config[f"{member.guild.id}"]["greetings"]

        """ 
                If greetings are enabled for the server, send a message from the list.

                Custom messages can be added to greetings.json.
                    Make sure to include the {member} and {guild} "tokens".
                        The {member} token will be replaced with the mention of the member joining.
                        The {guild} token will be replaced with the name of the guild.
        """

        if guild_config["enabled"]:
            greeting_channel = self.bot.get_channel(guild_config["channel"])
            message = choice(self.messages)

            if "{member}" in message:
                message = message.replace("{member}", member.mention)
            if "{guild}" in message:
                message = message.replace("{guild}", member.guild.name)

            await greeting_channel.send(message)

    @commands.group(description="Allows configuration of the greetings of new users in your server.",
                    invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def greetings(self, ctx):

        # Constructing the "welcome usage" embedded message
        file = File(fp="./assets/vgctired.png", filename="vgctired.png")
        embed = Embed(title="greetings",
                      description="Helps you take control of your greeting messages.",
                      color=0xff0000)
        embed.set_thumbnail(url="attachment://vgctired.png")
        embed.add_field(name="Intents",
                        value="To use these, execute 'greetings *intent*'. Some intents may require arguments, "
                              "and ones that do will have them shown below.",
                        inline=False)
        embed.add_field(name="set *#channel*",
                        value="Sets the channel for greeting messages.\n"
                              "Example usage: *greetings set #welcome*",
                        inline=False)
        embed.add_field(name="enable/disable",
                        value="Enables/disables greeting messages for this server.\n"
                              "Example usage: *greetings enable*",
                        inline=False)

        # Sending the embed
        return await ctx.send(file=file, embed=embed)

    @greetings.command(name="set")
    @commands.has_permissions(manage_guild=True)
    async def greetings_set(self, ctx, channel: TextChannel):

        # Sets the welcome channel for the server to the channel provided
        guild_config = admin.config[f"{ctx.guild.id}"]["greetings"]

        if channel.guild.id == ctx.guild.id:
            guild_config["channel"] = channel.id
            return await ctx.message.add_reaction("✅")

    @greetings.command(name="enable")
    @commands.has_permissions(manage_guild=True)
    async def greetings_enable(self, ctx):

        # This enables welcome messages for the server
        guild_config = admin.config[f"{ctx.guild.id}"]["greetings"]

        guild_config["enabled"] = True
        return await ctx.message.add_reaction("✅")

    @greetings.command(name="disable")
    @commands.has_permissions(manage_guild=True)
    async def greetings_disable(self, ctx):

        # This enables welcome messages for the server
        guild_config = admin.config[f"{ctx.guild.id}"]["greetings"]

        guild_config["enabled"] = True
        return await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(GreetingsModule(bot))
