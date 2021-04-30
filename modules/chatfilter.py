from re import sub

import discord
from discord import User, File, Embed, Message
from better_profanity import profanity
from discord.ext import commands

from core import admin


def usage_embed() -> tuple:
    file = File(fp="./assets/vgctired.png", filename="vgctired.png")
    embed = Embed(title="filter",
                  description="Provides helpful settings for your chat filter.",
                  color=0xff0000)
    embed.set_thumbnail(url="attachment://vgctired.png")
    embed.add_field(name="Intents",
                    value="To use these, execute 'filter *intent*'. Some intents may require arguments, "
                          "and ones that do will have them shown below.",
                    inline=False)
    embed.add_field(name="set *#channel*",
                    value="Sets the channel for filter logs. Use *set none* to disable logging.\n"
                          "Example usage: *filter set #log*",
                    inline=False)
    embed.add_field(name="enable/disable",
                    value="Enables/disables the chat filter for this server.\n"
                          "Example usage: *filter enable*",
                    inline=False)
    embed.add_field(name="add/remove *word*",
                    value="Adds/removes the word specified to/from a server-specific blacklist.\n"
                          "Example usage: *filter add admin*",
                    inline=False)
    return file, embed


class ChatFilterModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        profanity.load_censor_words_from_file("./data/default_word_list.txt")
        print("'Chat Filter' module loaded.")

    def exempt_check(self, message) -> bool:

        if message.author.id in admin.config[f"{message.guild.id}"]["chat-filter"]["whitelisted-members"]:
            return True
        elif message.channel.id in admin.config[f"{message.guild.id}"]["chat-filter"]["whitelisted-channels"]:
            return True
        elif message.author.id == self.bot.user.id:
            return True
        elif isinstance(message.author, User):
            return True
        else:
            return False

    @commands.Cog.listener("on_message")
    async def chat_filter(self, message: Message) -> None:
        # Loads the chat filter configuration of the server the message was sent
        try:
            guild_config = admin.config[f"{message.guild.id}"]["chat-filter"]
        except KeyError:
            guild_config = admin.config[f"{message.guild.id}"]
            guild_config["chat-filter"] = {
                "enabled": True,
                "log-channel": None,
                "use-default-list": True,
                "custom-words": [],
                "whitelisted-channels": [],
            }
            admin.save_configuration(admin.config)

        if guild_config["enabled"]:

            # If the message isn't sent by the bot, in a whitelisted channel, or sent by a whitelisted user...
            if not self.exempt_check(message):

                if message.author.guild_permissions.administrator and "-filter add" in message.content:
                    pass

                else:

                    text_without_formatting = sub("[^\\w-]+", " ", message.content)

                    # Checks if message contains a custom blacklisted word
                    for word in guild_config["custom-words"]:

                        if word in text_without_formatting.lower():

                            # Delete message
                            await message.delete()

                            # If the server has a log channel set, build an embed and send it.
                            if guild_config["log-channel"]:
                                file = File("./assets/vgcdisgusting.png")
                                embed = Embed(title="I have deleted a message from a channel.",
                                              description=f"Offender: {message.author.name}\n"
                                                          f"Channel: {message.channel}\n",
                                              color=0xff0000)
                                embed.add_field(name="Message content:", value=text_without_formatting)
                                embed.set_thumbnail(url="attachment://vgcdisgusting.png")

                                log_channel = self.bot.get_channel(guild_config["log-channel"])
                                await log_channel.send(file=file, embed=embed)
                                return

                            return

                    # ...check for profanity.
                    if guild_config["use-default-list"]:

                        if profanity.contains_profanity(text_without_formatting):

                            # Delete message
                            await message.delete()

                            # If the server has a log channel set, build an embed and send it.
                            if guild_config["log-channel"]:
                                file = File("./assets/vgcdisgusting.png")
                                embed = Embed(title="I have deleted a message from a channel.",
                                              description=f"Offender: {message.author.name}\n"
                                                          f"Channel: {message.channel}\n",
                                              color=0xff0000)
                                embed.add_field(name="Message content:", value=message.content)
                                embed.add_field(name="Filtered content:",
                                                value=profanity.censor(text_without_formatting, "#"))
                                embed.set_thumbnail(url="attachment://vgcdisgusting.png")
                                log_channel = self.bot.get_channel(guild_config["log-channel"])

                                await log_channel.send(file=file, embed=embed)
                                return

    @commands.group(name="filter",
                    description="Allows the configuration of the chat filter in this server.",
                    invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def filter_command(self, ctx: commands.Context):

        file = File(fp="./assets/vgctired.png", filename="vgctired.png")
        embed = Embed(title="filter",
                      description="Provides helpful settings for your chat filter.",
                      color=0xff0000)

        embed.set_thumbnail(url="attachment://vgctired.png")

        embed.add_field(name="Intents",
                        value="To use these, execute 'filter *intent*'. Some intents may require arguments, "
                              "and ones that do will have them shown below.",
                        inline=False)

        embed.add_field(name="set *#channel*",
                        value="Sets the channel for filter logs. Use *set none* to disable logging.\n"
                              "Example usage: *filter set #log*",
                        inline=False)

        embed.add_field(name="enable/disable",
                        value="Enables/disables the chat filter for this server.\n"
                              "Example usage: *filter enable*",
                        inline=False)

        embed.add_field(name="add/remove *word*",
                        value="Adds/removes the word specified to/from a server-specific blacklist.\n"
                              "Example usage: *filter add admin*",
                        inline=False)

        await ctx.send(file=file, embed=embed)
        return

    @filter_command.command(name="enable")
    @commands.has_permissions(manage_messages=True)
    async def enable_filter(self, ctx: commands.Context):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["enabled"] = True
        await ctx.message.add_reaction("✅")
        return

    @filter_command.command(name="disable")
    @commands.has_permissions(manage_messages=True)
    async def disable_filter(self, ctx: commands.Context):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["enabled"] = False
        await ctx.message.add_reaction("✅")
        return

    @filter_command.command(name="log")
    @commands.has_permissions(manage_messages=True)
    async def filter_log(self, ctx: commands.Context, channel):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]
        channels = ctx.message.channel_mentions

        if channels:
            guild_config["log-channel"] = channels[0].id
            await ctx.message.add_reaction("✅")
            return
        else:
            if channel.lower() == "none":
                guild_config["log-channel"] = None
                await ctx.message.add_reaction("✅")
                return

    @filter_log.error
    async def filter_log_error(self, ctx, error):

        # Gets original error (useful if the error invoked is a CommandInvokeError)
        error = getattr(error, "original", error)

        # If a channel or "none" isn't given
        if isinstance(error, commands.MissingRequiredArgument):
            # Sends an embed telling the user to try again.
            file = File(fp="./assets/vgcsad.png")
            embed = Embed(title="Sorry, something went wrong...",
                          description="There was no channel mentioned in that message. Make sure "
                                      "you use the hashtag (#) to properly mention the channel. "
                                      "Go ahead and try again!",
                          color=0xff0000)
            embed.set_thumbnail(url="attachment://vgcsad.png")
            await ctx.send(file=file, embed=embed)
            return

    @filter_command.command(name="add")
    @commands.has_permissions(manage_messages=True)
    async def add_word(self, ctx: commands.Context, word):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["custom-words"].append(word.lower())
        await ctx.message.add_reaction("✅")
        return

    @add_word.error
    async def add_word_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.MissingRequiredArgument):
            file = File(fp="./assets/vgcsad.png")
            embed = Embed(title="Sorry, something went wrong...",
                          description="It looks like you didn't provide a word. Try again with a "
                                      "word, like *filter add admin*.",
                          color=0xff0000)
            embed.set_thumbnail(url="attachment://vgcsad.png")
            await ctx.send(file=file, embed=embed)
            return

    @filter_command.command(name="remove")
    @commands.has_permissions(manage_messages=True)
    async def remove_word(self, ctx: commands.Context, word):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["custom-words"].remove(word.lower())
        await ctx.message.add_reaction("✅")
        return

    @remove_word.error
    async def remove_word_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.MissingRequiredArgument):
            file = File(fp="./assets/vgcsad.png")
            embed = Embed(title="Sorry, something went wrong...",
                          description="It looks like you didn't provide a word. Try again with a "
                                      "word, like *filter remove admin*.",
                          color=0xff0000)
            embed.set_thumbnail(url="attachment://vgcsad.png")
            await ctx.send(file=file, embed=embed)
            return
        elif isinstance(error, ValueError):
            file = File(fp="./assets/vgcyes.png")
            embed = Embed(title="That word wasn't found...",
                          description="Looks like you didn't need to run that command, "
                                      "because that word isn't in your server's list!",
                          color=0xff0000)
            embed.set_thumbnail(url="attachment://vgcyes.png")
            await ctx.send(file=file, embed=embed)
            return

    @filter_command.command(name="list")
    @commands.has_permissions(manage_messages=True)
    async def send_custom_list(self, ctx: commands.Context):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        if guild_config["custom-words"]:
            embed = Embed(title="Custom Words",
                          description="These words are filtered from chat within this server.",
                          color=0xff0000)

            string_of_words = str()

            for word in guild_config["custom-words"]:
                string_of_words += f"{word}\n"

            embed.add_field(name=f"There are {len(guild_config['custom-words'])} in this list:",
                            value=f"{string_of_words}")

            await ctx.send(embed=embed)
            return

        else:
            embed = Embed(title="Custom Words",
                          description="These words are filtered from chat within this server.\n\u200B",
                          color=0xff0000)
            embed.add_field(name="There are no words in this list!",
                            value="Use *filter add* to add words.")
            await ctx.send(embed=embed)
            return

    @filter_command.group(name="default")
    @commands.has_permissions(manage_messages=True)
    async def default_filter_list(self, ctx: commands.Context):
        pass

    @default_filter_list.command(name="enable")
    @commands.has_permissions(manage_messages=True)
    async def enable_default_list(self, ctx: commands.Context):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["use-default-list"] = True
        await ctx.message.add_reaction("✅")
        return

    @default_filter_list.command(name="disable")
    @commands.has_permissions(manage_messages=True)
    async def disable_default_list(self, ctx: commands.Context):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        guild_config["use-default-list"] = False
        await ctx.message.add_reaction("✅")
        return

    @commands.group(description="Add/remove users or channels to the server whitelist.",
                    invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def whitelist(self, ctx, intent=None, element=None) -> None:

        # TODO: Usage embed
        pass

    @whitelist.group(name="add",
                     invoke_without_command=True)
    async def whitelist_add(self, ctx):
        pass

    @whitelist_add.command(name="channel")
    async def whitelist_add_channel(self, ctx, channel: discord.TextChannel=None):
        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        if channel:
            guild_config["whitelisted-channels"].append(channel.id)
            await ctx.message.add_reaction("✅")
            return

    @whitelist_add.command(name="member")
    async def whitelist_add_member(self, ctx, member: discord.Member=None):
        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        if member:
            guild_config["whitelisted-members"].append(member.id)
            await ctx.message.add_reaction("✅")
            return

    @whitelist.group(name="remove",
                     invoke_without_command=True)
    async def whitelist_remove(self, ctx):
        pass

    @whitelist_remove.command(name="channel")
    async def whitelist_remove_channel(self, ctx, channel: discord.TextChannel):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        if channel and channel.id in guild_config["whitelisted-channels"]:
            guild_config["whitelisted-channels"].remove(channel.id)
            await ctx.message.add_reaction("✅")
            return

    @whitelist_remove.command(name="member")
    async def whitelist_remove_member(self, ctx, member: discord.Member):

        guild_config = admin.config[f"{ctx.guild.id}"]["chat-filter"]

        if member and member.id in guild_config["whitelisted-members"]:
            guild_config["whitelisted-members"].remove(member.id)
            await ctx.message.add_reaction("✅")
            return


def setup(bot):
    bot.add_cog(ChatFilterModule(bot))
