import os
import tweepy
from dotenv import load_dotenv

load_dotenv()
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# authorization of consumer key and consumer secret 
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET) 
  
# set access to user's access key and access secret  
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET) 
  
# calling the api  
api = tweepy.API(auth) 
  
# the screen name of the user 
screen_name = "TechLinkedYT"
screen_name = "saimon1345"
  
# fetching the user 
user = api.get_user(screen_name) 
  
# fetching the ID 
ID = user.id_str 
  
print("The ID of the user is : " + ID) 