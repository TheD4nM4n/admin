import json
import discord
from discord.ext import commands
from random import choice


def load_configuration():
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)


def save_configuration(config):
    with open("./data/serverconfig.json", "w") as stored_config:

        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


class GreetingsModule(commands.Cog):

    def __init__(self, bot):
        # Normal discord.py things
        self.bot = bot

        # This loads the preset messages in welcomeconfig.json.
        with open("./data/greetings.json", "r") as messages:
            self.messages = json.load(messages)['messages']

    @commands.Cog.listener('on_ready')
    async def loaded_message(self):
        print("'Greetings' module loaded.")

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):

        # Gets the configuration for the server that the user joined
        guild_config = load_configuration()[f"{member.guild.id}"]["greetings"]

        """
                If greetings are enabled for the server, send a message from the list.

                Custom messages can be added to greetings.json.
                    Make sure to include the {member} and {guild} "tokens".
                        The {member} token will be replaced with the mention of the member joining.
                        The {guild} token will be replaced with the name of the guild.
        """

        if guild_config["enabled"]:
            greeting_channel = self.bot.get_channel(guild_config["channel"])
            message = choice(self.messages).replace("{member}", member.mention).replace("{guild}", member.guild.name)
            await greeting_channel.send(message)

    @commands.command(description="Allows configuration of the greetings of new users in your server.")
    @commands.has_permissions(administrator=True)
    async def greetings(self, ctx: commands.Context, intent=None, channel: discord.TextChannel = None):

        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["greetings"]

        if intent:

            if intent.lower() == "enable":

                # This enables welcome messages for the server
                guild_config["enabled"] = True
                save_configuration(config)
                return await ctx.message.add_reaction("✅")

            elif intent.lower() == "disable":

                # I give you three guesses as to what this does
                guild_config["enabled"] = False
                save_configuration(config)
                return await ctx.message.add_reaction("✅")

            elif intent.lower() == "set":

                # Sets the welcome channel for the server to the channel provided
                if channel:
                    if channel.guild.id == ctx.guild.id:
                        guild_config["channel"] = channel.id
                        save_configuration(config)
                        return await ctx.message.add_reaction("✅")

            else:

                # Constructing the error embedded message
                file = discord.File(fp="./assets/vgcsad.png", filename="vgcsad.png")
                embed = discord.Embed(title="Sorry, that isn't a valid use of the **greetings** command.",
                                      description="Try sending *-greetings* to see valid uses!",
                                      color=0xff0000)
                embed.set_thumbnail(url="attachment://vgcsad.png")

                # Sending da embed
                return await ctx.send(file=file, embed=embed)

        else:

            # Constructing the "welcome usage" embedded message
            file = discord.File(fp="./assets/vgctired.png", filename="vgctired.png")
            embed = discord.Embed(title="greetings",
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

            # Sending da embed
            return await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(GreetingsModule(bot))
