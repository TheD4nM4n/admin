const { SlashCommandBuilder } = require('@discordjs/builders');
const { ChannelType } = require('discord-api-types/v9');
const { Permissions } = require('discord.js');
const fs = require('fs');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('giveaway')
    .setDescription('A set of tools to run giveaways within your server!'),
    async execute(interaction) {
        return 0
    }
}