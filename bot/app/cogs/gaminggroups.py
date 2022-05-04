import logging
import time
import json
import random

import discord
from discord.ext import commands, tasks


LOBBY_ID = 929440931319533579
BLUE_TEAM_ID = 882731923548545097
ORANGE_TEAM_ID = 882732027500175370
QUEUE_CHANNEL = 942467874788872222


class GamingGroups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")
        self.current_queues = {}

    @commands.group()
    @commands.guild_only()
    async def queue(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            if ctx.guild.id in self.current_queues and ctx.author.id in self.current_queues[ctx.guild.id]:
                await ctx.send(f'Found your queue.')

    @queue.command()
    @commands.guild_only()
    async def create(self, ctx: commands.Context, size: int = 6):
        if ctx.guild.id not in self.current_queues:
            self.current_queues[ctx.guild.id] = {}

        if ctx.author.id not in self.current_queues[ctx.guild.id]:
            create_time = time.time()
            self.current_queues[ctx.guild.id][ctx.author.id] = {'current': [],
                                                                'wait': [],
                                                                'queue_size': size,
                                                                'created_at': create_time,
                                                                'updated_at': create_time}

            await ctx.send(f'```{json.dumps(self.current_queues, indent=4)}```')
    

def setup(bot: commands.Bot):
    bot.add_cog(GamingGroups(bot))
