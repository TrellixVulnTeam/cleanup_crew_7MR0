import logging
import time
import json
import gzip
import aiohttp
import aiofiles
import discord

from discord.ext import commands
from pydaisi import Daisi

from .utils.worker import celery_app


class Replays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("RocketRandy.main")

    @commands.command()
    async def process(self, ctx):
        if ctx.message.attachments:
            if len(ctx.message.attachments) > 0:
                attachment_url = ctx.message.attachments[0].url
                async with aiohttp.ClientSession() as session:
                    self.logger.info(f'Getting replay from {attachment_url}.')
                    async with session.get(attachment_url) as response:
                        if response.status == 200:
                            file_name = ctx.message.attachments[0].filename
                            self.logger.info(f'Saving {file_name} to replay volume.')
                            async with aiofiles.open(f'/replays/{file_name}', 'wb') as replay:
                                await replay.write(await response.read())

                # process_result = celery_app.send_task('process_replay', [f'/replays/{file_name}'])
                await ctx.message.delete()
                pending_embed = discord.Embed(title=f'Processing replay for {ctx.author}',
                                              type='rich',
                                              url=attachment_url)
                pending_embed.add_field(name='Current Status', value='Processing')
                pending_embed.set_footer(text='This might take a moment...')

                msg = await ctx.send(embed=pending_embed)

                # DAISI

                daisi = Daisi("Rocket League Replay Analyzer", base_url='https://dev3.daisi.io')

                with open(f'/replays/{file_name}', 'rb') as in_file:
                    result = daisi.process_replay_raw(file_path=in_file.read())
                    blue_team = result._result['outputs'][0]['data']
                    orange_team = result._result['outputs'][1]['data']

                await ctx.send(json.dumps(blue_team))
                await ctx.send(json.dumps(orange_team))

                # while not process_result.ready():
                #     pending_embed.set_field_at(0, name='Current Status', value=process_result.state)
                #     await msg.edit(embed=pending_embed)
                #     time.sleep(1)

                # replay_data = process_result.get()
                # replay_data = json.dumps(gzip.decompress(replay_data).decode('utf-8'))
                # with open('/outputs/sample.json', 'w') as out_sample:
                #     out_sample.write(json.dumps(replay_data, indent=4))

                # players_data = {'0': [], '1': []}
                # for player in replay_data['properties']['PlayerStats']:
                #     player_data = {'name': player['Name'],
                #                    'stats': {
                #                        'Assists': player['Assists'],
                #                        'Saves': player['Saves'],
                #                        'Goals': player['Goals'],
                #                        'Shots': player['Shots'],
                #                        'Score': player['Score']
                #                    }
                #                    }
                #     players_data[str(player['Team'])].append(player_data)
                #
                # recorder_name = replay_data['properties'].get('PlayerName', ctx.author)
                # map_name = replay_data['properties']['MapName']
                # record_date = replay_data['properties']['Date']
                #
                # embed_msg = discord.Embed(title=f'{recorder_name}\'s replay at {map_name}',
                #                           type='rich',
                #                           url=attachment_url)
                #
                # embed_msg.add_field(name='Match Date', value=record_date, inline=False)
                #
                # team_zero_score = replay_data['properties']['Team0Score']
                # embed_msg.add_field(name=f'Team 0', value=f'{team_zero_score}', inline=False)
                #
                # for player in players_data['0']:
                #     stat_output = []
                #     for stat, value in player['stats'].items():
                #         stat_output.append(f'{stat}: {value}')
                #     embed_msg.add_field(name=player['name'],
                #                         value='\n'.join(stat_output),
                #                         inline=True)
                #
                # team_one_score = replay_data['properties']['Team1Score']
                # embed_msg.add_field(name=f'Team 1', value=f'{team_one_score}', inline=False)
                #
                # for player in players_data['1']:
                #     stat_output = []
                #     for stat, value in player['stats'].items():
                #         stat_output.append(f'{stat}: {value}')
                #     embed_msg.add_field(name=player['name'],
                #                         value='\n'.join(stat_output),
                #                         inline=True)
                #
                # embed_msg.set_footer(text='Click title to download replay.')
                #
                # await msg.edit(embed=embed_msg)


def setup(bot):
    bot.add_cog(Replays(bot))
