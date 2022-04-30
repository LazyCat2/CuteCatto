import disnake
from disnake.ext import commands
from __main__ import download, image_color, translate


class User(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(name='user', description='Профиль юзера')
        async def userinfo(ctx, user: disnake.User = commands.param(name='юзер')):
            await ctx.response.defer()
            download(user.display_avatar.with_format('png').with_size(64).url, f'tmp/{user.id}.png')
            emb = disnake.Embed(
                title=str(user),
                color=image_color(f'tmp/{user.id}.png'),
                description=f'''
{translate(ctx, 'acc_made')} <t:{round(user.created_at.timestamp())}:R>
{translate(ctx, 'came')} <t:{round(user.joined_at.timestamp())}:R>
'''
            )

            if user.display_avatar:
                emb.set_thumbnail(user.display_avatar.url)
            if user.banner:
                emb.set_image(user.banner.url)

            await ctx.send(embed=emb)


def setup(bot): bot.add_cog(User(bot))
