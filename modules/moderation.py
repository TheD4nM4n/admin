import discord
from discord.ext import commands
import json
from core import load_configuration, save_configuration


class MemberAlreadyAssigned(Exception):
    pass


class ModerationModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def loaded_message(self):
        print("'Moderation' module loaded.")

    @commands.Cog.listener("on_message")
    async def mute_listener(self, message):

        # Loads mute configuration
        config = load_configuration()
        guild_config = config[f"{message.guild.id}"]["mute"]

        # Checks if member is muted and deletes message if so
        if message.author.id in guild_config["muted-members"]:
            return await message.delete()

    @commands.command(description="Deletes the number of messages specified, starting at the most recent (includes "
                                  "the message used to invoke the command).")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context, number: int):
        messages = await ctx.channel.history(limit=number).flatten()

        for message in messages:
            await message.delete()

        await ctx.send(f"Deleted {len(messages)} messages.")

    @commands.group(description="Immediately deletes further messages from the user specified until disabled.",
                    invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx: commands.Context, intent=None, member: discord.Member = None):
        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["mute"]

        if intent:
            if intent.lower() == "add":
                guild_config["muted-members"].append(f"{member.id}")
                save_configuration(config)
                return await ctx.message.add_reaction("✅")

    @mute.command(name="add")
    async def mute_add(self, ctx: commands.Context, member: discord.Member):

        # Loads configuration and also ties an easier-to-use pointer to the mute section
        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["mute"]

        if member.id in guild_config["muted-members"]:
            raise MemberAlreadyAssigned("That member is already a part of the list.")
        # Adds the member to the mute list, and saves the list to disk
        guild_config["muted-members"].append(member.id)
        save_configuration(config)
        return await ctx.message.add_reaction("✅")

    @mute.command(name="remove")
    async def mute_remove(self, ctx: commands.Context, member: discord.Member):

        # Loads configuration and also ties an easier-to-use pointer to the mute section
        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["mute"]

        if str(member.id) in guild_config["muted-members"]:
            guild_config["muted-members"].remove(member.id)
            save_configuration(config)
            return await ctx.message.add_reaction("✅")

    @mute_add.error
    @mute_remove.error
    async def mute_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, MemberAlreadyAssigned):
                await ctx.send("That member is already muted. Did you mean to remove them?")


def setup(bot):
    bot.add_cog(ModerationModule(bot))
