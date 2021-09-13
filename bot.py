import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import config


def main():
    intents = discord.Intents.default()

    activity = discord.Activity(
        type=discord.ActivityType.listening, name="/activity"
    )

    bot = commands.Bot(config.BOT_PREFIX, intents=intents, activity=activity)

    # slash commands
    setattr(bot, "slash",
            SlashCommand(bot, override_type=True, sync_commands=True))

    # Get the modules of all cogs whose directory structure is cogs/<module_name>/cog.py
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")

    @bot.event
    async def on_ready():
        """When discord is connected"""
        print(f"{bot.user.name} has connected to Discord!")

    # Run Discord bot
    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
