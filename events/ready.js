const fs = require("fs");
const defaultConfig = {
  name: null,
  greetings: {
    enabled: true,
    channel: null,
  },
  "reaction-roles": {
    enabled: true,
  },
  "chat-filter": {
    enabled: true,
    logging: true,
    "log-channel": null,
    "use-default-list": true,
    "custom-words": [],
    "whitelisted-channels": [],
    "whitelisted-members": [],
  },
  mute: {
    enabled: true,
    role: null,
    "muted-members": [],
  },
};

module.exports = {
  name: "ready",
  once: true,
  execute(client) {
    console.log(`Successfully logged in as ${client.user.username}.`);

    fs.readFile("./data/guildConfig.json", (err, configFile) => {
      const config = JSON.parse(configFile);

      client.guilds.cache.forEach((guild) => {
        if (config[`${guild.id}`] === undefined) {
          const guildConfig = JSON.parse(JSON.stringify(defaultConfig));

          if (guild.systemChannel) {
            guildConfig["greetings"]["channel"] = guild.systemChannel.id;
          }

          guildConfig["name"] = guild.name;
          config[`${guild.id}`] = guildConfig;
        } else {
          if (config[`${guild.id}`]["mute"]["role"] == null) {
            const mutedRole = await guild.roles.create({
              data: {
                name: "Muted",
              },
              reason: "Role autogenerated by Admin",
            });

            config[`${guild.id}`]["mute"]["role"] = mutedRole.id;
          }
        }
      });

      const writableConfig = JSON.stringify(config, null, 2);

      fs.writeFile("./data/guildConfig.json", writableConfig, (err) => {
        if (err) {
          console.log(err);
        }
      });
    });
  },
};
