import disnake
from __main__ import start_at, translate

from disnake.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(
            description='Информация о боте'
        )
        async def about(ctx):
            gh = disnake.ui.Button(
                label='GitHub', style=disnake.ButtonStyle.link,
                url='https://github.com/LazyCat2/CuteCatto'
            )
            srv = disnake.ui.Button(
                label=translate(ctx, 'server'),
                style=disnake.ButtonStyle.link,
                url='https://discord.gg/q3wAyDX7db'
            )

            view = disnake.ui.View()
            view.add_item(gh)
            view.add_item(srv)

            await ctx.send(embed=disnake.Embed(
                description=f'''
{translate(ctx, 'started_at')} <t:{start_at}:R>
{translate(ctx, 'ping')}: {round(bot.latency * 1000)} ms
{len(bot.guilds)} {translate(ctx, 'servs')}
{translate(ctx, 'madeby')}: {await bot.fetch_user(850367233582301194)}
'''), view=view)


# [[Github]](https://github.com/Woolbex/catbot)

def setup(bot): bot.add_cog(Stats(bot))
