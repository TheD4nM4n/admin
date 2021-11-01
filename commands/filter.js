const { SlashCommandBuilder } = require('@discordjs/builders');
const { ChannelType } = require('discord-api-types/v9');
const { Permissions } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('filter')
    .setDescription('Configuration for Admin\'s built-in chat filter.')
    .addSubcommandGroup(subcommandGroup => 
        subcommandGroup
        .setName('log')
        .setDescription('Change settings for the built-in chat filter.'))
        .addSubcommand(subcommand =>
            subcommand
            .setName('channel')
            .setDescription('Sets the channel for log messages to be sent to.'))
            .addChannelOption(builder =>
                builder
                .addChannelType(ChannelType.GuildText)
                .setName('log-channel')
                .setDescription('The channel to send infraction logs to.')
                .setRequired(true)
                ),
    async execute(interaction) {
        if (interaction.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) {
            return await interaction.reply({ content: 'Work in progress. Try again later!' });
        } else {
            return await interaction.reply({ content: 'You don\'t have permission to use this command!', ephemeral: true })
        };
    },
};
