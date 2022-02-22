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

    await message.channel.send('I am the GRIDBot!')

client.run(os.getenv['TOKEN'])