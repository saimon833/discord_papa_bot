from discord.ext.commands.core import check
from discord.utils import get
from dotenv import load_dotenv

from modules.functions import *


async def play(ctx,client,ranks,main_channel):
    if await check_permission(ctx,ranks)==False:
        return
    ogolny=client.get_channel(main_channel) 
    voice_ch=ctx.author.voice.channel
    await ogolny.send('Kremówka time!')
    await ogolny.send('https://piekarniagrzybki.pl/wp-content/uploads/2017/12/kremowka.jpg')
    await join_papa(voice_ch,'comm',client)

async def leave(ctx,ranks):
    if await check_permission(ctx,ranks)==False:
        return
    await ctx.voice_client.disconnect()

async def seppuku(ctx):
    reason='Popełnił sekkupu. Gloria Victis!'
    await ctx.author.kick(reason=reason)
    tmp=str(ctx.message.author)+' popełnij seppuku'
    await ctx.send(tmp)
    await ctx.send('https://media1.tenor.com/images/6f64764b4b7874465d83de68342347cc/tenor.gif')

async def mute(ctx, person,ranks,muted):
    if await check_permission(ctx,ranks)==False:
        return
    if set_ID(person) in muted:
        await ctx.send("Podany user jest zmutowany lub nie istnieje")
    else:
        muted.add(set_ID(person))

async def unmute(ctx, person,ranks,muted):
    if await check_permission(ctx,ranks)==False:
        return
    try:
        muted.remove(set_ID(person))
    except:
        await ctx.send("Podany user jest odmutowany lub nie istnieje")

async def clear(ctx, amount, client, ranks):
    channel = ctx.message.channel
    if await check_permission(ctx,ranks)==False:
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
