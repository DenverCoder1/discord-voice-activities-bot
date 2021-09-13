import os

from dotenv.main import load_dotenv

load_dotenv()

BOT_PREFIX = "dt!"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Creates an integer ID list from a comma-separated string of IDs
GUILD_IDS = [
    int(gid)
    for gid in os.getenv("GUILD_IDS", "").split(",")
    if gid.isdigit()
] or None
