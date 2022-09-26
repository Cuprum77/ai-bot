import discord
import globals
import os
from discord.commands import SlashCommandGroup
from discord.ext import commands


class sudo(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    gpt = SlashCommandGroup(
        'sudo',
        'Commands related to the control of the bot application',
        checks=[commands.is_owner().predicate]
    )

    @gpt.command()
    async def restart(self, ctx: discord.ApplicationContext):
        await ctx.respond("Restarting my brain...")
        try:
            await self.bot.close()
        except Exception as exp:
            print(exp)
            await self.bot.close()
            exit(0)
        finally:
            os.system(f"python3 bot.py")

    @gpt.command()
    async def reload(self, ctx: discord.ApplicationContext):
        extensions = list(self.bot.extensions.keys())
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
                content = f"Reloaded {extension}"
                print('|', content, ' ' * (35 - len(content)), '|')
            except Exception as exc:
                raise exc
        await ctx.respond(f"Brain has been reloaded.")
        print('-' * 40)

    @gpt.command()
    async def shutdown(self, ctx: discord.ApplicationContext):
        await ctx.respond("Shutting down my brain...")
        await self.bot.close()
        exit(0)


def setup(bot):
    bot.add_cog(sudo(bot))
