import os
import json

from discord import Embed
from discord.ext import commands
from discord import Intents

bot = commands.Bot(command_prefix="-", intents=Intents.all())
bot.remove_command("help")


def load_token():

    # Returns the token stored in the "credentials.json" file.
    with open("./credentials.json", "r") as credentials:
        return json.load(credentials)["discord-token"]


def load_default_configuration():

    # Returns the default configuration (for use in generating new server configurations)
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)["default"]


def load_configuration():

    # Returns the configuration stored on disk.
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)


def save_configuration(config):
    with open("./data/serverconfig.json", "w") as stored_config:
        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


for module in os.listdir('./modules'):
    if module.endswith('.py'):
        bot.load_extension(f'modules.{module[:-3]}')


@bot.event
async def on_guild_join(guild):

    # Loads the serverconfig.json file and looks for the server in the json
    config = load_configuration()

    # If the server isn't in the config file, it loads the default config and modifies it to fit the server
    if guild.id not in config.keys():
        default_config = load_default_configuration()
        default_config["greetings"]["channel"] = guild.system_channel.id

        # Adds the server to the config, with the above configuration
        config[f"{guild.id}"] = default_config

        # Writes the new config to disk
        save_configuration(config)


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, module_name=None):
    if module_name is None:

        active_modules = [extension for extension in bot.extensions]

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

if __name__ == "__main__":
    bot.run(load_token())
