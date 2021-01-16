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

    @commands.group(description="Makes items.")
    async def make(self, ctx):
        pass

    @make.command(description="Makes an embed.")
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx: commands.Context, *, content: str):

        if content:

            split_message = content.split("|")

            embed = discord.Embed(title=split_message[0],
                                  description=split_message[1],
                                  color=0xff0000)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
