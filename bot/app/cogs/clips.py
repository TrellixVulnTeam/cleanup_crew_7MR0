import logging
import time
import os
import json
import random

import discord
from discord.ext import commands

CLIP_CHANNEL = 827932410041729054


class Clips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.group()
    async def clip(self, ctx):
        if ctx.invoked_subcommand is None:
            if os.path.exists('./resources/clips.json'):
                with open('./resources/clips.json') as in_file:
                    cur_clips = json.load(in_file)

                await ctx.send(f'{random.choice(cur_clips["clips"])}')
            else:
                await ctx.send(f"{ctx.author.mention} I don't have any clips to show...")

    @clip.command()
    async def load(self, ctx, limit: int):
        channel = self.bot.get_channel(CLIP_CHANNEL)

        messages = await channel.history(limit=limit).flatten()

        cur_clips = {'clips': []}

        if os.path.exists('./resources/clips.json'):
            with open('./resources/clips.json') as in_file:
                cur_clips = json.load(in_file)

        found_clips = []
        for msg in messages:
            splits = msg.content.split()
            for split in splits:
                if 'gifyourgame.com' in split:
                    found_clips.append(split)

        filtered_list = [clip for clip in found_clips if clip not in cur_clips['clips']]
        final_list = cur_clips['clips'] + filtered_list

        with open('./resources/clips.json', 'w') as out_file:
            json.dump({'clips': final_list}, out_file, indent=4)

        await ctx.send(f'{ctx.author.mention} I have finished loading {limit} message history. I found {len(filtered_list)}')


def setup(bot):
    bot.add_cog(Clips(bot))
