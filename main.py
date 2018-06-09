import discord
import random
import asyncio

# Import config data
from config import prefix, universal_prefix
import config

client = discord.Client()
flute_channel = 0
victim_channel = 0

# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    # Ignore messages from the wrong channels.
    if message.channel.id not in [config.bot_spam, config.flute, config.victim]:
        return
    
    # Give the flute players a tutorial if the Flute Bot gets told so by another bot (or Game Master).
    if message.channel.id == config.bot_spam and message.content == universal_prefix + 'sendtutorial':
        await client.send_message(config.tutorial,flute_channel)
        return
        
    # Stall the messages as long as flute_channel and victim_channel haven't been received from the client yet.
    while flute_channel == 0 or victim_channel == 0:
        print("Stalling a message while the channels yet need to be gathered.")
        await asyncio.sleep(1)
    
    # Copy message from the victim channel to the flute players' channel
    if message.channel == victim_channel:
        if len(message.content) < 1950:
            msg = '<@' + message.author.id + '>\n'
            msg += message.content
            msg_table = [msg]
        else:
            # To prevent the bot from crashing when having to send a message of about 2000 characters.
            msg = '<@' + message.author.id + '>\n'
            msg += message.content[0:1000]
            msg2 = '<@' + message.author.id + '>\n'
            msg2 += message.content[1000:]
            msg_table = [msg,msg2]
        for msg in msg_table:
            await client.send_message(msg,flute_channel)
        return
    
    # Whisper into the victim channel if the command whisper is given.
    if message.channel == flute_channel and message.content.startswith(prefix + 'w'):
        await client.send_message(msg[len(prefix) + 1:],victim_channel)
        return

# Whenever the bot regains its connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel(config.welcome_channel),'Beep boop! I just went online!')
    
    # Do I need to put "await" in front of this?
    flute_channel = client.get_channel(config.flute)
    victim_channel = client.get_channel(config.victim)

client.run(config.TOKEN)
