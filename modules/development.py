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

    @commands.Cog.listener('on_ready')
    async def loaded_message(self):
        print("'Development' module loaded.")


def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
