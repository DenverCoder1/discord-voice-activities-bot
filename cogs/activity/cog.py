from typing import Optional
from .launch import start_activity

import config
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from .activities import Activity


class VoiceActivitiesCog(commands.Cog, name="🔊 Voice Activities"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="activity",
        description="Start a voice channel activity",
        guild_ids=config.GUILD_IDS,
    )
    async def vc_activity_slash(
        self,
        interaction: Interaction,
        activity_key: str = SlashOption(
            name="name",
            description="Activity to play",
            required=False,
            choices={activity.full_name: activity.key for activity in Activity},
        ),
    ):
        """Slash command for starting an activity"""
        await start_activity(activity_key, interaction=interaction)

    @commands.command(aliases=[activity.key for activity in Activity])
    async def activity(self, ctx: commands.Context, activity_key: Optional[str] = None):
        """
        Command to start a voice channel activity

        Example usage:
        `>askaway` - Launch Ask Away
        `>awkword` - Launch Awkword
        `>betrayal` - Launch Betrayal.io
        `>blazing8s` - Launch Blazing 8s
        `>bobbleleague` - Launch Bobble League
        `>checkers` - Launch Checkers in the Park
        `>chess` - Launch Chess in the Park
        `>fishington` - Launch Fishington.io
        `>landio` - Launch Land.io
        `>letterleague` - Launch Letter League
        `>poker` - Launch Poker Night
        `>puttparty` - Launch Putt Party
        `>sketchheads` - Launch Sketch Heads
        `>spellcast` - Launch SpellCast
        `>wordsnacks` - Launch Word Snacks
        `>youtube` - Launch Watch Together
        """
        # if invoked with an alias, use it as the activity key
        if ctx.invoked_with != ctx.command.name:
            # set the activity key to the alias used
            activity_key = ctx.invoked_with
        await start_activity(activity_key, ctx=ctx)


def setup(client):
    client.add_cog(VoiceActivitiesCog(client))
