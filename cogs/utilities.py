import math
import psutil
import platform
import os
import sys
import discord
import globals
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.utils import get


async def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


class utilities(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    gpt = SlashCommandGroup(
        'utilities',
        'Commands related to retrieving bot information'
    )

    @gpt.command()
    async def help(self, ctx: discord.ApplicationContext):
        em = discord.Embed(title='Help')
        em.add_field(name="Commands", value=f'''
The bot uses slash commands only.
So to change the temperature you do
`/settings temp` and fill in the box
that appears with the desired setting

```
SETTINGS

temp       |  usage: temp [float, 0 > x > 2]
k_sample   |  usage: k_sample [integer, 0 > x > 100]
p_sample   |  usage: p_sample [float, 0 > x > 1]
ngram      |  usage: ngram [float, 0 > x > 10]
limit      |  usage: limit [integer, 0 >= x > 5]
talk       |  usage: talk
schizo     |  usage: schizo
cursed     |  usage: cursed
empty      |  usage: empty
auto_empty |  usage: auto_empty    

UTILITIES

owners     |  usage: owners
help       |  usage: help
status     |  usage: status

SUDO

reload     |  usage: reload
restart    |  usage: restart
shutdown   |  usage: shutdown
```

Huggingface article for what `temperature`, `top-p`, `top-k` 
and `ngram` does: https://huggingface.co/blog/how-to-generate

`autoempty` just clears the bots memory inbetween setting changes
    ''', inline=False)

        await ctx.respond(embed=em)

    @gpt.command()
    async def status(self, ctx: discord.ApplicationContext):
        em = discord.Embed(title='Hardware')

        uname = platform.uname()
        sv_mem = psutil.virtual_memory()
        net_io = psutil.net_io_counters()

        em.add_field(name="System status", value=f'''```
SYSTEM INFORMATION

System:  {uname.system}
Release: {uname.release}
Machine: {uname.machine}
Python:  {platform.python_version()}


CPU

Processor:      {uname.processor}
Physical Cores: {psutil.cpu_count(logical=False)}
Total Cores     {psutil.cpu_count(logical=True)}
CPU Usage:      {psutil.cpu_percent()}%
CPU Frequency:  {round(psutil.cpu_freq().current / 1000, 2)} GHz


MEMORY

Total:      {await get_size(sv_mem.total)}
Available:  {await get_size(sv_mem.available)}
Used:       {await get_size(sv_mem.used)}
Percentage: {sv_mem.percent}%
Swap:       {await get_size(psutil.swap_memory().total)}


NETWORKING

Total Bytes Sent:     {await get_size(net_io.bytes_sent)}
Total Bytes Received: {await get_size(net_io.bytes_recv)}
    ```''', inline=False)

        await ctx.respond(embed=em)

    @gpt.command()
    async def settings(self, ctx: discord.ApplicationContext):
        _extra = True

        if (globals.shape_info is None) or (globals.last_message is None):
            _extra = False

        em = discord.Embed(title='Status')
        em.add_field(name="Bot parameters", value=f'''```
BOT PARAMETERS

Temperature: {globals.temperature}
Top-K: {globals.sample_k}
Top-P: {globals.sample_p}
Max repeating ngrams: {globals.ngram_size}
Limit: {globals.limit}

BOT SETTINGS

Talk: {globals.talk}
Schizo: {globals.schizo_bool}
Cursed: {globals.uwu_bool}
Auto-Empty: {globals.auto_empty}
```''', inline=False)

        if _extra:
            em.add_field(name="Bot internal parameters", value=f'''
```Shape library: {globals.shape_info}
Last size: {globals.shape_info[0] if len(globals.shape_info) != None else 0}
```
Context tensor:
```{globals.last_message}```
Decoded:
```{globals.tokenizer.decode(globals.last_message[:, :][0], skip_special_tokens=True)}```
    ''', inline=False)

        await ctx.respond(embed=em)


def setup(bot):
    bot.add_cog(utilities(bot))
