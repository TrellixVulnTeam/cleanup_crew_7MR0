import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AVATAR_HASH = os.getenv("AVATAR_HASH")

# Protected Directories
PROTECTED_DIRS = ['cogs/configs',
                  'cogs/utils']
