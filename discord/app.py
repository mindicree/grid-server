import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('GRIDBot ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello! I am the GRIDBot!')

with open('token.txt') as file:
    TOKEN = str(file.read())
client.run(TOKEN)