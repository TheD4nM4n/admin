const { SlashCommandBuilder, ContextMenuCommandBuilder } = require('@discordjs/builders');
const GiantBomb = require('giant-bomb');

const gb = new GiantBomb(
  '8226603f8cd63889946abcbe71a524260de50bf5',
  'TheD4nM4n/admin: A discord bot designed for teachers'
);
module.exports = {
  data: new SlashCommandBuilder()
    .setName('game')
    .setDescription('Replies with information about the game title given.')
    .addStringOption(builder => builder.setName('query').setDescription('The game to search for.').setRequired(true)),
  async execute(interaction) {
    const query = interaction.options.getString('query');
    let developerNames = '';
    let platformNames = '';

    const response = await gb.search({
      limit: 1,
      query: query,
      resources: ['game'],
      format: 'json',
    });

    console.log(response.results);

    if (response.results === undefined) {
      return await interaction.reply({
        content: 'Your query turned up no results! Was it spelled correctly?',
        ephemeral: true,
      });
    }

    const gameId = JSON.parse(
      await gb.search({
        limit: 1,
        query: query,
        resources: ['game'],
        format: 'json',
      })
    ).results[0].id;

    const gameResults = JSON.parse(
      await gb.getGame({
        id: gameId,
        fields: ['name', 'deck', 'image', 'platforms', 'developers', 'genres', 'site_detail_url'],
        format: 'json',
      })
    ).results;

    gameResults.developers.slice(0, 4).forEach(developer => {
      developerNames = developerNames.concat(`\n${developer.name}`);
    });

    gameResults.platforms.slice(0, 4).forEach(platform => {
      platformNames = platformNames.concat(`\n${platform.name}`);
    });

    if (gameResults.developers.length > 4) {
      developerNames = developerNames.concat(' (...)');
    }

    if (gameResults.platforms.length > 4) {
      platformNames = platformNames.concat(' (...)');
    }

    const embed = {
      color: 0xff0000,
      title: gameResults.name,
      url: gameResults.site_detail_url,
      author: {
        name: 'Made with Giant Bomb',
        url: 'https://www.giantbomb.com/',
      },
      description: gameResults.deck,
      thumbnail: {
        url: gameResults.image.small_url,
      },
      fields: [
        {
          name: 'Developers',
          value: developerNames,
          inline: true,
        },
        {
          name: 'Platforms',
          value: platformNames,
          inline: true,
        },
      ],
    };

    await interaction.reply({ embeds: [embed] });
  },
};
