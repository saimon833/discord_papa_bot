# bot.py
import asyncio
import datetime
import json
import os
import re

from dotenv import load_dotenv, main

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import check
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

data=[]
with open ("settings.json") as file:
    data=json.load(file)
formats=data["formats"]
dzban=data["dzban"]
wolacz=data["wolacz"]
main_channel=data["main_channel"]
test_channel=data["test_channel"]
ranks=data["ranks"]
liga=data["liga"]
bot_prefix=data["bot_prefix"]
bot_IDs=data["bot_ID"]

client = commands.Bot(command_prefix=bot_prefix)

muted=set()
@client.event
async def on_ready():
    papa_mobile.start()
    channel=client.get_channel(test_channel)  #test
    await channel.send('Bot online')
    print('Bot ready')

players={}

async def check_permission(ctx):
    user_ranks=[]
    for i in ranks:
        user_ranks.append(discord.utils.get(ctx.guild.roles,name=i))
    for i in user_ranks:
        if i in ctx.author.roles:
            return True
    await ctx.send('Nie masz admina polaku robaku')
    return False  

def reload_f():
    global bot_prefix
    global formats
    global dzban
    global wolacz
    global ranks
    global liga
    global bot_IDs
    with open ("settings.json") as file:
        data=json.load(file)
    formats=data["formats"]
    dzban=data["dzban"]
    wolacz=data["wolacz"]
    ranks=data["ranks"]
    liga=data["liga"]
    bot_prefix==data["bot_prefix"]
    bot_IDs=data["bot_ID"]

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
        voice.play(discord.FFmpegPCMAudio('barka_wykop.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.5
        await asyncio.sleep(202)
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
        for _ in members:
            members_number+=1
        if members_number>max_members:
            max_members=members_number
            choosen_channel_id=i
    print(voice_channel_list)
    print('Choosen channel: ',choosen_channel_id)
    print('Members: ',max_members)
    voice_channel_list.clear()
    return choosen_channel_id

def set_ID(x):
    tmp=''
    for i in range(len(x)-1):
        if x[i]=='!' or x[i]=='<' or x[i]=='>' or x[i]=='@':
            continue
        else:
            tmp+=x[i]
    return int(tmp)

@client.command(pass_context=True)
async def play(ctx):
    if await check_permission(ctx)==False:
        return
    ogolny=client.get_channel(main_channel) 
    voice_ch=ctx.author.voice.channel
    await ogolny.send('Kremówka time!')
    await ogolny.send('https://piekarniagrzybki.pl/wp-content/uploads/2017/12/kremowka.jpg')
    await join_papa(voice_ch,'comm')

@client.command(pass_context=True)
async def reload(ctx):
    if await check_permission(ctx)==False:
        return
    reload_f()
    await ctx.send('Reload complete')

@client.command(pass_context=True)
async def leave(ctx):
    if await check_permission(ctx)==False:
        return
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def seppuku(ctx):
    reason='Popełnił sekkupu. Gloria Victis!'
    await ctx.author.kick(reason=reason)
    tmp=str(ctx.message.author)+' popełnij seppuku'
    await ctx.send(tmp)
    await ctx.send('https://media1.tenor.com/images/6f64764b4b7874465d83de68342347cc/tenor.gif')

@client.command(pass_context=True)
async def clear(ctx, amount=1):
    channel = ctx.message.channel
    if await check_permission(ctx)==False:
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
        
@client.command(pass_context=True)
async def mute(ctx, person):
    if await check_permission(ctx)==False:
        return
    if set_ID(person) in muted:
        await ctx.send("Podany user jest zmutowany lub nie istnieje")
    else:
        muted.add(set_ID(person))

@client.command(pass_context=True)
async def unmute(ctx, person):
    if await check_permission(ctx)==False:
        return
    try:
        muted.remove(set_ID(person))
    except:
        await ctx.send("Podany user jest odmutowany lub nie istnieje")

@client.event
async def on_message(message):
    if message.author==client.user or message.author.id in bot_IDs:
        return
    if message.author.id in muted:
        await message.delete()
        odpowiedz=str(message.author)+' został ocenzurowany.'
        await message.channel.send(odpowiedz)
        return

    if '🍔' in message.content.lower():
        await message.channel.send('https://www.youtube.com/watch?v=DoLb0Y_LePg')
    if 'czy można' in message.content.lower():
        for wyraz in dzban:
            if wyraz in message.content.lower():# or message.author.id==256112702496178176:
                await message.channel.send('Nie, dzbanie')
                return
        await message.channel.send('https://pbs.twimg.com/media/EjVTRGAWAAse44V.jpg')
    for msg in wolacz:
        if msg in message.content.lower():
            await message.channel.send('Ktoś mnie wołał?')
            break
    if message.channel==client.get_channel(main_channel)  and message.author!=client.user:
        mem='https://cdn.discordapp.com/attachments/359753790217388032/776435958836625418/69526674_215214139468161_794023305529129398_n.png'
        for msg in formats:
            try:
                if msg in message.attachments[0].filename:
                    await message.channel.send(mem)
            except:
                if msg in message.content.lower():
                    await message.channel.send(mem)
    if message.content.startswith('$WhoAmI'):
        await message.channel.send(message.author.name)
        await message.channel.send(message.author.id)
    for msg in liga:
        if msg in message.content.lower():
            await message.channel.send('http://szymonk.bieda.it/uploads/wiedzmin.png')
    if 'chcę się zajebać' in message.content.lower():
        wiadomosc='<@'+str(message.author.id)+'> proszę, masz tu linę ^^'
        await message.channel.send(wiadomosc)
        await message.channel.send('https://palmersafetyus.com/wp-content/uploads/1867-Manila-Rope.jpg')
    await client.process_commands(message)

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
    elif datetime.datetime.now().hour==19 and datetime.datetime.now().minute==40:
        channel=client.get_channel(main_channel)  #ogolny
        await channel.send('<@&696083933623877734> 21 pamiętajcie o loku dziubdziaczki')
        await asyncio.sleep(300)
client.run(TOKEN)
