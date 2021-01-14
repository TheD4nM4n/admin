import discord
from discord.ext import commands
import json


def load_configuration():
    # Returns the configuration stored on disk.
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)


def save_configuration(config):
    with open("./data/serverconfig.json", "w") as stored_config:
        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


class DevelopmentModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # Loads mute configuration
        config = load_configuration()
        guild_config = config[f"{message.guild.id}"]["mute"]

        # Checks if member is muted and deletes message if so
        if str(message.author.id) in guild_config["muted-members"]:
            return await message.delete()

    @commands.command(description="Immediately deletes further messages from the user specified until disabled.")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, intent=None, member: discord.Member = None):
        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["mute"]

        if intent:
            if intent.lower() == "add":
                guild_config["muted-members"].append(f"{member.id}")
                save_configuration(config)
                return await ctx.message.add_reaction("✅")
            elif intent.lower() == "remove":
                if str(member.id) in guild_config["muted-members"]:
                    guild_config["muted-members"].remove(str(member.id))
                    save_configuration(config)
                    return await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
