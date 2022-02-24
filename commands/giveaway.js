const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('giveaway')
    .setDescription('A set of tools to run giveaways within your server!')
    .addRoleOption(role =>
      role
      .setName('role')
      .setDescription("The role to pick the winner from. To pick from all members, use @everyone.")
      .setRequired(true))
    .addStringOption(builder =>
      builder
      .setName('subject')
      .setDescription('What you are giving away.')
      .setRequired(true))
    .addBooleanOption(builder =>
      builder
      .setName("notify-winner")
      .setDescription("Send the winner a direct message to notify them.")),
    async execute(interaction) {
        const role = interaction.options.getRole('role')
        const notify = interaction.options.getBoolean('notify-winner')
        const subject = interaction.options.getString('subject')
        const winner = role.members.random()

        if (!interaction.guild.available) {
          return await interaction.reply({ content: "Sorry, the server you're in seems to be unavailable. There seems to be a server outage." })
        }

        await interaction.reply({ content: `The winner of "${subject}" is ${winner}!` })

        if (notify == true) {
          const embed = {
            color: 0xff0000,
            title: "You've won!",
            author: {
              name: winner.guild.name,
            },
            description: `You were drawn as a part of the "${subject}" giveaway in ${winner.guild.name}.
            Get in contact with ${interaction.member} for the next steps to claim your prize!`,
          }

          return await winner.send({ embeds: [ embed ] })
        }
    }
}