import discord
from zoya.local_settings import TOKEN

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hello'):
        await message.channel.send('hello, I am a bot')


client.run(TOKEN)
