const { SlashCommandBuilder } = require('@discordjs/builders');
const { Permissions } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('filter')
    .setDescription('Configuration for Admin\'s built-in chat filter.'),
    async execute(interaction) {
        if (interaction.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) {
            await interaction.reply({ content: 'Work in progress. Come back later!' })
        } else {
            return await interaction.reply({ content: 'You don\'t have permission to use this command!', ephemeral: true })
        };
    },
};
