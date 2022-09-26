import discord
import globals
import sys
import math
import torch
from unidecode import unidecode
from uwuipy import uwuipy
from discord.ext import commands
from random import randint, random
from transformers import AutoModelWithLMHead, AutoModelForCausalLM, AutoTokenizer, GPT2Tokenizer


# uwuify the message
async def uwuify(message: str, id: int):
    uwu = uwuipy(id)
    message = uwu.uwuify(message)
    return message


# replace the emojis in message with one from the list
async def replace_emoji(message: str):
    index = 0
    message_split = message.split(' ')
    for line in message_split:
        if line in globals.mentionNames:
            message_split[index] = globals.mentions[globals.mentionNames.index(line)]
        elif line in globals.emojiNames:
            message_split[index] = globals.emojis[globals.emojiNames.index(line)]
        index += 1
    return ' '.join(message_split)


class gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # print out information when the bot wakes up
        print('-' * 40)
        content = 'Logged in as:'
        print('|', content, ' ' * (35 - len(content)), '|')
        content = f'   {self.bot.user.name}'
        print('|', content, ' ' * (35 - len(content)), '|')
        content = f'   {self.bot.user.id}'
        print('|', content, ' ' * (35 - len(content)), '|')
        content = f'Owned by:'
        print('|', content, ' ' * (35 - len(content)), '|')
        content = f'   {globals.bot_owner}'
        print('|', content, ' ' * (35 - len(content)), '|')
        print('-' * 40)
        content = 'Active in these guilds:'
        print('|', content, ' ' * (35 - len(content)), '|')
        for guild in self.bot.guilds:
            content = f'   {guild.name}'
            print('|', content, ' ' * (35 - len(content)), '|')
            await guild.me.edit(nick=globals.bot_nick)
        print('-' * 40)

    @commands.Cog.listener()
    async def on_message(self, message):
        # if the user is a bot and schizo mode is not enabled, or if the message starts with the bot prefix, return
        if message.author.bot and not globals.schizo_bool:
            return

        # if we are allowed to talk, talk
        if globals.talk or globals.schizo_bool:
            globals.talk = False

            # ignore the message if it comes from either itself or other bots
            if globals.schizo_bool:
                globals.last_message = None
                globals.shape_info = []

            # form query payload with the content of the message
            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = globals.tokenizer.encode(message.content + globals.tokenizer.eos_token, return_tensors='pt')
            bot_input_ids = torch.cat([globals.last_message, new_user_input_ids], dim=-1) \
                if globals.last_message is not None else new_user_input_ids

            # if we overflow, just wipe memory and do nothing
            if bot_input_ids.shape[1] > 200:
                globals.last_message = None
                globals.shape_info = []
                _talk = True
                return

            # generated a response while limiting the total chat history to 1000 tokens,
            async with message.channel.typing():
                chat_history_ids = globals.model.generate(
                    bot_input_ids, max_length=200,
                    pad_token_id=globals.tokenizer.eos_token_id,
                    no_repeat_ngram_size=globals.ngram_size,
                    do_sample=True,
                    top_k=globals.sample_k,
                    top_p=globals.sample_p,
                    temperature=globals.temperature
                )

                globals.last_message = chat_history_ids
                globals.shape_info.append(chat_history_ids.shape[-1])

                # if we are over the limit, start popping the old unused variables
                if len(globals.shape_info) > globals.limit:
                    yeet = globals.shape_info[0]
                    globals.last_message = globals.last_message[:, yeet:]
                    globals.shape_info.pop(0)
                    globals.shape_info = [x - yeet for x in globals.shape_info]

                # pretty print last ouput tokens from bot
                payload = globals.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                                           skip_special_tokens=True)
                payload = await replace_emoji(payload)

            if globals.uwu_bool:
                # send the model's response to the Discord channel
                msg = unidecode(payload)
                msg = await uwuify(msg, message.id)
                await message.channel.send(msg)
            else:
                # send the model's response to the Discord channel
                await message.channel.send(payload)

            globals.talk = True


def setup(bot):
    bot.add_cog(gpt(bot))
