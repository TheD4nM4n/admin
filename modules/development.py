from discord.ext import commands


class DevelopmentModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("'Development' module loaded.")


def setup(bot):
    bot.add_cog(DevelopmentModule(bot))
