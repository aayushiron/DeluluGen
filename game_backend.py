import openai
import json
import re

openai.api_key_path = 'openai_key'

stats = {}
messages = [{'role': 'system', \
             'content': 'You are going to control a game defined by a ' + 
                         'prompt given to you. You will give the player ' +
                         'a full background for their character and their stats. ' +
                         'You will add the struct ITEMSTATS: {"Health"\: <health>, ' +
                         '"SP"\: <sp>, "Items"\: []} ' +
                         'at the end of all your messages'}]

def display_stats():
    # print(stats)
    for stat in stats:
        print(stat + ": " + str(stats[stat]))
        if stat == 'Items':
            for item in stats['Items']:
                print(item)

def process_response(response):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    message_resp = response['choices'][0]['message']['content']
    message_piece = message_resp.split('ITEMSTATS: ')
    if len(message_piece) == 1:
        mess_copy = messages
        mess_copy.append({'role':'user', 'content': 'ITEMSTATS'})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mess_copy
        )
        message_resp += response['choices'][0]['message']['content']
        message_piece.append(message_resp.split('ITEMSTATS: ')[1])

    message, stats_str = message_piece
    search = re.search("{[^{}]*}", stats_str)
    return message.strip(), json.loads(search.group())

def prompt_user():
    prompt = input('Please describe the setting of the game you want to play:\n> ')
    messages.append({'role':'user', 'content': 'Prompt: ' + prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    message_resp = response['choices'][0]['message']['content']
    message, stat = process_response(message_resp)
    global stats
    stats = stat
    messages.append({'role': response['choices'][0]['message']['role'], 'content': message})
    print(message)

def game_loop():
    prompt = input('\n> ')
    if prompt == 'stats':
        display_stats()
    else:
        messages.append({'role':'user', 'content': 'Prompt: ' + prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message_resp = response['choices'][0]['message']['content']
        message, stat = process_response(message_resp)
        global stats
        stats = stat
        messages.append({'role': response['choices'][0]['message']['role'], 'content': message})
        print(message)

prompt_user()

while (True):
    game_loop()