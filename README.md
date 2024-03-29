# Discord Voice Activities Bot

[![Discord](https://img.shields.io/discord/819650821314052106?color=7289DA&logo=discord&logoColor=white)](https://discord.gg/fPrdqh3Zfu "Dev Pro Tips Discussion & Support Server")
[![Powered by Nextcord](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Nextcord-0d1620?logo=nextcord)](https://github.com/nextcord/nextcord "Powered by Nextcord Python API Wrapper")

A simple bot for launching Discord's activities in voice channels.

[**Add the bot**](https://discord.com/api/oauth2/authorize?client_id=887066414723260517&permissions=3072&scope=bot%20applications.commands)

![Discord activities demo](https://user-images.githubusercontent.com/20955511/133156951-db1ad975-c3b9-4317-964c-dc965bd3d724.gif)

Once the bot is added, you can launch an activity with `/activity` or `>activity`.

## Commands

Slash command support with `/activity`

![slash command](https://user-images.githubusercontent.com/20955511/133788815-2f67757f-5092-49df-a085-a657a98830b5.png)

## Environment Variables

The following environment variables can be specified in a `.env` file to configure the bot for self-hosting:

-   `DISCORD_TOKEN`: The token for the bot.
-   `GUILD_IDS` (optional): A comma-separated list of guild IDs to activate slash commands in. (This is for testing since global slash commands can take an hour to register.)

## Add the bot

Click [**here**](https://discord.com/api/oauth2/authorize?client_id=887066414723260517&permissions=3072&scope=bot%20applications.commands) to add the bot with the basic permissions.
