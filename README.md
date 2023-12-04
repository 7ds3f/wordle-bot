# BOTTLE

A Discord Wordle bot.

Created by EggieVAL, CasterNinja, LucaVits, SoumayahIlias, timcuber37, and 7ds3f.

## Requirements
This bot requires Python, PyEnchant, Discord, and Requests to function properly.
- To install Python 3.11.6, visit [this link](https://www.python.org/downloads/)
- To install PyEnchant, use `pip install pyenchant` in a terminal
- To install Discord, use `pip install discord.py` in a terminal
- To install Requests, use `pip install requests` in a terminal



## How To Run BOTTLE
1. Download the repo code
2. Install the required libraries mentioned above
3. Get a Discord bot token using this [Web Tutorial](https://discordgsm.com/guide/how-to-get-a-discord-bot-token). Save your token and **DO NOT SHARE IT WITH ANYONE**
4. Create a `.env` file in `...\wordle-bot\src\assets\`. Paste "DISCORD_TOKEN=*YOUR BOT TOKEN HERE*" in that file. **AGAIN, DO NOT SHARE THIS TOKEN WITH ANYONE**. 
Below is an example image of how you should setup your `.env` file:
![Example Environment Variable Image](./src/assets/exampleENV.jpg)
5. Add the bot to your server. Tutorial [Linked Here](https://discordjs.guide/preparations/adding-your-bot-to-servers.html#creating-and-using-your-invite-link)
6. Locate and run the code: Find "...\wordle-bot\src\main.py" in the downloaded files. In a terminal, run the command `python /path/to/main.py`. The code should output "Bottle is Running!", and the bot should now be online in your server. To stop running the bot, kill the terminal.
7. To get started with BOTTLE, use `/help` in Discord to see the list of available commands



## How To Configure BOTTLE
Note: Do not edit or remove the `.config` folder. This folder should be hidden and remain unchanged as it contains the default configuration files.

1. Run the bot at least once to generate a `config\` folder.
2. Locate the generated folder in `assets`. The path is `...\wordle-bot\src\assets\config`.
3. Choose the desired file you want to configurate. If you want to configure how rooms are created, then check out `room.cfg`. These files further elaborate their settings.



## Invalid Configuration Files
You can fix any invalid configuration files by deleting them. Re-running the bot should create the missing configuration files.

You can also add the missing sections and/or options. The program will raise an error stating what is missing.

<img src="./src/assets/bottle.png" alt="Bottle Logo" width="160"/>
