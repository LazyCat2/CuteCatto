import disnake
from disnake.ext import commands
from __main__ import download, image_color, translate


class Invite(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(description='Показывает инфу об инвайте')
        async def invite(ctx, invite_code: str):
            await ctx.response.defer(ephemeral=True)
            inv = invite_code.split('/')[::-1][0]
            try:
                i = await bot.fetch_invite(inv)
                if not i:
                    print(0 / 0)
            except:
                return await ctx.send(translate(ctx, 'invalid_invite'), ephemeral=True)
            if i.guild.icon:
                download(i.guild.icon.with_format('png').with_size(64).url, f'tmp/{i.guild.id}.png')
                color = image_color(f'tmp/{i.guild.id}.png')
            else:
                color = 0
            emb = disnake.Embed(
                title=i.guild.name,
                description=(i.guild.description or translate(ctx, 'no_descr')) + '\n\n' + f'''
                {translate(ctx, 'inviter')}: {i.inviter or '???'}
                '''.strip(),
                timestamp=i.guild.created_at,
                color=color
            )
            b = i.guild.banner
            ico = i.guild.icon

            emb.set_footer(text='ID: ' + str(i.guild.id))
            if ico: emb.set_thumbnail(ico.url)
            if b: emb.set_image(b.url)

            await ctx.send(embed=emb, ephemeral=True)


def setup(bot): bot.add_cog(Invite(bot))
