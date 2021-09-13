from typing import Union

import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from discordTogether import DiscordTogether
from utils.embedder import error_embed

from .activities import Activity


class DiscordTogetherCog(commands.Cog, name="Discord Together"):
    def __init__(self, bot: commands.Bot):
        self.__dt = DiscordTogether(bot)

    async def _start_activity(self, ctx: Union[SlashContext, commands.Context], activity_key: str):
        activity = Activity.get_activity(activity_key)
        # Check that the activity is valid
        if activity is None:
            return await ctx.send(embed=error_embed(
                title="Activity not found.",
                description=(
                    "Please select one of the following activities:\n"
                    f'{", ".join(f"`{activity.value.key}`" for activity in Activity)}'
                )
            ))
        # Check that the user is in a voice channel
        if ctx.author.voice is None:
            return await ctx.send(embed=error_embed(
                title="You are not in a voice channel.",
                description="Please join a voice channel and try again."
            ))
        # Here we consider that the user is in a voice channel accessible to the bot
        link = await self.__dt.create_link(ctx.author.voice.channel.id, activity.value.key)
        await ctx.send(f"Click the blue link!\n{link}")

    @cog_ext.cog_slash(
        name="activity",
        description=("Start a voice channel activity"),
        guild_ids=config.GUILD_IDS,
        options=[
            create_option(
                name="name",
                description="Activity to play",
                option_type=SlashCommandOptionType.STRING,
                required=True,
                choices=[
                    create_choice(name=activity.value.full_name,
                                  value=activity.value.key)
                    for activity in Activity
                ],
            ),
        ],
        connector={"name": "activity_key"}
    )
    async def vc_activity_slash(self, ctx: SlashContext, activity_key: str):
        """Slash command for starting an activity"""
        await self._start_activity(ctx, activity_key)

    @commands.command()
    async def activity(self, ctx: commands.Context, activity_key: str = ""):
        """
        Command to start a voice channel activity

        Example usage:
        ```
        >activity youtube
        >activity poker
        >activity chess
        >activity betrayal
        >activity fishing
        ```
        """
        await self._start_activity(ctx, activity_key)


def setup(client):
    client.add_cog(DiscordTogetherCog(client))
