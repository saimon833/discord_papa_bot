# bot.py
import asyncio
import json
import os

import discord
import tweepy
from discord.ext import commands, tasks
from discord.ext.commands.core import check
from discord.utils import get
from dotenv import load_dotenv
from tweepy import Stream
from tweepy.streaming import StreamListener

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

data=[]
with open ("settings_skni.json") as file:
    data=json.load(file)
tweet_channel=data["tweet_channel"]
main_channel=data["main_channel"]
test_channel=data["test_channel"]
bot_prefix=data["bot_prefix"]

client = commands.Bot(command_prefix=bot_prefix)

tweet=[]
class TweetListener(StreamListener):
    def on_status(self, status):
        global tweet
        if status.in_reply_to_status_id is None:
            s=status._json
            text=s["text"]
            pp=s["user"]["profile_image_url_https"]
            name='@'+s["user"]["screen_name"]
            link='https://twitter.com/'+s["user"]["screen_name"]+'/status/'+s["id_str"]
            title=s["user"]["screen_name"]+' - Twitter'
            print(s)
            footer=s["created_at"]
            ft=footer.split(' ')
            footer=ft[0]+' '+ft[1]+' '+ft[3]
            TwitterEmbed = discord.Embed(title=title,description=text,url=link, color=0xFF0000)
            TwitterEmbed.set_footer(text=footer)
            TwitterEmbed.set_thumbnail(url=pp)
            TwitterEmbed.set_author(name=name, icon_url=pp)
            tweet.append(TwitterEmbed)
TwitterAuth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
TwitterAuth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
TweetAPI = tweepy.API(TwitterAuth)
NewListener = TweetListener()
NewStream = tweepy.Stream(auth=TweetAPI.auth, listener=NewListener)
NewStream.filter(follow=['1170627202741866497'], is_async=True)

muted=set()

@client.event
async def on_ready():
    papa_mobile.start()
    channel=client.get_channel(test_channel)  #test
    await channel.send('Bot online')
    print('Bot ready')

players={}

def reload_f():
    global tweet_channel
    with open ("settings.json") as file:
        data=json.load(file)
    tweet_channel=data["tweet_channel"]

@client.command(name='reload',
                description="Reloads config",
                pass_context=True)
async def reload(ctx):
    reload_f()
    await ctx.send('Reload complete')

@tasks.loop(seconds=2)
async def papa_mobile():
    global tweet
    try:
        channel=client.get_channel(tweet_channel)
        await channel.send(embed=tweet[0])
        tweet[:]=[]
    except:
        pass
client.run(TOKEN)
