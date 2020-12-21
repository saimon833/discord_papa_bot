# bot.py
import asyncio
import datetime
import json
import os

from discord.ext import commands, tasks
from discord.ext.commands.core import check
from discord.utils import get
from dotenv import load_dotenv

from modules import commands as c
from modules import functions as f

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

@client.command(pass_context=True)
async def reload(ctx):
    if await f.check_permission(ctx,ranks)==False:
        return
    reload_f()
    await ctx.send('Reload complete')

@client.command(pass_context=True)
async def play(ctx):
    await c.play(ctx,client,ranks,main_channel)

@client.command(pass_context=True)
async def leave(ctx):
    await c.leave(ctx,ranks)

@client.command(pass_context=True)
async def seppuku(ctx):
    await c.seppuku(ctx)
@client.command(pass_context=True)
async def clear(ctx, amount=1):
    await c.clear(ctx, amount, client, ranks)
        
@client.command(pass_context=True)
async def mute(ctx, person):
   await c.mute(ctx,person,ranks,muted)

@client.command(pass_context=True)
async def unmute(ctx, person):
    await c.unmute(ctx,person,ranks,muted)

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
        id=f.check_channel(client)
        if id==0:
            await asyncio.sleep(180)
        else:
            await f.join_papa(id,'auto',client)
    elif datetime.datetime.now().hour==19 and datetime.datetime.now().minute==40:
        channel=client.get_channel(main_channel)  #ogolny
        await channel.send('<@&696083933623877734> 21 pamiętajcie o loku dziubdziaczki')
        await asyncio.sleep(300)
client.run(TOKEN)
