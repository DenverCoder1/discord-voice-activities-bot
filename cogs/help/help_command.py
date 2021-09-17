import discord
from discord.ext import commands
from discord.ext.commands.core import Command


class NewHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    COLOUR = discord.Colour.blurple()

    def get_ending_note(self):
        """Returns note to display at the bottom"""
        prefix = self.clean_prefix
        invoked_with = self.invoked_with
        return f"Use {prefix}{invoked_with} [command] for more info on a command."

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        embed = discord.Embed(title="Bot Commands", colour=self.COLOUR)
        embed.set_author(
            name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url
        )
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(
                    self.__command_and_aliases_names(filtered)
                )
                if cog and cog.description:
                    value = f"{cog.description}\n{value}"
                embed.add_field(name=name, value=value)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands", colour=self.COLOUR
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        embed = discord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    def __command_and_aliases_names(self, filtered: list[Command]) -> list[str]:
        prefix = self.clean_prefix
        names_with_aliases = []
        for command in filtered:
            names_with_aliases += [f"`{prefix}{command.name}`"]
            for alias in command.aliases:
                names_with_aliases += [f"`{prefix}{alias}`"]
        return names_with_aliases

    # Use the same function as group help for command help
    send_command_help = send_group_help
