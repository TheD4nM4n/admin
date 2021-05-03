from discord import Role
from random import choice
from discord.ext import commands


class EventsModule(commands.Cog):

    def __init__(self, bot):

        # Discord.py things
        self.bot = bot
        print("'Events' module loaded.")

    @commands.group(description="A powerful set of tools for running giveaways.",
                    invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx: commands.Context) -> None:
        pass

    @giveaway.command(name="draw",
                      description="Draws a random winner from everyone in the server or role (if specified).")
    @commands.has_permissions(manage_guild=True)
    async def giveaway_draw(self, ctx, role: Role = None):
        if role:
            await ctx.send(f"Your winner is {choice(role.members).mention}!")

        else:
            await ctx.send(f"Your winner is{choice(ctx.guild.members).mention}!")


def setup(bot):
    bot.add_cog(EventsModule(bot))
