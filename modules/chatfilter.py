import discord
import json

from discord.ext import commands
from better_profanity import profanity


def load_configuration():
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)


def save_configuration(config):
    with open("./data/serverconfig.json", "w") as stored_config:
        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


def usage_embed():
    file = discord.File(fp="./assets/vgctired.png", filename="vgctired.png")
    embed = discord.Embed(title="filter",
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

    # TODO: Add ability to bypass the default banned word list

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        config = load_configuration()
        # Loads the chat filter configuration of the server the message was sent

        print("'Chat Filter' module loaded.")

    def exempt_check(self, message, guild_config) -> bool:

        if message.author.id in guild_config["whitelisted-members"]:
            return True
        elif message.channel in guild_config["whitelisted-channels"]:
            return True
        elif message.author.id == self.bot.user.id:
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        config = load_configuration()
        # Loads the chat filter configuration of the server the message was sent
        try:
            guild_config = config[f"{message.guild.id}"]["chat-filter"]
        except KeyError:
            guild_config = config[f"{message.guild.id}"]
            guild_config["chat-filter"] = {
                "enabled": True,
                "log-channel": None,
                "custom-words": [],
                "whitelisted-channels": []
            }
            save_configuration(config)

        # If the message isn't sent by the bot, in a whitelisted channel, or sent by a whitelisted user...
        if not self.exempt_check(message, guild_config):

            if message.author.guild_permissions.administrator and "-filter add" in message.content:
                pass

            else:

                # ...check for profanity.
                if profanity.contains_profanity(message.content):

                    # Delete message
                    await message.delete()

                    # If the server has a log channel set, build an embed and send it.
                    if guild_config["log-channel"]:
                        file = discord.File("./assets/vgcdisgusting.png")
                        embed = discord.Embed(title="I have deleted a message from a channel.",
                                              description=f"Offender: {message.author.name}\n"
                                                          f"Channel: {message.channel}\n",
                                              color=0xff0000)
                        embed.add_field(name="Message content:", value=message.content)
                        embed.set_thumbnail(url="attachment://vgcdisgusting.png")
                        log_channel = self.bot.get_channel(guild_config["log-channel"])

                        return await log_channel.send(file=file, embed=embed)

                else:

                    # If it can't find a swear word, it will look through the list of custom words
                    for word in guild_config["custom-words"]:

                        if word in message.content.lower():

                            # Delete message
                            await message.delete()

                            # If the server has a log channel set, build an embed and send it.
                            if guild_config["log-channel"]:
                                file = discord.File("./assets/vgcdisgusting.png")
                                embed = discord.Embed(title="I have deleted a message from a channel.",
                                                      description=f"Offender: {message.author.name}\n"
                                                                  f"Channel: {message.channel}\n",
                                                      color=0xff0000)
                                embed.add_field(name="Message content:", value=message.content)
                                embed.set_thumbnail(url="attachment://vgcdisgusting.png")

                                log_channel = self.bot.get_channel(guild_config["log-channel"])
                                return await log_channel.send(file=file, embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def filter(self, ctx, intent=None, arg=None):

        # Gets copies of the full config file and the server-specific config
        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["chat-filter"]

        if intent:
            if intent.lower() == "enable":

                guild_config["enabled"] = True
                save_configuration(config)
                return await ctx.message.add_reaction("✅")

            elif intent.lower() == "disable":

                guild_config["enabled"] = False
                save_configuration(config)
                return await ctx.message.add_reaction("✅")

            elif intent.lower() == "set":

                channels = ctx.message.channel_mentions

                if channels:
                    guild_config["log-channel"] = channels[0].id
                    save_configuration(config)
                    return await ctx.message.add_reaction("✅")
                else:
                    if arg.lower() == "none":
                        guild_config["log-channel"] = None
                        save_configuration(config)
                        return await ctx.message.add_reaction("✅")
                    else:
                        file = discord.File(fp="./assets/vgcsad.png")
                        embed = discord.Embed(title="Sorry, something went wrong...",
                                              description="There was no channel mentioned in that message. Make sure "
                                                          "you use the hashtag (#) to properly mention the channel. "
                                                          "Go ahead and try again!",
                                              color=0xff0000)
                        embed.set_thumbnail(url="attachment://vgcsad.png")
                        return await ctx.send(file=file, embed=embed)

            elif intent.lower() == "add":

                if arg:
                    guild_config["custom-words"].append(arg.lower())
                    save_configuration(config)
                    return await ctx.message.add_reaction("✅")

                else:
                    file = discord.File(fp="./assets/vgcsad.png")
                    embed = discord.Embed(title="Sorry, something went wrong...",
                                          description="It looks like you didn't provide a word. Try again with a "
                                                      "word, like *filter add admin*.",
                                          color=0xff0000)
                    embed.set_thumbnail(url="attachment://vgcsad.png")
                    return await ctx.send(file=file, embed=embed)
                    pass

            elif intent.lower() == "remove":

                if arg:
                    if arg in guild_config["custom-words"]:
                        guild_config["custom-words"].remove(arg.lower())
                        save_configuration(config)
                        return await ctx.message.add_reaction("✅")
                    else:
                        file = discord.File(fp="./assets/vgcyes.png")
                        embed = discord.Embed(title="That word wasn't found...",
                                              description="Looks like you didn't need to run that command, "
                                                          "because that word isn't in your server's list!",
                                              color=0xff0000)
                        embed.set_thumbnail(url="attachment://vgcyes.png")
                        return await ctx.send(file=file, embed=embed)

                else:
                    file = discord.File(fp="./assets/vgcsad.png")
                    embed = discord.Embed(title="Sorry, something went wrong...",
                                          description="It looks like you didn't provide a word. Try again with a "
                                                      "word, like *filter remove admin*.",
                                          color=0xff0000)
                    embed.set_thumbnail(url="attachment://vgcsad.png")
                    return await ctx.send(file=file, embed=embed)

            elif intent.lower() == "list":

                if guild_config["custom-words"]:
                    embed = discord.Embed(title="Custom Words",
                                          description="These words are filtered from chat within this server.",
                                          color=0xff0000)

                    string_of_words = str()

                    for word in guild_config["custom-words"]:
                        string_of_words += f"{word}\n"

                    embed.add_field(name=f"There are {len(guild_config['custom-words'])} in this list:",
                                    value=f"{string_of_words}")

                    return await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Custom Words",
                                          description="These words are filtered from chat within this server.\n\u200B",
                                          color=0xff0000)
                    embed.add_field(name="There are no words in this list!",
                                    value="Use *filter add* to add words.")
                    return await ctx.send(embed=embed)

            else:
                message = usage_embed()
                return await ctx.send(file=message[0], embed=message[1])

        else:
            message = usage_embed()
            return await ctx.send(file=message[0], embed=message[1])

    @commands.command()
    async def whitelist(self, ctx, intent=None, element=None) -> None:

        config = load_configuration()
        guild_config = config[f"{ctx.guild.id}"]["chat-filter"]

        if intent:

            if intent.lower() == "add":

                if element:

                    if element.lower() == "channel":
                        channels = ctx.message.channel_mentions

                        if channels:
                            guild_config["whitelisted-channels"].append(channels[0].id)
                            save_configuration(config)
                            await ctx.message.add_reaction("✅")
                            return

                    elif element.lower() == "member":
                        mentions = ctx.message.mentions

                        if mentions:
                            guild_config["whitelisted-channels"].remove(mentions[0].id)
                            save_configuration(config)
                            await ctx.message.add_reaction("✅")
                            return

            elif intent.lower() == "remove":

                if element:

                    if element.lower() == "channel":
                        channels = ctx.message.channel_mentions

                        if channels and channels[0].id in guild_config["whitelisted-channels"]:
                            guild_config["whitelisted-channels"].remove(channels[0].id)
                            save_configuration(config)
                            await ctx.message.add_reaction("✅")
                            return

                    elif element.lower() == "member":
                        mentions = ctx.message.mentions

                        if mentions and mentions[0].id in guild_config["whitelisted-members"]:
                            guild_config["whitelisted-channels"].remove(mentions[0].id)
                            save_configuration(config)
                            await ctx.message.add_reaction("✅")
                            return
                        pass

                pass

        else:

            # TODO: usage embed
            pass


def setup(bot):
    bot.add_cog(ChatFilterModule(bot))
