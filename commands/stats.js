const { SlashCommandBuilder } = require('@discordjs/builders');
const { executionAsyncResource } = require('async_hooks');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('stats')
    .setDescription('Sends statistics about the current server.'),
    async executionAsyncResource(interaction) {
        await interaction.reply('Not quite built yet. Stay tuned!');
    },
};
