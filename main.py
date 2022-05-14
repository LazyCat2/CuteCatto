import random
import string
import db
import disnake
import os
import time

from disnake.ext import commands, tasks
from petpetgif import petpet
from tools import *

if not os.path.exists('tmp/'):
    os.mkdir('tmp')


@tasks.loop(seconds=60)
async def clear_():
    now = time.time()
    for x in os.listdir('tmp/'):
        path = 'tmp/' + x
        if os.stat(path).st_mtime < now - 60:
            os.remove(path)
            print(path, 'removed')


bot = commands.InteractionBot(sync_commands=False)
start_at = round(time.time())
guild = [937021403096551494]

errors = {
    commands.errors.MissingPermissions: 'usr_perm_err',
    commands.errors.NoPrivateMessage: 'dm_cmd'
}

errors_text = {
    'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions':
        'bot_perm_err',
    'Command raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large':
        'too_large'

}


@bot.event
async def on_ready():
    await clear_()
    clear_.start()

    for x in os.listdir('commands/'):
        if not x.endswith('.py'): continue
        x = x[:-3]

        try:
            bot.load_extension(f'commands.{x}')
        except Exception as e:
            exit(-1)
        else:
            print(x, 'is loaded')

    await bot.change_presence(activity=disnake.Game(name='with cats :3'))
    download(bot.user.avatar.url, 'tmp/me.png')
    disnake.Embed.set_default_color(image_color('tmp/me.png'))
    print('Ready')


@commands.has_guild_permissions(manage_messages=True)
@bot.slash_command(description='Чистит сообщения')
async def clear(ctx, amount: int = commands.param(
    name='количество',
    max_value=2500,
    min_value=1
), user: disnake.User = commands.param(
    name='юзер',
    default=None
)):
    amount = int(amount)
    await ctx.send(translate(ctx, 'cls'), ephemeral=True)
    await ctx.channel.purge(limit=amount, check=lambda msg: ((not user) or (msg.author == user)) and not msg.pinned)
    await ctx.edit_original_message(content=translate(ctx, 'done'))


@bot.event
async def on_slash_command_error_(ctx: disnake.MessageCommandInteraction, error):
    print(error, ':', type(error))
    if type(error) == commands.errors.CheckFailure: return
    a = errors.get(type(error)) or errors_text.get(str(error))
    if a:
        a = translate(ctx, a)

    await ctx.send(a or translate(ctx, 'unknown'), ephemeral=True)


@bot.event
async def on_member_join(member):
    return
    with db.User(member.id) as u, db.Data(member.guild.id) as d:
        if d['wlcm_cnl'] and d['wlcm_text'] and d['wlcm_enb']:
            await bot.get_channel(int(d['wlcm_cnl'])). \
                send(
                d['wlcm_text'].replace('@user', member.mention),
                allowed_mentions=disnake.AllowedMentions(
                    everyone=False,
                    users=([member] if u['ping'] else []),
                    roles=[]
                )
            )


@bot.application_command_check()
async def check_commands(ctx):
    if not ctx.guild:
        await ctx.send(translate(ctx, 'dm_cmd'), ephemeral=True)
        return False
    return True


bot.run(open('token.txt').read())
