from typing import Optional

import nextcord

DEFAULT_COLOUR = nextcord.Color.blurple


def __trim(text: str, limit: int) -> str:
    """limit text to a certain number of characters"""
    return text[: limit - 3].strip() + "..." if len(text) > limit else text


def error_embed(title: str, description: Optional[str] = None) -> nextcord.Embed:
    """Embed a message with a title and a red highlight"""
    # create the embed
    return build_embed(title=title, description=description, colour=nextcord.Colour.red())


def build_embed(
    title: str,
    description: Optional[str] = None,
    footer: Optional[str] = None,
    image: Optional[str] = None,
    thumbnail: Optional[str] = None,
    url: Optional[str] = None,
    colour: nextcord.Colour = DEFAULT_COLOUR,
) -> nextcord.Embed:
    """Embed a message and an optional description, footer, and url"""
    # create the embed
    embed = nextcord.Embed(title=__trim(title, 256), url=url, colour=colour)
    if description:
        embed.description = __trim(description, 2048)
    if footer:
        embed.set_footer(text=__trim(footer, 2048))
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed
