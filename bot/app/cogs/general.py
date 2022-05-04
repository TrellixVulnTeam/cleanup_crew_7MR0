import logging
import time

import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        await ctx.send(f'{ctx.author.mention} slaps {member.mention} around a bit with a big trout!')

    @commands.command()
    async def embed_test(self, ctx):
        embed_msg = discord.Embed(title='This is a test embed', type='rich', color=0xff0000)
        embed_msg.add_field(name='test_field_1', value='test 1', inline=True)
        embed_msg.add_field(name='test_field_2', value='test 2', inline=True)

        new_embed = discord.Embed(title='HAHA I edited it', type='rich', color=0x0000ff)
        new_embed.add_field(name='edit1', value='EDITED', inline=False)

        msg = await ctx.send(embed=embed_msg)
        time.sleep(5)
        await msg.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(General(bot))
