# bot.py
import asyncio
import re
import os
from discord.ext import commands, tasks
from discord.ext.commands.core import check
from dotenv import load_dotenv
import discord
from discord.utils import get
import datetime

from dotenv import main

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
main_channel=int(os.getenv('main_channel'))
test_channel=int(os.getenv('test_channel'))
censor_yaevin=int(os.getenv('censor_yaevin'))

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    papa_mobile.start()
    print('Bot ready')
    channel=client.get_channel(test_channel)  #test
    await channel.send('Bot online')

players={}

@client.command(pass_context=True)
async def play(ctx):
    if check_permission(ctx)==False:
        await ctx.send('Nie masz admina polaku robaku')
        return
    voice_ch=ctx.author.voice.channel
    await join_papa(voice_ch,'comm')
    
def check_permission(ctx):
    admin=discord.utils.get(ctx.guild.roles,name="Dyrekcja")
    moderator=discord.utils.get(ctx.guild.roles,name="Ordynator")
    if admin in ctx.author.roles or moderator in ctx.author.roles:
        return True
    else:
        return False  

async def join_papa(id,typ):
    if id==0: 
        return
    else:
        channel=0
        if typ=='auto':
            channel=client.get_channel(id)
        elif typ=='comm':
            channel=id
        await channel.connect()
        voice = get(client.voice_clients)
        voice.play(discord.FFmpegPCMAudio('barka.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.5
        await asyncio.sleep(180)
        await voice.disconnect()

def check_channel():
    max_members=0
    choosen_channel_id=0
    voice_channel_list = []
    for guild in client.guilds:
        for channel in guild.voice_channels:
            voice_channel_list.append(channel.id)
    for i in voice_channel_list:
        channel = client.get_channel(i)
        members = channel.voice_states.keys() 
        members_number=0
        for member in members:
            members_number+=1
        if members_number>max_members:
            max_members=members_number
            choosen_channel_id=i
    print(voice_channel_list)
    print('Choosen channel: ',choosen_channel_id)
    print('Members: ',max_members)
    voice_channel_list.clear()
    return choosen_channel_id

@client.command(pass_context=True)
async def leave(ctx):
    if check_permission(ctx)==False:
        await ctx.send('Nie masz admina polaku robaku')
        return
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def jy(ctx):
    if ctx.author.id=='360478472700690432':
        ctx.send('Chiałbyś kurwo')
    else:
        await ctx.send('Jebać <@360478472700690432>')

@client.command(pass_context=True)
async def clear(ctx, amount=1):
    channel = ctx.message.channel
    if check_permission(ctx)==False:
        await ctx.send('Nie masz admina polaku robaku')
        return
    if amount>20:
        await ctx.send('Maks 20 wiadomości')
        return
    if ctx.channel==client.get_channel(526399406564573184):
        await ctx.send('Zygi mnie zajebie')
        return
    messages = []
    async for message in channel.history(limit=amount+1):
        messages.append(message)
    await channel.delete_messages(messages)
    await ctx.send('Messages deleted.')
        
formats=[
    '.png',
    '.jpg',
    '.gif',
    '.jpeg',
]
dzban=[
    'przez zero',
    'przez 0',
    '/0',
    '0^0',
]
@client.event
async def on_message(message):
    if message.author==client.user:
        return
    if message.author.id==360478472700690432 and censor_yaevin==1:
        channel = message.channel   
        messages = []
        async for message in channel.history(limit=1):
            messages.append(message)
        await channel.delete_messages(messages)
        await channel.send('Jewin został ocenzurowany.')
        return
    if '🍔' in message.content.lower():
        await message.channel.send('https://www.youtube.com/watch?v=DoLb0Y_LePg')
    if 'czy można' in message.content.lower():
        for wyraz in dzban:
            if wyraz in message.content.lower():# or message.author.id==256112702496178176:
                await message.channel.send('Nie, dzbanie')
                return
        await message.channel.send('https://pbs.twimg.com/media/EjVTRGAWAAse44V.jpg')
    if message.channel==client.get_channel(main_channel)  and message.author!=client.user:
        for msg in formats:
            if msg in message.content.lower():
                await message.channel.send('https://cdn.discordapp.com/attachments/359753790217388032/776435958836625418/69526674_215214139468161_794023305529129398_n.png')
    if message.content.startswith('$WhoAmI'):
        await message.channel.send(message.author.name)
        await message.channel.send(message.author.id)
    await client.process_commands(message)

@client.command(pass_context=True)
async def jb(ctx):
    await ctx.send('Bloku jest jebanym omnibusem')

@tasks.loop(seconds=2)
async def papa_mobile():
    if datetime.datetime.now().hour==21 and datetime.datetime.now().minute==37:
        channel=client.get_channel(main_channel)  #ogolny
        await channel.send('Kremówka time!')
        await channel.send('https://piekarniagrzybki.pl/wp-content/uploads/2017/12/kremowka.jpg')
        id=check_channel()
        if id==0:
            await asyncio.sleep(180)
        else:
            await join_papa(id,'auto')
        
client.run(TOKEN)