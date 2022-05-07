from __main__ import *

import disnake.ui

import db


def create_view(ctx):
    view = disnake.ui.View()

    view.add_item(AllowPing(ctx))
    view.add_item(AllowScreenshot(ctx))

    return view


class AllowPing(disnake.ui.Button):
    def __init__(self, ctx):
        with db.User(ctx.author.id) as user:
            super().__init__(
                label=translate(ctx, 'off_ping' if user['ping'] else 'on_ping'),
                style=(
                    disnake.ButtonStyle.blurple if user['ping']
                    else disnake.ButtonStyle.gray
                )
            )

    async def callback(self, interaction: disnake.MessageInteraction):
        with db.User(interaction.author.id) as u:
            u['ping'] = not u['ping']
        await interaction.response.edit_message(view=create_view(interaction))


class AllowScreenshot(disnake.ui.Button):
    def __init__(self, ctx):
        with db.User(ctx.author.id) as user:
            super().__init__(
                label=translate(ctx, 'off_screenshot' if user['screenshot'] else 'on_screenshot'),
                style=(
                    disnake.ButtonStyle.blurple if user['screenshot']
                    else disnake.ButtonStyle.gray
                )
            )

    async def callback(self, interaction: disnake.MessageInteraction):
        with db.User(interaction.author.id) as u:
            u['screenshot'] = not u['screenshot']
        await interaction.response.edit_message(view=create_view(interaction))


class UserSettings(commands.Cog):
    def __init__(self, bot):
        @bot.slash_command(name='user-settings')
        async def user_settings(ctx):
            await ctx.send(content='_ _', view=create_view(ctx), ephemeral=True)


def setup(bot): bot.add_cog(UserSettings(bot))
