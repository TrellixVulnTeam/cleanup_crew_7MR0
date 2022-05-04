import os
import logging
from pathlib import Path

from discord.ext import commands

from config import PROTECTED_DIRS

logger = logging.getLogger("RocketRandy.main")


async def set_avatar(client: commands.Bot, avatar_path: Path):
    with open(avatar_path, "rb") as avatar_image:
        await client.user.edit(avatar=avatar_image.read())
        return client.user.avatar


async def load_all_extensions(client: commands.Bot):
    for root, dirs, files in os.walk("cogs"):
        if root not in PROTECTED_DIRS:
            for file_name in [file for file in files if file.endswith(".py")]:
                cog_name = Path(file_name).stem
                root = root.replace("\\", ".").replace("/", ".")
                logger.info(f"Loading {root}.{cog_name} extension...")
                client.load_extension(f"{root}.{cog_name}")
