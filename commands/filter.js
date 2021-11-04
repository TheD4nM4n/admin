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
    )
    .addSubcommandGroup(subcommandGroup =>
      subcommandGroup
        .setName('list')
        .setDescription('Changes settings for the list of words banned by Admin.')
        .addSubcommand(subcommand =>
          subcommand
            .setName('add')
            .setDescription('Adds the defined word to the list of banned words for the server.')
            .addStringOption(builder =>
              builder.setName('word').setDescription('Word to add to the list of banned words.').setRequired(true)
            )
        )
        .addSubcommand(subcommand =>
          subcommand
            .setName('remove')
            .setDescription("Removes the word listed from this server's list.")
            .addStringOption(builder =>
              builder.setName('word').setDescription('Word to remove from the list of banned words.').setRequired(true)
            )
        )
        .addSubcommand(subcommand =>
            subcommand
            .setName('default')
            .setDescription('Allows enabling or disabling of the built-in list of banned words.')
            .addStringOption(option =>
                option
                .setName('state')
                .setDescription('The state you would like the built-in profanity list to use.')
                .setRequired(true)
                .addChoice('enable', 'enable')
                .addChoice('disable', 'disable')
                )
            )
    ),
  async execute(interaction) {
    if (interaction.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) {
      const config = JSON.parse(fs.readFileSync('./data/guildConfig.json'));
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
            break;
        }
      } else if (interaction.options.getSubcommandGroup((required = false)) === 'list') {
        switch (interaction.options.getSubcommand()) {
          case 'add':
            const wordToAdd = interaction.options.getString('word');
            config[`${interaction.guildId}`]['chat-filter']['custom-words'].push(wordToAdd);
            fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
              if (err) {
                return console.log(err);
              } else {
                return interaction.reply({
                  content: `Added word ${wordToAdd} to the list. To remove, use \`/filter list remove\`.`,
                  ephemeral: true,
                });
              }
            });
            break;

          case 'remove':
            const wordList = config[`${interaction.guildId}`]['chat-filter']['custom-words'];
            const wordToRemove = interaction.options.getString('word');
            const index = wordList.indexOf(wordToRemove);
            if (index > -1) {
              wordList.splice(index, 1);
            } else {
              return interaction.reply({
                content: `The word '${wordToRemove}' wasn't found in the list. You should be good to go!`,
                ephemeral: true,
              });
            }
            fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
              if (err) {
                return console.log(err);
              } else {
                return interaction.reply({
                  content: `Removed word ${wordToRemove} from the list!`,
                  ephemeral: true,
                });
              }
            });
            break;

            case 'default':
                const state = interaction.options.getString('state');
                let messageContent = ''
                if (state === 'enable') {
                    config[`${interaction.guildId}`]['chat-filter']['use-default-list'] = true;
                    messageContent = 'Enabled default list filtering!';
                } else {
                    config[`${interaction.guildId}`]['chat-filter']['use-default-list'] = false;
                    messageContent = 'Disabled default list filtering!';
                }
                fs.writeFile('./data/guildConfig.json', JSON.stringify(config, null, 2), err => {
                    if (err) {
                        return console.log(err);
                    } else {
                        return interaction.reply({
                            content: messageContent,
                            ephemeral: true,
                        });
                    }
                });
                break;
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
