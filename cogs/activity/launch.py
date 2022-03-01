import sys
import traceback
from typing import Any, Callable, Coroutine, Dict, Optional

import nextcord
from nextcord import Interaction, User
from nextcord.ext import commands
from utils.embedder import error_embed

from .activities import Activity
from .activity_view import ActivityView


async def _launch_response_kwargs(user: User, activity: Activity) -> Dict[str, Any]:
    """
    Gets the keyword arguments for the response for passing to a send or edit message function

    Arguments:
        user: User to create the link for
        activity: The activity to launch

    Returns:
        Dictionary containing the send/edit function kwargs
    """
    # check that the channels are accessible
    if not hasattr(user, "voice"):
        return {
            "embed": error_embed(
                title="Bot is missing permissions.",
                description="This bot requires the `View Channels` permission.",
            )
        }
    # check that the user is in a voice channel
    if user.voice is None:
        return {
            "embed": error_embed(
                title="You are not in a voice channel.",
                description="Please join a voice channel and try again.",
            )
        }
    # create link
    try:
        invite = await activity.create_link(user.voice.channel)
    except nextcord.errors.Forbidden:
        print(traceback.print_exc(), file=sys.stderr)
        return {
            "embed": error_embed(
                title="Bot is missing permissions.",
                description="This bot requires permission to create invites.",
            )
        }
    except nextcord.errors.HTTPException:
        print(traceback.print_exc(), file=sys.stderr)
        return {
            "embed": error_embed(
                title="Failed to create an invite for that activity.",
                description=f"Please try a different activity.",
            )
        }
    # send link
    return {"content": f"Click the blue link to start the activity!\n{invite.url}"}


async def _send_activity_button_prompt(
    user: User, sender: Callable[..., Coroutine]
) -> ActivityView:
    """
    Prompts the user with buttons to select a valid activity

    Args:
        user: User who can interact with the buttons
        sender: Function to send the buttons (eg. `ctx.send` or `interaction.send`)

    Returns:
        - Reference to the method for editing the response
        - The chosen activity
    """
    view = ActivityView(activities=list(Activity), user=user)
    view.message = await sender(content="Please select an activity.", view=view)
    await view.wait()
    return view


async def start_activity(
    activity_key: Optional[str],
    *,
    ctx: Optional[commands.Context] = None,
    interaction: Optional[Interaction] = None,
):
    """
    Sends a link to launch and join the activity

    Args:
        activity_key: key for the activity (eg. `youtube`, `chess`)
            If not specified, or an invalid key is provided, the user
            will be prompted to select an activity with buttons.
        ctx: Command context if applicable
        interaction: Interaction if applicable
    """
    message_kwargs = {"content": ""}
    # method to use for sending the link
    sender = ctx.send if ctx else interaction.send
    # user for creating the activity
    user = ctx.author if ctx else interaction.user
    # get the activity by the user-specified key
    activity = Activity.get_activity(activity_key)
    # Send buttons if the user did not specify a valid activity
    if activity is None:
        view = await _send_activity_button_prompt(user, sender)
        if not view.activity:
            return
        activity = view.activity
        # set function for editing the message
        sender = (
            view.message.edit if view.message else interaction.edit_original_message
        )
        # remove view when editing the message
        view.clear_items()
        message_kwargs["view"] = view
    # send response for launching activity
    message_kwargs |= await _launch_response_kwargs(user, activity)
    await sender(**message_kwargs)
