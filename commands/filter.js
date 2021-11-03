const { SlashCommandBuilder } = require('@discordjs/builders');
const { ChannelType } = require('discord-api-types/v9');
const { Permissions } = require('discord.js');
const fs = require('fs');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('filter')
    .setDescription("Configuration for Admin's built-in chat filter.")
    .addSubcommand(subcommand => subcommand.setName('enable').setDescription('Enables chat filtering in this server.'))
    .addSubcommand(subcommand =>
      subcommand.setName('disable').setDescription('Disables chat filtering in this server.')
    )
    .addSubcommandGroup(subcommandGroup =>
      subcommandGroup
        .setName('log')
        .setDescription('Change settings for the built-in chat filter.')
        .addSubcommand(subcommand =>
          subcommand
            .setName('channel')
            .setDescription('Sets the channel for log messages to be sent to.')
            .addChannelOption(builder =>
              builder
                .addChannelType(ChannelType.GuildText)
                .setName('log-channel')
                .setDescription('The channel to send infraction logs to.')
                .setRequired(true)
            )
        )
        .addSubcommand(subcommand =>
          subcommand.setName('enable').setDescription('Enables infraction logging for the server.')
        )
        .addSubcommand(subcommand =>
          subcommand.setName('disable').setDescription('Disables infraction logging for the server.')
        )
    ),
  async execute(interaction) {
    if (interaction.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) {
      const config = JSON.parse(fs.readFileSync('./data/guildConfig.json'));
      console.log(interaction.options.getSubcommandGroup((required = false)));
      if (interaction.options.getSubcommandGroup((required = false)) === 'log') {
        switch (interaction.options.getSubcommand()) {
          case 'channel':
            const channel = interaction.options.getChannel('log-channel');
            config[`${interaction.guildId}`]['chat-filter']['log-channel'] = channel.id;
            fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
              if (err) {
                return console.log(err);
              } else {
                return interaction.reply({
                  content: `Logging channel set as ${channel.name}!`,
                  ephemeral: true,
                });
              }
            });
            break;
          case 'enable':
            config[`${interaction.guildId}`]['chat-filter']['logging'] = true;
            fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
              if (err) {
                return console.log(err);
              } else {
                return interaction.reply({
                  content: `Enabled infraction logging!`,
                  ephemeral: true,
                });
              }
            });
            break;
          case 'disable':
            config[`${interaction.guildId}`]['chat-filter']['logging'] = false;
            fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
              if (err) {
                return console.log(err);
              } else {
                return interaction.reply({
                  content: `Disabled infraction logging!`,
                  ephemeral: true,
                });
              }
            });
        }
      } else if (interaction.options.getSubcommand() === 'enable') {
        config[`${interaction.guildId}`]['chat-filter']['enabled'] = true;
        fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
          if (err) {
            return console.log(err);
          } else {
            return interaction.reply({
              content: `Enabled chat filter!`,
              ephemeral: true,
            });
          }
        });
      } else if (interaction.options.getSubcommand() === 'disable') {
        config[`${interaction.guildId}`]['chat-filter']['enabled'] = false;
        fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
          if (err) {
            return console.log(err);
          } else {
            return interaction.reply({
              content: `Disabled chat filter!`,
              ephemeral: true,
            });
          }
        });
      }
    } else {
      return await interaction.reply({
        content: "You don't have permission to use this command!",
        ephemeral: true,
      });
    }
  },
};
