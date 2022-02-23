import discord
import os
from playsound import playsound
import random
from datetime import datetime

client = discord.Client()
rand = random.Random(str(datetime.utcnow()))

@client.event
async def on_ready():
    playsoundrand('grid_bot_ready')
    print('GRIDBot ready!')

@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    if messageHas(msg, 'CODE1'):
        playsoundrand('code_1')
        await message.channel.send('**Code 1 Recieved!**')

    if messageHas(msg, 'CODE2') >= 0:
        playsoundrand('code_2')
        await message.channel.send('**Code 2 Recieved!**')

    if messageHas(msg, 'CODE3') >= 0:
        playsoundrand('code_3')
        await message.channel.send('**Code 3 Recieved!**')

    if messageHas(msg, 'CODE4') >= 0:
        playsoundrand('code_4')
        await message.channel.send('**Code 4 Recieved!**')

    if messageHas(msg, 'CODE5') >= 0:
        playsoundrand('code_5')
        await message.channel.send('**Code 5 Recieved!**')

def messageHas(m, s):
    return m.upper().replace(' ', '').find(s) >= 0


def playsoundrand(folder):
    num_files = len(os.listdir(f'sfx/{folder}'))
    if num_files > 1:
        filename = rand.randrange(1, num_files)
        playsound(f'sfx/{folder}/{filename}.mp3', block=False)
    else:
        playsound(f'sfx/{folder}/1.mp3', block=False)


with open('token.txt') as file:
    TOKEN = str(file.read())
client.run(TOKEN)