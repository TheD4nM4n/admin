from os import listdir, getenv
from discord import Embed, File, Guild, Activity, ActivityType, Intents
from discord.ext import commands, tasks
from copy import copy, deepcopy
from logging import getLogger, DEBUG, FileHandler, Formatter
import config

logger = getLogger('discord')
logger.setLevel(DEBUG)
handler = FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = getenv("TOKEN")
ADMIN = getenv("ADMIN")
PREFIX = getenv("PREFIX", "-")
CONFIG_LOCATION = "./data/serverconfig.json"

if TOKEN is None:
    raise Exception("No token provided.")
if ADMIN is None:
    print("[WARN] No bot administrator was defined. Low level bot access will be impossible!")


class AdminBot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(command_prefix=PREFIX,
                         intents=kwargs['intents'],
                         activity=kwargs['activity'],
                         help_command=None)
        self.owner_id = int(ADMIN)
        self.last_saved_config = None

    async def on_ready(self):

        for module in listdir('./modules'):
            if module.endswith('.py'):
                self.load_extension(f'modules.{module[:-3]}')

        for guild in self.guilds:
            if str(guild.id) not in config.config:

                # Loads the default config and modifies it to fit the server
                default_config = config.get_default_configuration()

                if guild.system_channel is None:
                    default_config["greetings"]["channel"] = None

                else:
                    default_config["greetings"]["channel"] = guild.system_channel.id

                default_config["name"] = guild.name

                # Adds the server to the config, with the above configuration
                config.config[f"{guild.id}"] = default_config

        # Writes the new config to disk
        self.config_daemon.start()

    async def on_guild_join(self, guild: Guild) -> None:
        # If the server isn't in the config file, it loads the default config and modifies it to fit the server
        if str(guild.id) not in config.config:
            default_config = config.get_default_configuration()
            default_config["greetings"]["channel"] = guild.system_channel.id
            default_config["name"] = guild.name

            # Adds the server to the config, with the above configuration
            config.config[f"{guild.id}"] = default_config

            # Writes the new config to disk
            config.save_data(config.config, CONFIG_LOCATION)

    @tasks.loop(minutes=1.0)
    async def config_daemon(self):
        config.save_data(config.config, CONFIG_LOCATION)
        self.last_saved_config = deepcopy(config.config)


admin = AdminBot(intents=Intents.all(),
                 activity=Activity(type=ActivityType.listening, name="-help"))


@admin.command(description="Reloads the specified module, or all of them if no module is specified.")
@commands.is_owner()
async def reload(ctx: commands.Context, module_name=None):
    if module_name is None:

        active_modules = [extension for extension in admin.extensions]

        for module_title in active_modules:
            admin.unload_extension(module_title)

        for module_title in listdir("./modules"):
            if module_title.endswith(".py"):
                admin.load_extension(f"{module_title[:-3]}")

        await ctx.message.add_reaction("✅")

    else:

        full_module_name = f'modules.{module_name}'

        if full_module_name in admin.extensions:
            admin.unload_extension(full_module_name)
            admin.load_extension(full_module_name)
            return await ctx.message.add_reaction("✅")

        admin.load_extension(full_module_name)
        await ctx.message.add_reaction("✅")


@admin.command(description="Lists all modules.")
@commands.is_owner()
async def modules(ctx: commands.Context):
    active_modules = "\n".join(admin.extensions)

    inactive_modules = ''
    for admin_module in listdir("./modules"):
        if admin_module.endswith(".py"):
            if f"modules.{admin_module[:-3]}" not in admin.extensions:
                inactive_modules += f"{admin_module[:-3]}\n"

    embed = Embed(title="Module List",
                  description="This is where you can see everything I do!",
                  color=0xff0000)

    if len(active_modules) > 0:
        embed.add_field(name=f"There are **{len(admin.extensions)}** active modules:",
                        value=active_modules)

    if len(inactive_modules) > 0:
        embed.add_field(name=f"There are **{len(inactive_modules.split())}** inactive modules:",
                        value=inactive_modules)

    await ctx.send(embed=embed)


@admin.command(description="Enables a module.")
@commands.is_owner()
async def enable(ctx: commands.Context, module_name):
    if module_name.lower() not in admin.extensions:
        if f"{module_name.lower()}.py" in listdir("./modules"):
            admin.load_extension(f"modules.{module_name.lower()}")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("I'm sorry, but that module doesn't exist.")
    else:
        return await ctx.send(f"That module is already loaded!")


@admin.command(description="Disables a module.")
@commands.is_owner()
async def disable(ctx: commands.Context, module_name):
    if module_name.lower() in admin.extensions:
        admin.remove_cog(module_name.lower())
        admin.unload_extension(f'modules.{module_name.lower()}')
        await ctx.message.add_reaction("✅")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Sorry, that module either doesn't exist, or is already disabled.")


@admin.group(name="help", description="Displays all Admin commands.", invoke_without_command=True)
async def help_command(ctx: commands.Context):
    file = File(fp="./assets/vgclove.png")

    embed = Embed(title="Help", description="Thank you for seeing what I can do!",
                  color=0xff0000)
    embed.set_thumbnail(url="attachment://vgclove.png")
    for command in admin.commands:
        command_data = admin.get_command(command.name)
        if command_data.checks:
            pass
        else:
            if command_data.description:
                embed.add_field(name=command_data.name, value=command_data.description, inline=False)
            else:
                embed.add_field(name=command_data.name, value="placeholder", inline=False)
    embed.set_footer(text="For moderator commands, execute the command '-help moderator'.")

    await ctx.send(file=file, embed=embed)


@help_command.command(name="moderator")
@commands.has_permissions(administrator=True)
async def moderator_help(ctx: commands.Context):
    file = File(fp="./assets/vgclove.png")
    embed = Embed(title="Help", description="Thank you for seeing what I can do (for administrators)!",
                  color=0xff0000)
    embed.set_thumbnail(url="attachment://vgclove.png")
    for command in admin.commands:
        command_data = admin.get_command(command.name)
        if not command_data.checks:
            pass
        else:
            if command_data.description:
                embed.add_field(name=command_data.name, value=command_data.description, inline=False)
            else:
                embed.add_field(name=command_data.name, value="placeholder", inline=False)

    await ctx.send(file=file, embed=embed)


if __name__ == "__main__":
    admin.run(TOKEN)
