import disnake
from disnake.ext import commands
from __main__ import translate


class btn(disnake.ui.Button):
    long = 0
    clicks = {}

    def __init__(self, disabled=False):
        super().__init__(
            emoji='➕', disabled=disabled,
            style=disnake.ButtonStyle.blurple
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        global text
        self.long += 1
        self.clicks[interaction.author] = self.clicks.get(interaction.author, 0) + 1
        text = pns(self.long, self.clicks, interaction)
        await interaction.response.edit_message(content=text, allowed_mentions=disnake.AllowedMentions(users=[]))


class v(disnake.ui.View):
    def __init__(self, ctx, disabled=False):
        super().__init__(timeout=15 if not disabled else 1)

        self.add_item(btn(disabled))
        self.d = disabled
        self.ctx = ctx

    async def on_timeout(self) -> None:
        if self.d: return
        try:
            await self.ctx.edit_original_message(view=None)
        except:
            ...


def pns(sm, c, ctx):
    n = '\n'
    top = ''
    u = []

    text = f'''
    {translate(ctx, 'total')} {sm} {translate(ctx, 'clicks')}
    '''

    if c:
        users = sorted(c, key=lambda z: c[z], reverse=True)
        for x in users:
            t = f'{x.mention}: {c[x]} {translate(ctx, "clicks")}'
            if len(n.join(u) + text + t) + 3 >= 2000:
                break
            u.append(t)

        top = n.join(u)

    return text + '\n\n' + top


class clicker(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(
            description='Кликай :)'
        )
        async def clicker(ctx):
            await ctx.send(pns(0, {}, ctx), view=v(ctx))


def setup(bot): bot.add_cog(clicker(bot))
