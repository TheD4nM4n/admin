const fs = require('fs');
const Filter = require('bad-words');
const { MessageAttachment } = require('discord.js');

const filter = new Filter();

module.exports = {
  name: 'messageCreate',
  once: false,
  execute(message) {
    fs.readFile('./data/guildConfig.json', (err, configFile) => {
      const config = JSON.parse(configFile);
      let filterEnabled = config[`${message.guildId}`]['chat-filter']['enabled'];
      let loggingEnabled = config[`${message.guildId}`]['chat-filter']['logging'];
      let logChannelId = config[`${message.guildId}`]['chat-filter']['log-channel'];

      if (filterEnabled) {
        if (filter.isProfane(message.content)) {
          message.delete();

          if (loggingEnabled === true) {
            if (logChannelId === null) {
              const owner = message.guild.members.cache.get(message.guild.ownerId);
              owner.send(
                "Hey, it seems that you have infraction logging enabled for your server, but I don't have a channel to log to. To fix this, go into your server and use the command */filter log channel*. Thank you!"
              );
            } else {
              const file = new MessageAttachment('./assets/vgcdisgusting.png');
              const logChannel = message.guild.channels.cache.get(logChannelId);
              const embed = {
                color: 0xff0000,
                title: "I've deleted a message from a channel.",
                description: `Offender: ${message.member.displayName}
                Channel: ${message.channel.name}`,
                thumbnail: {
                  url: 'attachment://vgcdisgusting.png',
                },
                fields: [
                  {
                    name: 'Message content:',
                    value: `${message.content}`,
                    inline: true,
                  },
                  {
                    name: 'Filtered message:',
                    value: `${filter.clean(message.content)}`,
                    inline: true,
                  },
                ],
              };
              logChannel.send({ files: [file], embeds: [embed] });
            }
          }
        }
      }
    });
  },
};
