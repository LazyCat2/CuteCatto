from __main__ import *


class ImageCommands(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(description='Погладить кого-то')
        async def pet(ctx,
                      user: disnake.User = commands.param(name='юзер', default=None),
                      image: disnake.Attachment = commands.param(name='картинка', default=None),
                      ):
            await ctx.response.defer()
            _, inp, out = await handle_image(ctx, user, image)

            if not _: return

            petpet.make(inp, out)
            await ctx.send(file=disnake.File(out, 'pet.gif'))

        @bot.slash_command(name='screenshot', description='Отправляет скрин сообщения')
        async def scrsht(
                ctx, user: disnake.User = commands.param(name='юзер'),
                text: str = commands.param(name='текст')
        ):
            await ctx.response.defer()
            screenshot(user, text, f'tmp/{user.id}b.png')
            await ctx.send(file=disnake.File(f'tmp/{user.id}b.png', 'screenshot.png'))

        @bot.slash_command(description='Делает демотиватор')
        async def demotivator(
                ctx,
                user: disnake.User = commands.param(name='юзер', default=None),
                image: disnake.Attachment = commands.param(name='картинка', default=None),
                text1=commands.param(name='текст1'),
                text2=commands.param(name='текст2', default='')
        ):
            await ctx.response.defer()
            _, inp, out = await handle_image(ctx, user, image)

            if not _: return

            a = Demotivator(text1, text2)
            a.create(inp, use_url=False, font_name='font.ttf',
                     result_filename=out)

            await ctx.send(file=disnake.File(out, out))

        @bot.slash_command(description='Блюрит картинку')
        async def blur(ctx, user: disnake.User = commands.param(
            name='юзер',
            default=None
        ),
                       image: disnake.Attachment = commands.param(
                           name='картинка',
                           default=None
                       ),
                       power: int = commands.param(
                           min_value=1,
                           max_value=250,
                           name='интенсивность'
                       )):
            await ctx.response.defer()
            OriImage, inp, out = await handle_image(ctx, user, image)
            if not OriImage: return

            boxImage = OriImage.filter(ImageFilter.GaussianBlur(radius=power))
            boxImage.save(out)

            await ctx.send(file=disnake.File(out, 'blur.png'))


def setup(bot): bot.add_cog(ImageCommands(bot))