import os
import sys

import logging

from dotenv import set_key
from pathlib import Path
from discord.ext import commands
from config import DISCORD_TOKEN, AVATAR_HASH, PROTECTED_DIRS
from utils import set_avatar, load_all_extensions

# LOGGING
logger = logging.getLogger("RocketRandy.main")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# RESOURCES
avatar_path = Path("resources/avatar.png")
disc_bot_client = commands.Bot(command_prefix='.')


@disc_bot_client.event
async def on_ready():
    # Check avatar
    if AVATAR_HASH != disc_bot_client.user.avatar:
        logger.info(f"Changing my avatar to {avatar_path}.")
        set_key(
            "../.env.compose.bot", "AVATAR_HASH", await utils.set_avatar(disc_bot_client, avatar_path)
        )
    else:
        logger.info(f"No need to change my avatar, handsome as always")

    await load_all_extensions(disc_bot_client)

    logger.info(f"{disc_bot_client.user} has connected to Discord!")


##########

if __name__ == "__main__":
    disc_bot_client.run(DISCORD_TOKEN)
