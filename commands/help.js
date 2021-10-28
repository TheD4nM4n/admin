const { MessageEmbed, MessageAttachment } = require('discord.js')
const { SlashCommandBuilder } = require('@discordjs/builders');
const { execute } = require('../events/ready');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('help')
    .setDescription('Provides a helpful little guide into the world of Admin!'),
    async execute(interaction) {
        const file = new MessageAttachment('./assets/vgcyes.png');
        const embed = {
            color: 0xff0000,
            title: 'Welcome to Admin!',
            description: `**Admin now uses slash commands!**
            To view the list of possible commands, just
            type a forward slash (/) to view the possible
            options! For answers to some frequently asked
            questions, try "/faq"!`,
            thumbnail: {
                url: 'attachment://vgcyes.png',
            }
        };
        return await interaction.reply({ embeds: [embed], files: [file] });
    }
}