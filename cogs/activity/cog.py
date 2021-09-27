from typing import Any, Coroutine, Dict, Optional, Tuple, Union

import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import (spread_to_rows,
                                                   create_button,
                                                   wait_for_component)
from discordTogether import DiscordTogether
from utils.embedder import error_embed

from .activities import Activity


class VoiceActivitiesCog(commands.Cog, name="🔊 Voice Activities"):
    def __init__(self, bot: commands.Bot):
        self.__dt = DiscordTogether(bot)

    async def _launch_response_kwargs(self, ctx: Union[SlashContext, commands.Context], activity: Activity) -> Dict[str, Any]:
        """
        Gets the keyword arguments for the response for passing to a send or edit message function

        Arguments:
            ctx: Command or interaction context
            activity: The activity to launch

        Returns:
            Dictionary containing the send/edit function kwargs
        """
        # check that the channels are accessible
        if not hasattr(ctx.author, "voice"):
            return {
                "embed": error_embed(
                    title="Bot is missing permissions.",
                    description="This bot requires the `View Channels` permission."
                )
            }
        # check that the user is in a voice channel
        if ctx.author.voice is None:
            return {
                "embed": error_embed(
                    title="You are not in a voice channel.",
                    description="Please join a voice channel and try again."
                )
            }
        # here we consider that the user is in a voice channel accessible to the bot
        link = await self.__dt.create_link(ctx.author.voice.channel.id, activity.value.key)
        return {"content": f"Click the blue link to start the activity!\n{link}"}

    async def _send_activity_button_prompt(self, ctx: Union[SlashContext, commands.Context]) -> Tuple[Coroutine[Any, Any, None], Activity]:
        """
        Prompts the user with buttons to select a valid activity

        Args:
            ctx: Interaction or command context

        Returns:
            - Reference to the method for editing the response
            - The chosen activity
        """
        identifier = getattr(
            ctx.message, "id", getattr(ctx, "interaction_id", None)
        )
        buttons = (
            create_button(style=ButtonStyle.primary,
                          custom_id=f"DiscordVoiceActivity::{identifier}::{activity.value.key}",
                          label=activity.value.full_name)
            for activity in Activity
        )
        action_rows = spread_to_rows(*buttons)
        await ctx.send(content="Please select an activity.", components=action_rows)
        button_ctx: ComponentContext = await wait_for_component(ctx.bot, components=action_rows)
        # get activity
        activity = Activity.get_activity(button_ctx.custom_id.split("::")[-1])
        # return the method for updating the message and the activity
        return button_ctx.edit_origin, activity

    async def _start_activity(self, ctx: Union[SlashContext, commands.Context], activity_key: Optional[str]):
        """
        Sends a link to launch and join the activity

        Args:
            ctx: Interaction or command context
            activity_key: key for the activity (eg. `youtube`, `chess`)
                If not specified, or an invalid key is provided, the user
                will be prompted to select an activity with buttons.
        """
        # method to use for sending the link
        sender: Coroutine = ctx.send
        # get the activity by the user-specified key
        activity = Activity.get_activity(activity_key)
        # Send buttons if the user did not specify a valid activity
        if activity is None:
            sender, activity = await self._send_activity_button_prompt(ctx)
        # send response for launching activity
        message_kwargs = await self._launch_response_kwargs(ctx, activity)
        await sender(**{"content": "", "embed": None, "components": None, **message_kwargs})

    @cog_ext.cog_slash(
        name="activity",
        description=("Start a voice channel activity"),
        guild_ids=config.GUILD_IDS,
        options=[
            create_option(
                name="name",
                description="Activity to play",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name=activity.value.full_name,
                                  value=activity.value.key)
                    for activity in Activity
                ],
            ),
        ],
        connector={"name": "activity_key"}
    )
    async def vc_activity_slash(self, ctx: SlashContext, activity_key: Optional[str] = None):
        """Slash command for starting an activity"""
        await self._start_activity(ctx, activity_key)

    @commands.command(aliases=[activity.value.key for activity in Activity])
    async def activity(self, ctx: commands.Context, activity_key: Optional[str] = None):
        """
        Command to start a voice channel activity

        Example usage:
        `>activity` - Select from a list of activities
        `>youtube` - Launch YouTube Together
        `>poker` - Launch Poker Night
        `>chess` - Launch Chess in the Park
        `>betrayal` - Launch Betrayal.io
        `>fishing` - Launch Fishington.io
        `>letter-tile` - Launch Letter Tile
        `>word-snack` - Launch Word Snack
        `>doodle-crew` - Launch Doodle Crew
        """
        # if invoked with an alias, use it as the activity key
        if ctx.invoked_with != ctx.command.name:
            # set the activity key to the alias used
            activity_key = ctx.invoked_with
        await self._start_activity(ctx, activity_key)


def setup(client):
    client.add_cog(VoiceActivitiesCog(client))
