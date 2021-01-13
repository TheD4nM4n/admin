import json
import discord

from discord.ext import commands


def load_configuration() -> dict:

    # Returns the configuration stored on disk.
    with open("./data/serverconfig.json", "r", encoding="utf-8") as stored_config:
        return json.load(stored_config)


def save_configuration(config) -> None:
    with open("./data/serverconfig.json", "w") as stored_config:
        # This writes the configuration with the changes made to the disk.
        json.dump(config, stored_config, indent=4)
        stored_config.truncate()


class ReactionRolesModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("'Reaction Roles' module loaded.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):

        guild_reaction_roles = load_configuration()[f"{reaction.guild_id}"]["reaction-roles"]
        if str(reaction.message_id) in guild_reaction_roles.keys():

            reaction_role_pairs = guild_reaction_roles[str(reaction.message_id)]
            print(reaction.emoji.name.encode("utf-8"))

            if reaction.emoji.name in reaction_role_pairs.keys():

                guild = self.bot.get_guild(reaction.guild_id)
                role = discord.utils.get(guild.roles, id=reaction_role_pairs[f"{reaction.emoji.name}"])

                await reaction.member.add_roles(role)


def setup(bot):
    bot.add_cog(ReactionRolesModule(bot))
