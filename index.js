// Necessary requirements
const fs = require('fs');
const { Client, Intents, Collection } = require('discord.js');
const { token } = require('./config.json');

// Client and command collection initialization 
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });
client.commands = new Collection();

// Retrieval and parsing of commands in './commands' directory
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
}

// Log on ready state
client.once('ready', () => {
    console.log(`Successfully logged in as ${client.user.username}.`);
});

// Command execution
client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;
    const command = client.commands.get(interaction.commandName);

    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        await interaction.reply({ content: 'There was an error while running this command, please try again.', ephemeral: true });
    }
});

// Logging into Discord with access token (found in config.json)
client.login(token);