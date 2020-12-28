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


class ChatFilterModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("'Chat Filter' module loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Loads the chat filter configuration of the server the message was sent
        guild_config = load_configuration()[f"{message.guild.id}"]["chat-filter"]

        # If the message isn't sent by the bot or in a whitelisted channel...
        if message.author != self.bot.user or message.channel not in guild_config["whitelisted-channels"]:

            # ...check for profanity.
            if profanity.contains_profanity(message.content):
                self.filter_message(message, guild_config)
            else:
                for word in guild_config["whitelisted-channels"]:
                    if word in message.content:
                        self.filter_message(message, guild_config)

    def filter_message(self, message, config):
        await message.delete()
        if config["log-channel"]:
            log_channel = self.bot.get_channel(config["log-channel"])
            file = discord.File("./assets/vgcdisgusting.png", filename="vgcdisgusting.png")
            embed = discord.Embed(title="I have deleted a message from a channel.",
                                  description=f"Offender: {message.author.name}\n"
                                              f"Offender ID: {message.author.id}\n"
                                              f"Channel: {message.channel}\n",
                                  color=0xff0000)
            embed.add_field(name="Message content:", value=message.content)
            embed.set_thumbnail(url="attachment://vgcdisgusting.png")
            await log_channel.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(ChatFilterModule(bot))
