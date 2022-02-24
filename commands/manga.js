const { SlashCommandBuilder } = require("@discordjs/builders");
const Anilist = require("anilist-node");
const { anilistToken } = require("../config.json");

const anilist = new Anilist(anilistToken);

module.exports = {
  data: new SlashCommandBuilder()
    .setName("manga")
    .setDescription(
      "Searches for the game provided, and returns information about it."
    )
    .addStringOption((builder) =>
      builder
        .setName("query")
        .setDescription("The manga to search for.")
        .setRequired(true)
    ),
  async execute(interaction) {
    const query = interaction.options.getString("query");
    const results = await anilist.searchEntry.manga(query, null, 1, 1);

    if (!results.media[0]) {
      return await interaction.reply({
        content: "Your query turned up no results! Was it spelled correctly?",
        ephemeral: true,
      });
    }

    const mangaData = await anilist.media.manga(results.media[0].id);

    let embed = {
      color: 0xff0000,
      title: mangaData.title.romaji,
      url: mangaData.siteUrl,
      author: {
        name: "Made with Anilist",
        url: "https://www.anilist.co/",
      },
      description: `English: ${mangaData.title.english}`,
      thumbnail: {
        url: mangaData.coverImage.medium,
      },
      fields: [
        {
          name: "Description",
          value: "",
          inline: false,
        },
        {
          name: "Average Score",
          value: `${mangaData.averageScore}`,
          inline: true,
        },
        {
          name: "Genre",
          value: mangaData.genres[0],
          inline: true,
        },
      ],
    };

    if (mangaData.title.english === null) {
      embed.description = "English: None";
    }

    if (mangaData.description === null) {
      embed.fields[0] = {
        name: "Description",
        value: "None",
        inline: false,
      };
    } else {
      embed.fields[0] = {
        name: "Description",
        value: mangaData.description.split("<")[0],
        inline: false,
      };
    }

    if (mangaData.averageScore === null) {
      embed.fields[1] = {
        name: "Average Score",
        value: "None",
        inline: false,
      };
    }
    return await interaction.reply({ embeds: [embed] });
  },
};
