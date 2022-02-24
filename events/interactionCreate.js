module.exports = {
  // Command execution code
  name: "interactionCreate",
  once: false,
  execute(interaction) {
    if (!interaction.isCommand()) return;
    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) return;

    try {
      command.execute(interaction);
    } catch (error) {
      console.error(error);
      interaction.reply({
        content:
          "There was an error while running this command, please try again.",
        ephemeral: true,
      });
    }
  },
};
