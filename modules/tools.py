import discord
from discord.ext import commands
import asyncio

COLORS = {
    "red": 0xff0000,
    "orange": 0xffa500,
    "yellow": 0xffff00,
    "green": 0x00ff00,
    "blue": 0x0000ff,
    "indigo": 0x4b0082,
    "violet": 0xee82ee
}


class ToolsModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("'Tools' module loaded.")

    @commands.group(description="Makes items.")
    @commands.has_permissions(administrator=True)
    async def make(self, ctx):
        pass

    @make.command(description="Makes an embed. Denote the beginning of the description using a '|' symbol.")
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx: commands.Context, color: str = "red", *, content: str):

        # Check function for seeing if the message sent is valid
        def check(msg: discord.Message) -> bool:
            return msg.author == ctx.message.author and msg.channel == ctx.channel

        # Fetches color from the dictionary, and splits the content into it's title and description
        html_color = COLORS[color]
        split_message = content.split("|")

        # We aren't finished yet!
        finished = False

        embed = discord.Embed(title=split_message[0],
                              description=split_message[1],
                              color=html_color)

        await ctx.send("Construction started! To continue adding fields, follow the initial formatting *name|value* "
                       "in new messages, then send *done* when complete.\n*Note: The construction will time out 60 "
                       "seconds after the last field added.*")

        while not finished:

            message: discord.Message = await self.bot.wait_for('message', check=check, timeout=60)

            if message.content.lower() == "done":
                finished = True

            else:
                split_message = message.content.split('|')
                embed.add_field(name=split_message[0],
                                value=split_message[1])

        await ctx.send(embed=embed)

    @make.group(name="server")
    @commands.has_permissions(administrator=True)
    async def make_server(self, ctx: commands.Context):
        pass

    @embed.error
    async def make_embed_error(self, ctx, error):
        error = getattr(error, "original", error)

        print(type(error))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You didn't include your embed content! Try again with your embed's title and description, "
                           "separated by a | symbol.")
        elif isinstance(error, IndexError):
            await ctx.send("You didn't separate your title and description correctly! Use a | symbol to separate the "
                           "title and description. Try again!")
        elif isinstance(error, asyncio.TimeoutError):
            await ctx.send("The construction has timed out, and as such has been cancelled. Try again!")


def setup(bot):
    bot.add_cog(ToolsModule(bot))
