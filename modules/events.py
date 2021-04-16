from discord import Role
from random import choice
from discord.ext import commands


class EventsModule(commands.Cog):

    def __init__(self, bot):

        # Discord.py things
        self.bot = bot
        print("'Events' module loaded.")

    @commands.command(description="A powerful set of tools for running giveaways.")
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx: commands.Context, intent=None, role: Role = None) -> None:

        if intent:

            if intent.lower() == "draw":

                if role:
                    giveaway_winner = choice(role.members)
                    await ctx.send(f"Your winner is {giveaway_winner.mention}!")
                    return

                else:
                    giveaway_winner = choice(ctx.guild.members)
                    await ctx.send(f"Your winner is {giveaway_winner.mention}!")
                    return


def setup(bot):
    bot.add_cog(EventsModule(bot))
