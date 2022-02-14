from typing import TYPE_CHECKING, List, Optional
import nextcord

if TYPE_CHECKING:
    from .activities import Activity


class ActivityButton(nextcord.ui.Button["ActivityView"]):
    """
    Class representing a button for launching an activity
    """

    def __init__(self, activity: "Activity"):
        self.activity = activity
        super().__init__(label=activity.full_name, style=nextcord.ButtonStyle.primary)

    async def callback(self, interaction: nextcord.Interaction):
        self.view.activity = self.activity
        self.view.stop()


class ActivityView(nextcord.ui.View):
    """
    Class for displaying buttons for launching activities
    """

    def __init__(self, activities: List["Activity"], user: nextcord.User):
        super().__init__(timeout=180)
        self.activity: Optional["Activity"] = None
        self.message: Optional[nextcord.Message] = None
        self._user = user

        for activity in activities:
            self.add_item(ActivityButton(activity))

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self._user == interaction.user

    async def on_timeout(self) -> None:
        if self.message:
            for child in self.children:
                if isinstance(child, nextcord.ui.Button):
                    child.disabled = True
            await self.message.edit(view=self)
