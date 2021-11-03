const { MessageAttachment } = require('discord.js');
const { SlashCommandBuilder } = require('@discordjs/builders');

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
            options!`,
      thumbnail: {
        url: 'attachment://vgcyes.png',
      },
      fields: [
        {
          name: 'What is a slash command?',
          value: `Slash Commands are a new, more intuitive way to interact with Admin! Commands are listed natively within the Discord client, and can be accessed by typing a forward slash.`,
          inline: false,
        },
        {
          name: 'Can I still use a dash?',
          value: `Unfortunately, no. dash commands have been removed with the advent of slash commands. All of the original functionality (and more!) is still intact, so you aren\t missing out on anything!`,
          inline: false,
        },
        {
          name: 'What is all this talk about "Jay-S"?',
          value: `JS is short for JavaScript, the programming language that is now the home of Admin! The rewrite of Admin in JavaScript comes features like slash commands with more soon to come.`,
          inline: false,
        },
      ],
    };
    return await interaction.reply({ embeds: [embed], files: [file] });
  },
};
