import os
import json

from discord import Embed, File
from discord.ext import commands
from discord import Intents

bot = commands.Bot(command_prefix="-", intents=Intents.all())
bot.remove_command("help")


def load_token() -> str:

    # Returns the token stored in the "credentials.json" file.
    with open("./credentials.json", "r") as credentials:
        return json.load(credentials)["discord-token"]


def load_default_configuration() -> dict:

    # Returns the default configuration (for use in generating new server configurations)
    with open("./data/serverconfig.json", "r") as stored_config:
        return json.load(stored_config)["default"]


def load_configuration() -> dict:

    # Returns the configuration stored on disk.
    with open("./data/serverconfig.json", "r", encoding="utf-8") as stored_config:
        return json.load(stored_config)


def save_configuration(config) -> None:
    with open("./data/serverconfig.json", "w") as stored_config:
        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


for module in os.listdir('./modules'):
    if module.endswith('.py'):
        bot.load_extension(f'modules.{module[:-3]}')


@bot.event
async def on_ready():
    config = load_configuration()

    for guild in bot.guilds:
        if str(guild.id) not in config.keys():

            # Loads the default config and modifies it to fit the server
            default_config = load_default_configuration()
            default_config["greetings"]["channel"] = guild.system_channel.id
            default_config["name"] = guild.name

            # Adds the server to the config, with the above configuration
            config[f"{guild.id}"] = default_config

    # Writes the new config to disk
    save_configuration(config)


@bot.event
async def on_guild_join(guild):

    # Loads the serverconfig.json file and looks for the server in the json
    config = load_configuration()

    # If the server isn't in the config file, it loads the default config and modifies it to fit the server
    if guild.id not in config.keys():
        default_config = load_default_configuration()
        default_config["greetings"]["channel"] = guild.system_channel.id
        default_config["name"] = guild.name

        # Adds the server to the config, with the above configuration
        config[f"{guild.id}"] = default_config

        # Writes the new config to disk
        save_configuration(config)


@bot.command(description="Reloads the specified module, or all of them if no module is specified.")
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


@bot.command(description="Lists all modules.")
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


@bot.command(description="Enables a module.")
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


@bot.command(description="Disables a module.")
@commands.has_permissions(administrator=True)
async def disable(ctx, module_name):
    if f"modules.{module_name.lower()}" in bot.extensions:
        bot.remove_cog(module_name.lower())
        bot.unload_extension(f'modules.{module_name.lower()}')
        await ctx.message.add_reaction("✅")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Sorry, that module either doesn't exist, or is already disabled.")


@bot.command(name="help", description="Displays all Admin commands.")
async def help_command(ctx, arg=None):
    file = File(fp="./assets/vgclove.png")
    if arg is None:
        embed = Embed(title="Help", description="Thank you for seeing what I can do!",
                      color=0xff0000)
        embed.set_thumbnail(url="attachment://vgclove.png")
        for command in bot.commands:
            command_data = commands.Bot.get_command(bot, command.name)
            if command_data.checks:
                pass
            else:
                if command_data.description:
                    embed.add_field(name=command_data.name, value=command_data.description, inline=False)
                else:
                    embed.add_field(name=command_data.name, value="placeholder", inline=False)
        embed.set_footer(text="For moderator commands, execute the command '-help moderator'.")
    elif arg == "moderator":
        embed = Embed(title="Help", description="Thank you for seeing what I can do (for administrators)!",
                      color=0xff0000)
        embed.set_thumbnail(url="attachment://vgclove.png")
        for command in bot.commands:
            if ctx.author.guild_permissions.administrator:
                command_data = commands.Bot.get_command(bot, command.name)
                if not command_data.checks:
                    pass
                else:
                    if command_data.description:
                        embed.add_field(name=command_data.name, value=command_data.description, inline=False)
                    else:
                        embed.add_field(name=command_data.name, value="placeholder", inline=False)
    else:
        return
    await ctx.send(file=file, embed=embed)

if __name__ == "__main__":
    bot.run(load_token())
