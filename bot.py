import os

import nextcord
from nextcord.ext import commands

import config


def main():
    intents = nextcord.Intents.default()

    activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="/activity")

    bot = commands.Bot(
        config.BOT_PREFIX,
        intents=intents,
        activity=activity,
        rollout_delete_unknown=False,
    )

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
