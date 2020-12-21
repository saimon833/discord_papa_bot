import asyncio

import discord
from discord.ext.commands.core import check
from discord.utils import get
from dotenv import load_dotenv


async def check_permission(ctx,ranks):
    user_ranks=[]
    for i in ranks:
        user_ranks.append(discord.utils.get(ctx.guild.roles,name=i))
    for i in user_ranks:
        if i in ctx.author.roles:
            return True
    await ctx.send('Nie masz admina polaku robaku')
    return False  
async def join_papa(id,typ,client):
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
def set_ID(x):
    tmp=''
    for i in range(len(x)-1):
        if x[i]=='!' or x[i]=='<' or x[i]=='>' or x[i]=='@':
            continue
        else:
            tmp+=x[i]
    return int(tmp)
def check_channel(client):
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
