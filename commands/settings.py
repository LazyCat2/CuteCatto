from __main__ import translate, db, bot
import disnake
from disnake.ext import commands


def create_view(ctx, screen=None):
    view = disnake.ui.View()

    if screen == 'lang':
        view.add_item(RuBtn())
        view.add_item(EnBtn())

    elif screen == 'wlcm':
        view.add_item(EnbWlcmBtn(ctx))
        view.add_item(WlcmTextBtn(ctx))
        view.add_item(WlcmCnl(ctx))

    view.add_item(Select(ctx, screen))
    return view


def create_embed(ctx, screen=None):
    if screen is None:
        return disnake.utils.MISSING
    if screen == 'lang':
        return disnake.Embed(
            title=translate(ctx, 'stng'),
            description=translate(ctx, 'current') + ' ' + translate(ctx, 'this')
        )
    elif screen == 'wlcm':
        with db.Data(ctx.guild_id) as d:
            try:
                cnl = bot.get_channel(int(d['wlcm_cnl'])).mention
            except Exception as bruh:
                print(bruh)
                cnl = None
            return disnake.Embed(
                title=translate(ctx, 'wlcm'),
                description=(
                    ('👋' if d['wlcm_cnl'] and d['wlcm_text'] and d['wlcm_enb'] else '🚪') + ' | ' +
                    ((cnl + ' | ') if cnl else '') +
                    d['wlcm_text'].split('\n')[0][:50]
                )
            )


async def callback(interaction: disnake.MessageInteraction):
    with db.Data(interaction.guild.id) as d:
        d['lang'] = interaction.component.custom_id
    await interaction.response.edit_message(
        view=create_view(interaction, 'lang'),
        embed=create_embed(interaction, 'lang')
    )


class Select(disnake.ui.Select):
    def __init__(self, ctx, default=None):
        super().__init__(
            placeholder=translate(ctx, 'slct_stng')
        )

        self.add_option(
            label=translate(ctx, 'lang'),
            description=translate(ctx, 'this'),
            emoji=translate(ctx, 'emj'),
            default=default == 'lang',
            value='lang'
        )

        with db.Data(ctx.guild.id) as d:
            self.add_option(
                label=translate(ctx, 'wlcm'),
                description=d['wlcm_text'][:100].replace('\n', ' ') or translate(ctx, 'empty'),
                emoji='👋' if d['wlcm_cnl'] and  d['wlcm_text'] and d['wlcm_enb'] else '🚪',
                default=default == 'wlcm',
                value='wlcm'
            )

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(
            view=create_view(interaction, interaction.values[0]),
            embed=create_embed(interaction, interaction.values[0])
        )


class RuBtn(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            emoji='🇷🇺',
            custom_id='ru',
            style=disnake.ButtonStyle.blurple
        )

    async def callback(self, interaction: disnake.MessageInteraction, /):
        await callback(interaction)


class EnBtn(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            emoji='🇬🇧',
            custom_id='en',
            style=disnake.ButtonStyle.blurple
        )

    async def callback(self, interaction: disnake.MessageInteraction, /):
        await callback(interaction)


class EnbWlcmBtn(disnake.ui.Button):
    def __init__(self, ctx):
        with db.Data(ctx.guild.id) as d:
            super().__init__(
                label=(
                    translate(ctx, 'enb') if not d['wlcm_enb']
                    else translate(ctx, 'dsb')
                ), style=(
                    disnake.ButtonStyle.blurple if d['wlcm_enb']
                    else disnake.ButtonStyle.gray
                )
            )

    async def callback(self, interaction: disnake.MessageInteraction):
        with db.Data(interaction.guild_id) as d:
            d['wlcm_enb'] = not d['wlcm_enb']
        await interaction.response.edit_message(
            view=create_view(interaction, 'wlcm'),
            embed=create_embed(interaction, 'wlcm')
        )


class WlcmTextBtn(disnake.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label=translate(ctx, 'edit_wlcm_text'),
            style=disnake.ButtonStyle.blurple,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(WlcmText(interaction))


class WlcmText(disnake.ui.Modal):
    def __init__(self, ctx):
        with db.Data(ctx.guild_id) as d:
            super(WlcmText, self).__init__(
                title=translate(ctx, 'wlcm_text'),
                components=[
                    disnake.ui.TextInput(
                        label=translate(ctx, 'wlcm_text_hint'),
                        style=disnake.TextInputStyle.paragraph,
                        custom_id='text',
                        value=d['wlcm_text'],
                        max_length=1000
                    )
                ], custom_id='wlcm_text'
            )

    async def callback(self, interaction: disnake.ModalInteraction, /) -> None:
        with db.Data(interaction.guild_id) as d:
            d['wlcm_text'] = interaction.text_values['text'].strip()
        await interaction.response.edit_message(
            view=create_view(interaction, 'wlcm'),
            embed=create_embed(interaction, 'wlcm')
        )

class WlcmCnl(disnake.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label=translate(ctx, 'set_crnt_cnl'),
            style=disnake.ButtonStyle.blurple
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        with db.Data(interaction.guild_id) as d:
            d['wlcm_cnl'] = interaction.channel_id
        await interaction.response.edit_message(
            view=create_view(interaction, 'wlcm'),
            embed=create_embed(interaction, 'wlcm')
        )


class Settings(commands.Cog):
    def __init__(self, bot):
        @commands.has_permissions(administrator=True)
        @bot.slash_command()
        async def settings(ctx):
            await ctx.send(content='_ _', view=create_view(ctx, ''), ephemeral=True)


def setup(bot): bot.add_cog(Settings(bot))
