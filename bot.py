import discord
import os
import json
import globals
import logging
from pathlib import Path
from transformers import AutoModelWithLMHead, AutoModelForCausalLM, AutoTokenizer, GPT2Tokenizer


# the directory of the shared folder
shared_dir = os.path.abspath('../shared/')
settings_file = 'bot_settings.json'

# emoji and mentions files
files = [
    shared_dir + '/emojis.txt',
    shared_dir + '/emojiNames.txt',
    shared_dir + '/mentions.txt',
    shared_dir + '/mentionsNames.txt'
]

# cogs
cogs_ext = [
    'gpt',
    'settings',
    'utilities',
    'sudo'
]

# check if the setting file exists in the directory
if not Path(settings_file).exists():
    print('No bot setting file exists, creating one now')
    bot_settings = {
        'BOT-NAME': '',
        'BOT-NICK': '',
        'BOT-TOKEN': '',
        'BOT-OWNER': 'token'
    }
    # create a new file and fill it with the settings
    with open(settings_file, 'w') as file:
        json.dump(bot_settings, file, indent=4, ensure_ascii=False)
    exit(0)

# load the settings into the bot
with open(settings_file) as file:
    try:
        bot_settings = json.load(file)
        # grab the relevant data from the json object
        BOT_TOKEN = bot_settings['BOT-TOKEN']
        BOT_NAME = bot_settings['BOT-NAME']
        BOT_NICK = bot_settings['BOT-NICK']
        BOT_OWNER = bot_settings['BOT-OWNER']

    except json.decoder.JSONDecodeError:
        content = 'you don\' fucked up now!'
        print('|', content, ' ' * (35 - len(content)), '|')
        print('-' * 40)
        exit(0)


# initialize the global variables
globals.initialize()
logging.basicConfig(level=logging.WARNING)

# load in the emoji and mentions files
emojiData = []
for file in files:
    with open(file) as data:
        try:
            content = data.read().split('\n')
            emojiData.append(content)
        except Exception:
            content = 'you don\' fucked up now!'
            print('|', content, ' ' * (35 - len(content)), '|')
            print('-' * 40)
            exit(0)

# paths
globals.shared_dir = shared_dir

# static variables
globals.bot_name = BOT_NAME
globals.bot_nick = BOT_NICK
globals.bot_owner = BOT_OWNER

# static datasets
globals.emojis = emojiData[0]
globals.emojiNames = emojiData[1]
globals.mentions = emojiData[2]
globals.mentionNames = emojiData[3]

print('-' * 40)
content = f'Loading the GPT2 Model...'
print('|', content, ' ' * (35 - len(content)), '|')
globals.tokenizer = GPT2Tokenizer.from_pretrained(os.path.join(globals.shared_dir, 'DialoGPT-medium'))
globals.model = AutoModelForCausalLM.from_pretrained(os.path.join(globals.shared_dir, 'DialoGPT-medium'))
#globals.model = AutoModelForCausalLM.from_pretrained(f'GPT2-{globals.bot_name}')
content = f'GPT2 model successfully loaded'
print('|', content, ' ' * (35 - len(content)), '|')

print('-' * 40)
content = f'Starting {BOT_NAME}...'
print('|', content, ' ' * (35 - len(content)), '|')
bot = discord.Bot(owner_id=globals.bot_owner, intents=discord.Intents.all(), help_command=None)
print('-' * 40)
content = f"Loading {len(cogs_ext)} extensions:"
print('|', content, ' ' * (35 - len(content)), '|')
# load the cogs aka extensions
for ext in cogs_ext:
    try:
        content = f"   loading cogs.{ext}"
        print('|', content, ' ' * (35 - len(content)), '|')
        bot.load_extension(f'cogs.{ext}')
    except Exception as exc:
        content = f"error loading {ext}"
        print('|', content, ' ' * (35 - len(content)), '|')
        raise exc

bot.run(BOT_TOKEN)
