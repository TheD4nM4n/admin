from datetime import datetime

from discord import Embed
from discord.ext import commands


class StatisticsModule(commands.Cog):

    def __init__(self, bot):

        # Discord.py things
        self.bot = bot

    @commands.command(aliases=["stats"])
    async def statistics(self, ctx) -> None:

        number_of_days = (datetime.today().date() - ctx.guild.created_at.date()).days
        print(number_of_days)

        embed = Embed(title="Server Statistics",
                      description=f"Server statistics for {ctx.guild.name}",
                      color=0xff0000)
        embed.set_thumbnail(url=str(ctx.guild.icon_url_as(static_format='png')))
        embed.add_field(name="Members",
                        value=f"Member count: {len(ctx.guild.members)} members\n"
                              f"Members/day: {round(len(ctx.guild.members) / number_of_days, 2)} members/day\n"
                              f"",
                        inline=False)

        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(StatisticsModule(bot))
