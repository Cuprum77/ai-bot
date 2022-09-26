import discord
import globals
from discord.commands import SlashCommandGroup
from discord.ext import commands


async def empty_memory():
    globals.last_message = None
    globals.shape_info = []


class settings(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    gpt = SlashCommandGroup(
        'settings',
        'Commands related to modifying the bot behaviour'
    )

    @gpt.command()
    async def temp(self, ctx: discord.ApplicationContext, float_number: float):
        if 2 > float_number > 0:
            globals.temperature = float_number
            if globals.auto_empty:
                await empty_memory()
            response = f'`Temperature` was set to `{globals.temperature}`' if not globals.auto_empty \
                else f'`Temperature` was set to `{globals.temperature}`, and memory was wiped'
            await ctx.respond(response)

    @gpt.command()
    async def k_sample(self, ctx: discord.ApplicationContext, int_number: int):
        if 100 >= int_number >= 0:
            globals.sample_k = int_number
            if globals.auto_empty:
                await empty_memory()
            response = f'`Sample K` was set to `{globals.sample_k}`' if not globals.auto_empty \
                else f'`Sample K` was set to `{globals.sample_k}`, and memory was wiped'
            await ctx.respond(response)

    @gpt.command()
    async def p_sample(self, ctx: discord.ApplicationContext, float_number: float):
        if 1 > float_number > 0:
            globals.sample_p = float_number
            if globals.auto_empty:
                await empty_memory()
            response = f'`Sample P` was set to `{globals.sample_p}`' if not globals.auto_empty \
                else f'`Sample P` was set to `{globals.sample_p}`, and memory was wiped'
            await ctx.respond(response)

    @gpt.command()
    async def ngram(self, ctx: discord.ApplicationContext, int_number: int):
        if 10 < int_number > 0:
            globals.ngram_size = int_number
            if globals.auto_empty:
                await empty_memory()
            response = f'`No Repeat Ngrams` was set to `{globals.ngram_size}`' if not globals.auto_empty \
                else f'`No Repeat Ngrams` was set to `{globals.ngram_size}`, and memory was wiped'
            await ctx.respond(response)

    @gpt.command()
    async def empty(self, ctx: discord.ApplicationContext):
        await empty_memory()
        await ctx.respond(f'`Memory wiped`')

    @gpt.command()
    async def auto_empty(self, ctx: discord.ApplicationContext):
        globals.auto_empty = not globals.auto_empty
        await ctx.respond(f'`Auto-Empty` was set to `{globals.auto_empty}`')

    @gpt.command()
    async def limit(self, ctx: discord.ApplicationContext, int_number: int):
        if 0 <= int_number > 5:
            int_number = 3

        globals.limit = int_number
        if globals.auto_empty:
            await empty_memory()

        response = f'`Memory size` was set to `{globals.limit}`' if not globals.auto_empty \
            else f'`Memory size` was set to `{globals.limit}`, and memory was wiped'
        await ctx.respond(response)


    @gpt.command()
    async def talk(self, ctx: discord.ApplicationContext):
        globals.talk = not globals.talk
        await ctx.respond(f'`Enable` was set to `{globals.talk}`')

    @gpt.command()
    async def schizo(self, ctx: discord.ApplicationContext):
        globals.schizo_bool = not globals.schizo_bool
        await ctx.respond(f'`Schizo Mode` was set to `{globals.schizo_bool}`')

    @gpt.command()
    async def cursed(self, ctx: discord.ApplicationContext):
        globals.uwu_bool = not globals.uwu_bool
        await ctx.respond(f'`Cursed Mode` was set to `{globals.uwu_bool}`')


def setup(bot):
    bot.add_cog(settings(bot))
