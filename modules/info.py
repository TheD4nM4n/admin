from discord import Embed, File
from discord.ext import commands
from rawgpy import RAWG
from html import unescape

import json
import re


def get_key(application):
    with open("./credentials.json") as credentials:
        keys = json.load(credentials)
        return keys[application]


rawg = RAWG(get_key("rawg-key"))


def clean_text(raw_html):
    unescaped_html = unescape(raw_html)
    cleaner = re.compile("<.*?>")
    cleaner_text = re.sub(cleaner, '', unescaped_html)
    cleanerer_text = cleaner_text[:225] + (cleaner_text[225:] and '...')
    final_text = cleanerer_text.split("\n")[0]
    return final_text


def get_game(name):
    # Gets game information from rawg.io
    results = rawg.search(name)
    game = results[0]
    game.populate()

    # Prepares name for screenshot GET request
    name_with_underscores = game.name.lower().replace(" ", "-")
    final_name = re.sub("[^\\w-]+", "", name_with_underscores)
    print(final_name)

    # Gets screenshots of game
    photos = rawg.get_request(url=f"https://api.rawg.io/api/games/{final_name}/screenshots")

    # Returns the items
    return game, photos["results"][0]["image"]


class InfoModule(commands.Cog):

    def __init__(self, bot):
        # Discord.py things
        self.bot = bot

    @commands.command(description="Provides details on the specified game.")
    async def game(self, ctx, *, arg=None):

        # Makes the bot look like it is typing.
        # Helpful for showing the bot isn't just broken.
        await ctx.trigger_typing()

        # See get_game method
        game, image = get_game(arg)

        # See clean_text method
        cleaned_description = clean_text(game.description)

        # Sets up the embedded message
        file = File(fp="./assets/rawg.jpg", filename="rawg.jpg")
        embed = Embed(title=game.name,
                      description=cleaned_description,
                      url=None,
                      color=0xff0000)
        embed.set_author(name="Made with RAWG", url="https://rawg.io", icon_url="attachment://rawg.jpg")
        embed.set_thumbnail(url=image)

        # Initial variables
        platform_list = str()
        publisher_list = str()

        # Makes a string of all publishers for a game
        for publisher in game.publishers:
            publisher_list += f"{publisher.name}\n"
        embed.add_field(name="Publishers", value=publisher_list)

        # Makes a string of all platforms a game is on (up to 4)
        for platform in game.platforms[:4]:
            platform_list += f"{platform.name}\n"

        # Adds ending with the remaining amount of platforms (if there is more than 4)
        if len(game.platforms) > 4:
            platform_list += f"...and {len(game.platforms) - 4} more"
        embed.add_field(name="Platforms", value=platform_list)

        # Sending da embed
        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(InfoModule(bot))
