from discord import Embed, File
from discord.ext import commands
from rawgpy import RAWG
from html import unescape
import re


def clean_text(raw_html):
    unescaped_html = unescape(raw_html)
    cleaner = re.compile("<.*?>")
    cleaner_text = re.sub(cleaner, '', unescaped_html)
    cleanerer_text = cleaner_text[:225] + (cleaner_text[225:] and '...')
    final_text = cleanerer_text.split("\n")[0]
    return final_text


def get_game(name):

    # Gets game information from rawg.io
    rawg = RAWG("047ce837ca0c424394cde59a35cf73f4")
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

    @commands.command()
    async def game(self, ctx, *, arg=None):

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
