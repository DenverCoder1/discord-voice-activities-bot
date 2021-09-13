from dataclasses import dataclass
from enum import Enum


@dataclass
class ActivityItem:
    """
    Object representing a single activity
    """
    key: str
    full_name: str


class Activity(Enum):
    """
    Enum for the different types of activities.
    """
    youtube = ActivityItem("youtube", "YouTube Together")
    poker = ActivityItem("poker", "Poker Night")
    chess = ActivityItem("chess", "Chess in the Park")
    betrayal = ActivityItem("betrayal", "Betrayal.io")
    fishing = ActivityItem("fishing", "Fishington.io")

    @classmethod
    def get_activity_by_key(cls, key):
        """
        Get an activity by key.
        """
        for activity in cls:
            if activity.value.key == key:
                return activity
        return None

    @classmethod
    def get_activity_keys(cls):
        """
        Get a list of all activity keys.
        """
        return [activity.value.key for activity in cls]
