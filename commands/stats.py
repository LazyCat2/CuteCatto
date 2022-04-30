import disnake
from __main__ import start_at, translate

from disnake.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(
            description='Информация о боте'
        )
        async def about(ctx):
            await ctx.send(embed=disnake.Embed(
                description=f'''
{translate(ctx, 'started_at')} <t:{start_at}:R>
{translate(ctx, 'ping')}: {round(bot.latency * 1000)} ms
{len(bot.guilds)} {translate(ctx, 'servs')}
{translate(ctx, 'madeby')}: {await bot.fetch_user(850367233582301194)}
'''))


# [[Github]](https://github.com/Woolbex/catbot)

def setup(bot): bot.add_cog(Stats(bot))
