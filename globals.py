def initialize():
    # paths
    global shared_dir

    # gpt
    global tokenizer
    global model

    # static values, assigned only on boot
    global bot_name
    global bot_nick
    global bot_owner

    # static datasets
    global emojis
    global emojiNames
    global mentions
    global mentionNames

    # dynamic values
    global last_message
    global shape_info
    global limit
    global temperature
    global sample_k
    global sample_p
    global ngram_size

    # dynamic settings
    global auto_empty
    global talk
    global schizo_bool
    global uwu_bool

    # assign default values to the variables

    # paths
    shared_dir = ''

    # static values defaults
    bot_name = ''
    bot_nick = ''
    bot_owner = 0

    # static dataset defaults
    emojis = []
    emojiNames = []
    mentions = []
    mentionNames = []

    # dynamic value defaults
    last_message = None
    shape_info = []
    limit = 3
    temperature = 1.99
    sample_k = 100
    sample_p = 0.8
    ngram_size = 3

    # dynamic setting defaults
    auto_empty = True
    talk = True
    schizo_bool = False
    uwu_bool = False