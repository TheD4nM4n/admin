const fs = require('fs');
const Filter = require('bad-words');

filter = new Filter();

module.exports = {
  name: 'messageCreate',
  once: false,
  execute(message) {
    fs.readFile('./data/guildConfig.json', (err, configFile) => {
      const config = JSON.parse(configFile);

      if (config[`${message.guildId}`]['chat-filter']['enabled']) {
        if (filter.isProfane(message.content)) {
          message.delete();
        }
      }
    });
  },
};
