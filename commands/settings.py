from __main__ import translate, db
import disnake
from disnake.ext import commands


def create_embed(ctx):
    return disnake.Embed(
        title=translate(ctx, 'stng'),
        description=translate(ctx, 'current') + ' ' + translate(ctx, 'this'),
        color=disnake.Color.blurple()
    )


async def callback(interaction: disnake.MessageInteraction, id):
    if interaction.author.id != id:
        return await interaction.send(translate(interaction, 'wrong'), ephemeral=True)

    with db.Data(interaction.guild.id) as d:
        d['lang'] = interaction.component.custom_id
    await interaction.response.edit_message(embed=create_embed(interaction))


class RuBtn(disnake.ui.Button):
    def __init__(self, id):
        super().__init__(
            emoji='🇷🇺',
            custom_id='ru',
            style=disnake.ButtonStyle.blurple
        )

        self.id = id

    async def callback(self, interaction: disnake.MessageInteraction, /):
        await callback(interaction, self.id)


class EnBtn(disnake.ui.Button):
    def __init__(self, id):
        super().__init__(
            emoji='🇬🇧',
            custom_id='en',
            style=disnake.ButtonStyle.blurple
        )

        self.id = id

    async def callback(self, interaction: disnake.MessageInteraction, /):
        await callback(interaction, self.id)


class Settings(commands.Cog):
    def __init__(self, bot):
        @commands.has_permissions(administrator=True)
        @bot.slash_command()
        async def settings(ctx):
            view = disnake.ui.View()
            view.add_item(RuBtn(ctx.author.id))
            view.add_item(EnBtn(ctx.author.id))

            await ctx.send(embed=create_embed(ctx), view=view)


def setup(bot): bot.add_cog(Settings(bot))
