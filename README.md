# Discord Voice Activities Bot

[![Discord](https://img.shields.io/discord/819650821314052106?color=7289DA&logo=discord&logoColor=white)](https://discord.gg/fPrdqh3Zfu "Dev Pro Tips Discussion & Support Server")

A simple slash command bot for launching Discord's activities in voice channels.

[**Add the bot**](https://discord.com/api/oauth2/authorize?client_id=887066414723260517&permissions=277025393664&scope=bot%20applications.commands)

![discord-activities-bot](https://user-images.githubusercontent.com/20955511/133156951-db1ad975-c3b9-4317-964c-dc965bd3d724.gif)

Once the bot is added, you can launch an activity with `/activity` or `dt!activity <name>`

This bot makes use of [discord-together](https://github.com/apurv-r/discord-together) by apurv-r.

## List of Activities

The activities you can currently launch are:

* **YouTube Together**
* **Poker Night**
* **Chess in the Park**
* **Betrayal.io**
* **Fishington.io**

## Environment Variables

The following environment variables can be specified in a `.env` file to configure the bot:

* `DISCORD_TOKEN`: The token for the bot.
* `GUILD_IDS` (optional): A comma-separated list of guild IDs to activate slash commands in.

## Add the bot

Click [**here**](https://discord.com/api/oauth2/authorize?client_id=887066414723260517&permissions=277025393664&scope=bot%20applications.commands) to add the bot with the default permissions.