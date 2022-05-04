import logging
import time

import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension_name: str):
        self.logger.info(f"Reloading extension: {extension_name}")
        self.bot.reload_extension(extension_name)
        await ctx.send(
            f"{ctx.author.mention} I have reloaded the {extension_name} extension."
        )

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension_name: str):
        self.logger.info(f'Loading extension: {extension_name}')
        self.bot.load_extension(extension_name)
        await ctx.send(f'{ctx.author.mention} I have loaded the {extension_name} extension')

    @commands.group()
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.author.mention} I'm not sure what to set...")

    @set.command()
    async def status(self, ctx, activity_type: str, *, status):
        self.logger.info(activity_type == 'streaming')
        if activity_type == 'streaming':
            await self.bot.change_presence(activity=discord.Streaming(name=status, url='https://twitch.tv/'))
        elif activity_type == 'listening':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        elif activity_type == 'watching':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        else:
            await self.bot.change_presence(activity=discord.Game(name=status))


def setup(bot):
    bot.add_cog(Admin(bot))
