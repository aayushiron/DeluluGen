import openai
import json
import re
import random

openai.api_key_path = 'openai_key'

stats = {}
messages = [{'role': 'system', \
             'content': 'You are going to control a game defined by a ' + 
                         'prompt given to you. You will create the player\'s ' +
                         'character a full background and will generate all their stats. ' +
                         'You will add the struct ITEMSTATS: {"Health"\: <health>, ' +
                         '"SP"\: <sp>, "Items"\: []} ' +
                         'at the end of all your messages'}, \
            ]

sentiment_message = [
    {
        'role': 'system', \
        'content': 'You are a sentiment analysis detector that detects if text is angry, sad, happy ' +\
                'or neutral. If the text is angry, you will reply with only \'A\'. If the text is sad, ' +\
                'you will reply with only \'S\'. If the text is neutral, you will reply with only \'N\'.  If the ' +\
                'text is happy, you will reply with only \'H\'.',
    }, 
    {
        'role': 'user', 'content': 'I\'m so pissed!'
    },
    {
        'role': 'assistant', 'content': 'A'
    }
]

happy_emojis = ['q(≧▽≦q)', 'ヾ(≧▽≦*)o', 'ψ(｀∇´)ψ', 'O(∩_∩)O', '(✿◡‿◡)', '(*^_^*)', '(*^▽^*)', '\^o^/', 'o(*^▽^*)┛', '(≧∀≦)ゞ', '( $ _ $ )', '(/≧▽≦)/', 'ヾ(≧ ▽ ≦)ゝ', 'o((>ω< ))o', '(☆▽☆)', '( •̀ ω •́ )y']
angry_emojis = ['╰（‵□′）╯', '(╬▔皿▔)╯', '￣へ￣', '( ˘︹˘ )', '╚(•⌂•)╝', '○|￣|_ =3', '(°ロ°)', '(╯▔皿▔)╯', '(╯‵□′)╯︵┻━┻', 'ಠ╭╮ಠ', '(ㆆ_ㆆ)', 'ಠಿ_ಠ']
sad_emojis = ['/_ \\', '＞﹏＜', '(っ °Д °;)っ', 'ಥ_ಥ', '~~>_<~~', 'X﹏X', '┗( T﹏T )┛', '(；′⌒`)', 'இ௰இ', '<(＿　＿)>', 'X﹏X', '(;´༎ຶД༎ຶ`)', 'o(￣┰￣*)ゞ']
neutral_emojis = ['(^人^)', 'ψ(._. )>', '(⓿_⓿)', '=￣ω￣=', '(✿◕‿◕✿)', '(￣﹃￣)', '(^◕.◕^)', '(ʘᴥʘ)', '(^._.^)ﾉ', '( ͡~ ͜ʖ ͡°)', '( ͡° ͜ʖ ͡°)', '( ͡• ͜ʖ ͡• )', '(ʘ ͜ʖ ʘ)', 'ᓚᘏᗢ', 'ฅʕ•̫͡•ʔฅ', '( ͠° ͟ʖ ͡°)', '(:≡']
confused_emojis = ['¯\_(ツ)_/¯', '¯\_( ͡° ͜ʖ ͡°)_/¯', '＼（〇_ｏ）／', '(´･ω･`)?', '¯\(°_o)/¯', 'ㄟ( ▔, ▔ )ㄏ', '(+_+)?', '╮(╯-╰)╭', '(￣_￣|||)', '┑(￣Д ￣)┍', '◉_◉', '╮(╯▽╰)╭', '(ˉ▽ˉ；)...']

def display_stats():
    # print(stats)
    for stat in stats:
        print(stat + ": " + str(stats[stat]))
        if stat == 'Items':
            for item in stats['Items']:
                print(item)

def process_response(response):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    message_resp = response['choices'][0]['message']['content']
    message_piece = message_resp.split('ITEMSTATS: ')
    if len(message_piece) == 1:
        messages.append({'role': response['choices'][0]['message']['role'], 'content': message_resp})
        mess_copy = messages
        mess_copy.append({'role':'user', 'content': 'give me ITEMSTATS'})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=mess_copy
        )
        message_resp += response['choices'][0]['message']['content']
        # if len(message_resp.split('ITEMSTATS: ')) != 2:
        #     print('-------------------------------------------------')
        #     print(message_resp)
        message_piece.append(message_resp.split('ITEMSTATS: ')[1])

    message, stats_str = message_piece
    search = re.search("{[^{}]*}", stats_str)
    return message.strip(), json.loads(search.group())

def prompt_user(prompt):
    # prompt = input('Please describe the setting of the game you want to play:\n> ')
    messages.append({'role':'user', 'content': 'Prompt: ' + prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        message_resp = response['choices'][0]['message']['content']
        message, stat = process_response(message_resp)
    except:
        return "Error: ChatGPT is being mean 🐄. The prompt might be invalid.", 1
    global stats
    stats = stat
    return message, 0
    # print(message)

def game_loop(prompt):
    # prompt = input('\n> ')
    if prompt == 'stats':
        display_stats()
    else:
        messages.append({'role':'user', 'content': prompt})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )
            message_resp = response['choices'][0]['message']['content']
            message, stat = process_response(message_resp)
        except Exception as e:
            print(e)
            return "Error: ChatGPT is being mean 🐄. Try again in 20s.", 1
        global stats
        stats = stat
        messages.append({'role': response['choices'][0]['message']['role'], 'content': message})
        return message, 0
        # print(message)

def sentiment_emoji(message):
    if message[:5] == 'ERROR':
        return random.choice(sad_emojis)
    sent = sentiment_message + [{'role':'user', 'content': message}]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=sent
        )
        message_resp = response['choices'][0]['message']['content'].strip()
        if (message_resp[0] == 'S'):
            return random.choice(sad_emojis)
        elif (message_resp[0] == 'H'):
            return random.choice(happy_emojis)
        elif (message_resp[0] == 'A'):
            return random.choice(angry_emojis)
        elif (message_resp[0] == 'N'):
            return random.choice(neutral_emojis)
        else:
            return random.choice(confused_emojis)
    except:
        return random.choice(confused_emojis)

# prompt_user()

# while (True):
#     game_loop()


