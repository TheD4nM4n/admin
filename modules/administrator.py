from discord.ext import commands
from io import StringIO
from discord import File
from core import admin
from json import dumps
from asyncio import TimeoutError


class AdministratorModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("'Administrator' module loaded.")

    @commands.group(name="config",
                    invoke_without_command=True)
    @commands.is_owner()
    async def config(self, ctx):
        pass

    @config.command(name="dump")
    @commands.is_owner()
    async def dump_config(self, ctx):
        def check(message):
            return message.author == ctx.author

        initial_message = await ctx.send(
            "This will send a copy of the current configuration, which can contain sensitive information and/or "
            "language. Do you wish to proceed? y/n")
        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=10.0)

        except TimeoutError:
            await initial_message.delete()
            return await ctx.send("Cancelling config dump.")

        if confirmation.content.lower() == "y":

            config_file = StringIO(dumps(admin.config, indent=4))
            file = File(config_file, filename="admin_config.txt")
            await ctx.send(file=file)

            await confirmation.delete()
            await initial_message.delete()
            return

    @config.command(name="save")
    @commands.is_owner()
    async def force_save_config(self, ctx):

        admin.save_configuration()
        await ctx.message.add_reaction("✅")
        return

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def log(self, ctx):
        pass

    @log.command(name="dump")
    @commands.is_owner()
    async def dump_log(self, ctx):

        def check(message):
            return message.author == ctx.author

        initial_message = await ctx.send(
            "This will send a copy of the log, which can contain sensitive information. Do you wish to proceed? y/n")
        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=10.0)

        except TimeoutError:
            await initial_message.delete()
            return await ctx.send("Cancelling log dump.")

        if confirmation.content.lower() == "y":

            with open("./discord.log", "rb") as log:
                file = File(log)

            await ctx.send(file=file)

            await confirmation.delete()
            await initial_message.delete()
            return


def setup(bot):
    bot.add_cog(AdministratorModule(bot))
