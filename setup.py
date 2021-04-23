import json

bot_config_dict = {}

try:
    bot_config = open("botconfig.json", "x")
    bot_config.close()
except FileExistsError:
    print("File botconfig.json already exists within this directory. PLease delete before running again.")
    exit(1)
finally:
    bot_config = open("botconfig.json", "w")

print("Admin Official Setup\n"
      "--------------------\n"
      "This will walk you through the setup for making a new instance of Admin. Start by putting your Discord bot\n"
      "token here:", end="")
token = input()

bot_config_dict["discord-token"] = token

print("Perfect. Now, let's get your RAWG key, for -game:", end="")

rawg_key = input()
bot_config_dict["rawg-key"] = rawg_key

print("One more thing, let's get the IDs of your bot administrators! These are Discord user IDs for people who will\n"
      "be able to access the framework of your bot through Discord commands, like enabling or disabling modules. This\n"
      "section will loop infinitely until you type 'done', so you can put as many administrators as you would like.")

bot_config_dict["bot-administrators"] = []

while __name__ == "__main__":
    bot_admin_id = input("Enter an ID here, or 'done' if complete: ")
    if bot_admin_id.lower() == "done":
        break
    else:
        try:
            bot_config_dict['bot-administrators'].append(int(bot_admin_id))
        except ValueError:
            print("That value is not a valid ID, try again.")

json.dump(bot_config_dict, bot_config, indent=4)

print("Your bot is all set up! Now run core.py to start your bot!")
