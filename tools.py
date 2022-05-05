import os.path, yaml
from __main__ import *

import disnake


def get_lang(id):
    with db.Data(id) as d:
        return d['lang']


def download(url, path):
    if os.path.exists(path): return
    with open(path, 'w'): ...
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)


async def handle_image(ctx, user, image):
    inp = f'tmp/{ctx.id}_undone.png'
    out = f'tmp/{ctx.id}.png'

    if image and user:
        await ctx.send(translate(ctx, 'usr_and_img'))
        return None, inp, out

    if not (image or user):
        await ctx.send(translate(ctx, 'not_usr_or_img'))
        return None, inp, out

    if user:
        download(user.display_avatar.with_format('png').url, inp)
    else:
        await image.save(inp)

    try:
        OriImage = Image.open(inp, mode='r')
    except:
        await ctx.send(translate(ctx, 'format_err'))
        return None, inp, out
    return OriImage, inp, out


def screenshot(user, text, path, lang='en'):
    if len(text) > 250:
        text = text[:250] + '...'

    bg = (54, 57, 63)
    img = Image.new('RGB', ((max(
        len(text),
        len(user.name),
        (len(translate(lang, 'file_only')) if not text else 0)
    ) * 10) + 60 + (45 if user.bot else 0), 60), color=bg)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('font.ttf', 15)
    d.text((50, 32), (text if text else translate(lang, 'file_only')), font=fnt,
           fill=((255, 255, 255) if text else (100, 100, 100)))
    d.text((50, 10), user.name, font=fnt, fill=(255, 255, 255))
    download(user.display_avatar.with_format('png').with_size(32).url, f'tmp/{user.id}a.png')
    avatar = Image.open(f'tmp/{user.id}a.png')
    avatar.thumbnail((32, 32))
    img.paste(avatar, (10, 10), Image.open('mask_circle.jpg'))
    if user.bot:
        d.rectangle((
            len(user.name) * 10 + 43, 10,
            len(user.name + '123') * 10 + 54, 30
        ), fill=(88, 101, 242))
        d.text((len(user.name) * 10 + 50, 10), translate(lang, 'bot'), font=fnt, fill=(255, 255, 255))
    img.save(path)


def image_color(path):
    OriImage = Image.open(path, mode='r')
    boxImage = OriImage.filter(ImageFilter.GaussianBlur(radius=2048))

    color = boxImage.getpixel((0, 0))
    try:
        a = tuple(list(color)[:-1]) if len(list(color)) == 4 else tuple(list(color))
        color = eval('0x%02x%02x%02x' % a)
    except:
        print(tuple(list(color)[:-1]))
        color = 0
    return color


localize = {}


def reload_localization():
    for x in os.listdir('localize'):
        localize[x.split('.')[0]] = yaml.safe_load(open('localize/' + x, encoding='UTF-8'))


def translate(lang, id, **kwargs):
    if (
            isinstance(lang, commands.Context) or
            isinstance(lang, disnake.ApplicationCommandInteraction) or
            isinstance(lang, disnake.MessageInteraction)
    ):
        if lang.guild:
            lang = get_lang(lang.guild.id)
        else:
            lang = 'en'

    if isinstance(lang, disnake.Guild):
        lang = get_lang(lang.id)

    if isinstance(lang, int):
        lang = get_lang(lang)

    result = localize.get(lang, localize['en']).get(id, id)

    for x in kwargs:
        result = result.replace('@' + x, kwargs[x])

    return result


reload_localization()
