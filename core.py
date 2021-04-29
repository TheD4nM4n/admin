from os import listdir
from json import load, dump
from discord import Embed, File, Guild, Activity, ActivityType, Intents
from discord.ext import commands, tasks


class AdminBot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs['command_prefix'],
                         intents=kwargs['intents'],
                         activity=Activity(type=ActivityType.listening, name="-help"))
        self.remove_command("help")
        try:
            self.config = self.load_configuration()
        except FileNotFoundError:
            self.config = {}
        with open("./botconfig.json", "r", encoding="utf-8") as credentials:
            config_json = load(credentials)
            self.token = config_json["discord-token"]
            self.administrators = config_json["bot-administrators"]
            self.rawg_key = config_json["rawg-key"]

    async def on_ready(self):
        for module in listdir('./modules'):
            if module.endswith('.py'):
                self.load_extension(f'modules.{module[:-3]}')

        for guild in self.guilds:
            if guild.id not in self.config:
                # Loads the default config and modifies it to fit the server
                default_config = self.default_configuration
                if guild.system_channel:
                    default_config["greetings"]["channel"] = guild.system_channel.id
                default_config["name"] = guild.name

                # Adds the server to the config, with the above configuration
                self.config[f"{guild.id}"] = default_config
        # Writes the new config to disk
        self.save_configuration(self.config)

        self.config_daemon.start()

    async def on_guild_join(self, guild: Guild) -> None:

        # If the server isn't in the config file, it loads the default config and modifies it to fit the server
        if str(guild.id) not in self.config:
            default_config = self.default_configuration
            default_config["greetings"]["channel"] = guild.system_channel.id
            default_config["name"] = guild.name

            # Adds the server to the config, with the above configuration
            self.config[f"{guild.id}"] = default_config

            # Writes the new config to disk
            self.save_configuration(self.config)

    @property
    def default_configuration(self) -> dict:
        # Returns the default configuration (for use in generating new server configurations)
        return {
            "name": None,
            "greetings": {
                "enabled": True,
                "channel": None
            },
            "reaction-roles": {
                "enabled": True
            },
            "chat-filter": {
                "enabled": True,
                "log-channel": None,
                "use-default-list": True,
                "custom-words": [],
                "whitelisted-channels": [],
                "whitelisted-members": []
            },
            "mute": {
                "enabled": True,
                "muted-members": []
            }
        }

    @staticmethod
    def load_configuration() -> dict:
        # Returns the configuration stored on disk.
        with open("./data/serverconfig.json", "r", encoding="utf-8") as stored_config:
            return load(stored_config)

    @staticmethod
    def save_configuration(config) -> None:
        with open("./data/serverconfig.json", "w") as stored_config:
            # This writes the configuration with the changes made to the disk.
            dump(config, stored_config, indent=4)
            stored_config.truncate()

    async def bot_administrator_check(self, ctx):
        return ctx.author.id in self.administrators

    @tasks.loop(minutes=1.0)
    async def config_daemon(self):
        self.save_configuration(self.config)


admin = AdminBot(command_prefix="-",
                 intents=Intents.all())


@admin.command(description="Reloads the specified module, or all of them if no module is specified.")
@commands.check(admin.bot_administrator_check)
async def reload(ctx: commands.Context, module_name=None):
    if module_name is None:

        active_modules = [extension for extension in admin.extensions]

        for module_title in active_modules:
            admin.unload_extension(module_title)

        for module_title in listdir("./modules"):
            if module_title.endswith(".py"):
                admin.load_extension(f"modules.{module_title[:-3]}")

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
@commands.check(admin.bot_administrator_check)
async def modules(ctx: commands.Context):
    active_modules = ''
    for admin_module in admin.extensions:
        active_modules += f"{admin_module[8:]}\n"

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
@commands.check(admin.bot_administrator_check)
async def enable(ctx: commands.Context, module_name):
    if f"modules.{module_name}" not in admin.extensions:
        if f"{module_name.lower()}.py" in listdir("./modules"):
            admin.load_extension(f"modules.{module_name.lower()}")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("I'm sorry, but that module doesn't exist.")
    else:
        return await ctx.send(f"That module is already loaded!")


@admin.command(description="Disables a module.")
@commands.check(admin.bot_administrator_check)
async def disable(ctx: commands.Context, module_name):
    if f"modules.{module_name.lower()}" in admin.extensions:
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
    admin.run(admin.token)
