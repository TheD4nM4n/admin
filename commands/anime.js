const { SlashCommandBuilder } = require("@discordjs/builders");
const Anilist = require("anilist-node");
const { anilistToken } = require("../config.json");

// Anilist API object initialization
const anilist = new Anilist(anilistToken);

module.exports = {
  data: new SlashCommandBuilder()
    .setName("anime")
    .setDescription(
      "Searches for the anime provided, and returns information about it."
    )
    .addStringOption((builder) =>
      builder
        .setName("query")
        .setDescription("The anime to search for.")
        .setRequired(true)
    ),
  async execute(interaction) {
    // Fetching results from Anilist
    const query = interaction.options.getString("query");
    const results = await anilist.searchEntry.anime(query, null, 1, 1);

    // No search results error handling
    if (!results.media[0]) {
      return await interaction.reply({
        content: "Your query turned up no results! Was it spelled correctly?",
        ephemeral: true,
      });
    }

    const animeData = await anilist.media.anime(results.media[0].id);

    // Use object instead of embed builders to hopefully dodge any changes with discord.js methods
    const embed = {
      color: 0xff0000,
      title: animeData.title.romaji,
      url: animeData.siteUrl,
      author: {
        name: "Made with Anilist",
        url: "https://www.anilist.co/",
      },
      description: `English: ${animeData.title.english}`,
      thumbnail: {
        url: animeData.coverImage.medium,
      },
      fields: [
        {
          name: "Description",
          value: animeData.description.split("<")[0],
          inline: false,
        },
        {
          name: "Average Score",
          value: `${animeData.averageScore}`,
          inline: true,
        },
        {
          name: "Genre",
          value: animeData.genres[0],
          inline: true,
        },
      ],
    };

    return await interaction.reply({ embeds: [embed] });
  },
};
