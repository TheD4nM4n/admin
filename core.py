import os

from discord import Embed
from discord.ext import commands
from discord import Intents

bot = commands.Bot(command_prefix="-", intents=Intents.all())
bot.remove_command("help")

with open("token.txt", "r") as token:
    TOKEN = token.read()

for module in os.listdir('./modules'):
    if module.endswith('.py'):
        bot.load_extension(f'modules.{module[:-3]}')


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, module_name=None):
    if module_name is None:

        active_modules = []
        for extension in bot.extensions:
            active_modules.append(extension)

        for module_title in active_modules:
            bot.unload_extension(module_title)

        for module_title in os.listdir("./modules"):
            if module_title.endswith(".py"):
                bot.load_extension(f"modules.{module_title[:-3]}")

        await ctx.message.add_reaction("✅")
    else:

        full_module_name = f'modules.{module_name}'

        if full_module_name in bot.extensions:
            bot.unload_extension(full_module_name)
            bot.load_extension(full_module_name)
            return await ctx.message.add_reaction("✅")

        bot.load_extension(full_module_name)
        await ctx.message.add_reaction("✅")


@bot.command()
@commands.has_permissions(administrator=True)
async def modules(ctx):
    active_modules = ''
    for bot_module in bot.extensions:
        active_modules += f"{bot_module[8:]}\n"

    inactive_modules = ''
    for bot_module in os.listdir("./modules"):
        if bot_module.endswith(".py"):
            if f"modules.{bot_module[:-3]}" not in bot.extensions:
                inactive_modules += f"{bot_module[:-3]}\n"

    embed = Embed(title="Module List",
                  description="This is where you can see everything I do!")

    if len(active_modules) > 0:
        embed.add_field(name=f"There are **{len(bot.extensions)}** active modules:",
                        value=active_modules)

    if len(inactive_modules) > 0:
        embed.add_field(name=f"There are **{len(inactive_modules.split())}** inactive modules:",
                        value=inactive_modules)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def enable(ctx, module_name):
    if f"modules.{module_name}" not in bot.extensions:
        if f"{module_name.lower()}.py" in os.listdir("./modules"):
            bot.load_extension(f"modules.{module_name.lower()}")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("I'm sorry, but that module doesn't exist.")
    else:
        return await ctx.send(f"That module is already loaded!")


@bot.command()
@commands.has_permissions(administrator=True)
async def disable(ctx, module_name):
    if f"modules.{module_name.lower()}" in bot.extensions:
        bot.remove_cog(module_name.lower())
        bot.unload_extension(f'modules.{module_name.lower()}')
        await ctx.message.add_reaction("✅")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Sorry, that module either doesn't exist, or is already disabled.")


bot.run(TOKEN)
