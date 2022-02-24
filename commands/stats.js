const { MessageEmbed } = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("stats")
    .setDescription("Sends statistics about the current server."),
  async execute(interaction) {
    const sent = await interaction.reply({
      content: "Loading...",
      fetchReply: true,
    });
    const embed = new MessageEmbed()
      .setColor("#ff0000")
      .setTitle(interaction.guild.name)
      .setDescription(`Server statistics for ${interaction.guild.name}`)
      .setThumbnail(interaction.guild.iconURL())
      .addFields(
        {
          name: "Member Statistics",
          value: `Member count: ${interaction.guild.memberCount}\nAverage members/day: *Coming Soon*`,
          inline: true,
        },
        {
          name: "Bot Statistics",
          value: `Bot Latency: ${
            sent.createdTimestamp - interaction.createdTimestamp
          }ms`,
          inline: true,
        }
      );
    await interaction.editReply({ content: "\u200b", embeds: [embed] });
  },
};
