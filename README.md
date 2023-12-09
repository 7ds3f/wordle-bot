# BOTTLE

A Discord Wordle bot.

Created by EggieVAL, CasterNinja, LucaVits, SoumayahIlias, timcuber37, and 7ds3f.

## How To Create Your Own BOTTLE
- First, open command prompt, and clone the repository via `git clone https://github.com/7ds3f/wordle-bot.git BOTTLE`.

- Next, in command prompt, change the current directory to wherever you saved the repository. For a tutorial, visit [here](https://www.howtogeek.com/659411/how-to-change-directories-in-command-prompt-on-windows-10/)

- Then, install [Python 3.11.6](https://www.python.org/downloads/release/python-3116/) and the required packages via `pip install -r requirements.txt`. You can check out the [Requirements](#requirements) for additional information.

- Now, build a Discord bot and save its token. We will be needing this soon to run the bot. For a tutorial, visit [here](https://discordgsm.com/guide/how-to-get-a-discord-bot-token). A warning from Discord:

```
It should be worth noting that this token is essentially your bot’s password. You should never share this with someone else. In doing so, someone can log in to your bot and do malicious things, such as leaving servers, ban all members inside a server, or pinging everyone maliciously.

The possibilities are endless, so do not share this token.

If you accidentally leaked your token, click the “Regenerate” button as soon as possible. This revokes your old token and re-generates a new one. Now you need to use the new token to login.
```

- Next, invite your Discord bot to a desired server via `https://discord.com/api/oauth2/authorize?client_id=<client_id>&permissions=1084479765584&scope=bot`. Replace `<client_id>` in the provided link with the application id of the bot. This can be found under **General Information** in the Discord Developer Portal.

- Lastly, create a `.env` file in `BOTTLE\src\assets\`, and enter `DISCORD_TOKEN = <your token>`. Obviously, replace `<your token>` with the token you saved previously.

- Now you can run your bot by running the `run.bat` file inside the repository. Or you can run it by manually entering `python src/main.py || python3 src/main.py` in command prompt. To get started with BOTTLE, use `/help` in Discord to see the list of available commands. To stop the bot from running, kill the terminal.

- Note that emojis will not be displayed correctly since your bot does not know they exist. This is something we can't control since that's how Discord bots are designed. For instructions, visit [How To Add Custom Emojis (Unavailable)](#how-to-add-custom-emojis-unavailable). The section says "unavailable," but the section has all the information needed for what we are trying to do.



## Requirements
BOTTLE requires Python 3.11.6. To install Python 3.11.6, visit [this link](https://www.python.org/downloads/release/python-3116/)

BOTTLE requires a few python packages:
- Discord; To install, use `pip install discord.py` in a terminal
- Dotenv; To install, use `pip install python-dotenv` in a terminal
- PyEnchant; To install, use `pip install pyenchant` in a terminal
- Requests; To install. use `pip install requests` in a terminal



## How To Add Custom Emojis (Unavailable)
- First, you need to add the emojis yourself to the server the bot is in. For a tutorial, visit [here](https://support.discord.com/hc/en-us/articles/360036479811-Custom-Emojis#:~:text=To%20upload%20custom%20emojis%2C%20choose,to%20upload%20a%20custom%20emoji.).
- Next, for all the emojis you want BOTTLE to use, you need their IDs. To get their IDs, type `\<emoji>` in Discord, where `<emoji>` is the emoji you want to add. For example, let's say I want to add the *gray letter A* emoji. To display this emoji for everyone to see in Discord, I would type `:gray_letter_a:`. To get the ID of this emoji, I would type `\:gray_letter_a:`. Once entered, copy the ID in the text channel Discord has sent you.
- Then, open File Explorer, locate the repository that contains the bot, and path to the emojis folder: `BOTTLE\src\assets\emojis`. Currently, you cannot add custom emojis. However, you can change the emojis BOTTLE currently uses by changing the emojis in the `square_letters.json` file. To do this, just replace one of the entries with an emoji ID.



## How To Configure BOTTLE
Note: Do not edit or remove the `.config` folder. This folder should be hidden and remain unchanged as it contains the default configuration files.

1. Run the bot at least once to generate a `config\` folder.
2. Locate the generated folder in `assets`. The path is `...\wordle-bot\src\assets\config`.
3. Choose the desired file you want to configurate. If you want to configure how rooms are created, then check out `room.cfg`. These files further elaborate their settings.



## Invalid Configuration Files
You can fix any invalid configuration files by deleting them. Re-running the bot should create the missing configuration files.

You can also add the missing sections and/or options. The program will raise an error stating what is missing.

<img src="./src/assets/bottle.png" alt="Bottle Logo" width="160"/>
