// Necessary requirements
const fs = require('fs');
const { Client, Intents, Collection } = require('discord.js');
const { token } = require('./config.json');

// Client and command collection initialization 
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
client.commands = new Collection();

// Retrieval of commands and event data from ./commands and ./events
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));

// Parsing and adding commands
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
}

// Parsing and adding event listeners
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
    } else {
        client.on(event.name, (...args) => event.execute(...args));
    }
}


// Logging into Discord with access token (found in config.json)
client.login(token);