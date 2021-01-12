from datetime import datetime
from discord.ext import commands


class StatisticsModule(commands.Cog):

    def __init__(self, bot):

        # Discord.py things
        self.bot = bot

    @commands.command(name="count")
    async def member_count(self, ctx) -> None:

        number_of_days = (datetime.today().date() - ctx.guild.created_at.date()).days
        print(number_of_days)
        await ctx.send(f"There are {len(ctx.guild.members)} members in {ctx.guild.name}.\n"
                       f"Average members per day: {len(ctx.guild.members) / number_of_days}")
        return


def setup(bot):
    bot.add_cog(StatisticsModule(bot))
