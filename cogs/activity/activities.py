from dataclasses import dataclass
from enum import Enum
from typing import Optional

import nextcord


@dataclass
class ActivityItem:
    """
    Data object representing a single activity
    """

    key: str
    full_name: str
    id: int


class Activity(Enum):
    """
    Enum for the different types of activities
    """

    # specify type of value for type hints
    value: ActivityItem

    # all activities
    awkword = ActivityItem("awkword", "Awkword", 879863881349087252)
    betrayal = ActivityItem("betrayal", "Betrayal.io", 773336526917861400)
    chess = ActivityItem("chess", "Chess in the Park", 832012774040141894)
    checkers = ActivityItem("checkers", "Checkers in the Park", 832013003968348200)
    fishing = ActivityItem("fishington", "Fishington.io", 814288819477020702)
    letter_tile = ActivityItem("letterleague", "Letter League", 879863686565621790)
    poker = ActivityItem("poker", "Poker Night", 755827207812677713)
    sketch_heads = ActivityItem("sketchheads", "Sketch Heads", 902271654783242291)
    spellcast = ActivityItem("spellcast", "SpellCast", 852509694341283871)
    youtube = ActivityItem("youtube", "Watch Together", 880218394199220334)
    word_snack = ActivityItem("wordsnacks", "Word Snacks", 879863976006127627)

    @classmethod
    def get_activity(cls, key) -> Optional["Activity"]:
        """
        Get an activity by key
        """
        for activity in cls:
            if activity.value.key == key:
                return activity
        return None

    async def create_link(self, channel: nextcord.VoiceChannel) -> nextcord.Invite:
        """
        Create a link to launch the activity
        """
        return await channel.create_invite(
            reason="Launch activity",
            max_age=0,  # number of seconds (0 = never expire)
            max_uses=0,  # number of uses (0 = unlimited)
            target_type=nextcord.InviteTarget.embedded_application,
            target_application_id=self.id,
        )

    @property
    def full_name(self) -> str:
        """
        Get the full name of the activity
        """
        return self.value.full_name

    @property
    def key(self) -> str:
        """
        Get the key of the activity
        """
        return self.value.key

    @property
    def id(self) -> str:
        """
        Get the id of the activity
        """
        return self.value.id
