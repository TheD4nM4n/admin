const { SlashCommandBuilder } = require("@discordjs/builders");
const fs = require("fs");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("mute")
    .setDescription("Mutes the member for the given amount of time.")
    .addMentionableOption((builder) =>
      builder
        .setName("member")
        .setDescription("the member to be muted.")
        .setRequired(true)
    )
    .addStringOption((builder) =>
      builder
        .setName("reason")
        .setDescription("The reason this member was muted.")
    ),
  async execute(interaction) {
    const member = interaction.options.getMentionableOption("member");
    const guildConfig = fs.readFile("./data/guildConfig.json", {}, (err) => {
      if (err) {
        console.log(err);
      }
    });
    if (typeof member == "GuildMember") {
      const reason = interaction.options.getStringOption("reason");
      const guildMuteRole = interaction.guild.roles.fetch(
        guildConfig[`${interaction.guild.id}`]["mute"]["role"]
      );
      if (member.roles.cache.has(guildMuteRole)) {
        return await interaction.reply({
          embeds: [
            {
              color: 0xff0000,
              title: `Cannot mute ${member}`,
              description: "That member is already muted.",
            },
          ],
        });
      }

      let memberRoles = []
      for (role in await member.roles.cache.fetch()) {
        memberRoles.append(role.id)
      }

      guildConfig[`${interaction.guild.id}`]['mute']['muted-members'][`${member.id}`] = {
        name: `${member}`,
        roles: memberRoles
      }

      member.roles.add(guildMuteRole);
    }
  },
};
