from os import getenv
from discord import Embed, File
from discord.ext import commands
from html import unescape
from Pymoe import Anilist
from re import sub, compile
import aiohttp

KEY = getenv("RAWG_KEY")
db = Anilist()


def beautify_for_description(raw_html) -> str:
    formatted_text = raw_html.replace("<br>", "").replace("<i>", "*").replace("</i>", "*")
    cleaned_text_paragraph = sub(compile('<.*?>'), '', formatted_text).split("\n")[0]
    final_text = cleaned_text_paragraph[:375] + (cleaned_text_paragraph[375:] and '... (cont.)')
    return final_text


def clean_text(raw_html) -> str:
    unescaped_html = unescape(raw_html)
    cleaner_text = sub(compile("<.*?>"), '', unescaped_html)
    final_text = (cleaner_text[:225] + (cleaner_text[225:] and '...')).split("\n")[0]
    return final_text


async def get_game(name):
    # Gets game information from rawg.io
    async with aiohttp.ClientSession() as session:
        url = f"https://api.rawg.io/api/games?key={KEY}&search={name}&page_size=1"
        async with session.get(url) as resp:
            result = await resp.json()
            print(result)

        slug = result['results'][0]['slug']

        url = f"https://api.rawg.io/api/games/{slug}?key={KEY}"
        async with session.get(url) as resp:
            result = await resp.json()
            return result


class InfoModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("'Info' module loaded.")

    @commands.command(name="game",
                      description="Provides details on the specified game.")
    async def game_command(self, ctx: commands.Context, *, arg=None):

        # Makes the bot look like it is typing.
        # Helpful for showing the bot isn't just broken.
        await ctx.trigger_typing()

        # See get_game method
        game = await get_game(arg)

        # See clean_text method
        cleaned_description = clean_text(game["description"])

        # Sets up the embedded message
        file = File(fp="./assets/rawg.jpg", filename="rawg.jpg")
        embed = Embed(title=game['name'],
                      description=cleaned_description,
                      color=0xff0000)
        embed.set_author(name="Made with RAWG", url="https://rawg.io", icon_url="attachment://rawg.jpg")
        embed.set_thumbnail(url=game['background_image'])

        # Initial variables
        platform_list = str()

        embed.add_field(name="Publisher", value=game['publishers'][0]['name'])

        # Makes a string of all platforms a game is on (up to 4)
        for platform in game['platforms'][:4]:
            platform_list += f"{platform['platform']['name']}\n"

        # Adds ending with the remaining amount of platforms (if there is more than 4)
        if len(game['platforms']) > 4:
            platform_list += f"...and {len(game['platforms']) - 4} more"
        embed.add_field(name="Platforms", value=platform_list)

        # Sending da embed
        await ctx.send(file=file, embed=embed)

    @commands.command(name="anime",
                      description="Searches anime based on the name entered, and sends back some basic information.")
    async def anime_command(self, ctx, *, query: str = None):

        async with ctx.typing():
            # Retrieves a search result from Anilist, then pulls more information from the 1st result
            results = db.search.anime(f"{query}")
            anime = db.get.anime(results['data']['Page']['media'][0]['id'])['data']['Media']

            # Beautifies description for sending to Discord
            anime_description = beautify_for_description(anime['description'])

            # Constructs embed for sending
            embed = Embed(title=f"{anime['title']['romaji']}",
                          description=f"English: {anime['title']['english']}",
                          color=0xff0000)
            embed.set_thumbnail(url=anime['coverImage']['large'])
            embed.add_field(name="Description",
                            value=f"{anime_description}",
                            inline=False)
            embed.add_field(name="Average Score",
                            value=f"{anime['averageScore']}")
            embed.add_field(name="Genre",
                            value=f"{anime['genres'][0]}")

        # Sends the embed
        await ctx.send(embed=embed)

    @commands.command(name="manga",
                      description="Searches manga based on the name entered, and sends back some basic information.")
    async def manga_command(self, ctx, *, query: str):

        async with ctx.typing():
            # Retrieves a search result from Anilist, then pulls more information from the 1st result
            results = db.search.manga(f"{query}")
            manga = db.get.manga(results['data']['Page']['media'][0]['id'])['data']['Media']

            # Beautifies description for sending to Discord
            if manga['description']:
                manga_description = beautify_for_description(manga['description'])

            # Constructs embed for sending
            embed = Embed(title=f"{manga['title']['romaji']}",
                          description=f"English: {manga['title']['english']}",
                          color=0xff0000)
            embed.set_thumbnail(url=manga['coverImage']['large'])

            if manga['description']:
                embed.add_field(name="Description",
                                value=f"{manga_description}",
                                inline=False)
            embed.add_field(name="Average Score",
                            value=f"{manga['averageScore']}")
            embed.add_field(name="Genre",
                            value=f"{manga['genres'][0]}")

        # Sends the embed
        await ctx.send(embed=embed)

    @manga_command.error
    @anime_command.error
    @game_command.error
    async def info_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, IndexError):
            await ctx.send(f"The search turned up no results! Try again with a different search.")


def setup(bot):
    bot.add_cog(InfoModule(bot))
