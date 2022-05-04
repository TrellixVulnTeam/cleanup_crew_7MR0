import logging
import time

import discord
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.command()
    async def join(self, ctx, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        volume = 100 if volume > 100 else volume

        self.logger.info(ctx.voice_client.source)

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")


def setup(bot):
    bot.add_cog(Voice(bot))
