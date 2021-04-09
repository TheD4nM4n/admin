import json
import discord

from discord.ext import commands
from core import load_configuration, save_configuration


class RoleNotAllowed(commands.CommandError):
    pass


class ReactionRolesModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def loaded_message(self):
        print("'Roles' module loaded.")

    @commands.Cog.listener("on_raw_reaction_add")
    async def reaction_role_listener(self, reaction):

        guild_reaction_roles = load_configuration()[f"{reaction.guild_id}"]["reaction-roles"]
        if str(reaction.message_id) in guild_reaction_roles.keys():

            reaction_role_pairs = guild_reaction_roles[str(reaction.message_id)]
            print(reaction.emoji.name.encode("utf-8"))

            if reaction.emoji.name in reaction_role_pairs.keys():
                guild = self.bot.get_guild(reaction.guild_id)
                role = discord.utils.get(guild.roles, id=reaction_role_pairs[f"{reaction.emoji.name}"])

                await reaction.member.add_roles(role)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def role(self, ctx: commands.Context):
        pass

    @role.command(name="all")
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx: commands.Context, role: discord.Role):

        async with ctx.typing():

            number_of_roles_given = 0
            number_of_errors = 0

            for member in ctx.guild.members:
                if member.id != self.bot.user.id:
                    await member.add_roles(role)
                    number_of_roles_given += 1

            file = discord.File(fp="./assets/vgcrollsafe.png")
            embed = discord.Embed(title="Mass role assignment done!",
                                  description=f"Added the role {role.mention} to {number_of_roles_given}"
                                              f"members, with {number_of_errors} errors.",
                                  color=0xff0000)
            embed.set_thumbnail(url="attachment://vgcrollsafe.png")

        await ctx.send(file=file, embed=embed)

    @role_all.error
    async def all_role_error(self, ctx, error):

        if isinstance(error, commands.RoleNotFound):
            await ctx.send("That doesn't seem to be a role here. Try again with a new role!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please include a role to give.")

    # @commands.command(description="Links a message sent with roles.")
    # @commands.has_permissions(administrator=True)
    # async def link(self, ctx: commands.Context):
    #     pass

    @role.group(description="Gives the role provided (if the role is available as a self serve).",
                invoke_without_command=True)
    async def give(self, ctx: commands.Context, role: discord.Role):

        # Loads the list of roles allowed to be self-served
        self_serve_roles = load_configuration()[f"{ctx.guild.id}"]["self-serve"]

        # Gives the
        if role.id in self_serve_roles:
            await ctx.author.add_roles(role)
            await ctx.message.add_reaction("✅")
        else:
            raise RoleNotAllowed("The role specified is not in the self-serve list.")

    @give.command()
    async def list(self, ctx: commands.Context):

        # Loads the list of roles allowed to be self-served
        self_serve_roles = load_configuration()[f"{ctx.guild.id}"]["self-serve"]

        string_of_roles = str()
        if self_serve_roles:
            for role_id in self_serve_roles:
                string_of_roles += ctx.guild.get_role(role_id).mention + "\n"
            embed = discord.Embed(title="Self-Serve List",
                                  description=string_of_roles,
                                  color=0xff0000)
            embed.add_field(name="To get any of these roles, use the command below:",
                            value="*role give @role*")
            await ctx.send(embed=embed)
        else:
            await ctx.send("It seems there are no roles for self-serve in this server. Contact a server admin if you "
                           "think this is an issue. Sorry for the inconvenience!")

    @give.error
    @role_all.error
    async def general_role_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.RoleNotFound):
            await ctx.send("That doesn't seem to be a role here. Try again with a new role!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please include a role to give.")
        elif isinstance(error, RoleNotAllowed):
            await ctx.send("That role is not in the self-serve list. If this is an error, contact a server "
                           "administrator to add the role to the list. Otherwise, try again with another role in the "
                           "list!")


def setup(bot):
    bot.add_cog(ReactionRolesModule(bot))
