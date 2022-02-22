import discord
import os
from playsound import playsound
import random
from datetime import datetime

client = discord.Client()
rand = random.Random(str(datetime.utcnow()))

@client.event
async def on_ready():
    play_random_sound('grid_bot_ready')
    print('GRIDBot ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    await message.channel.send('Hello! I am the GRIDBot!')


def play_random_sound(folder):
    num_files = len(os.listdir(f'sfx/{folder}'))
    if num_files != 1:
        filename = rand.randrange(1, num_files)
        playsound(f'sfx/{folder}/{filename}.mp3', block=False)
    else:
        playsound(f'sfx/{folder}/1.mp3', block=False)


with open('token.txt') as file:
    TOKEN = str(file.read())
client.run(TOKEN)