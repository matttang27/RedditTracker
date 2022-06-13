import asyncio
import os

import discord
from dotenv import load_dotenv

load_dotenv()

import datetime
import threading
import time
#copy pasted non-blocking timer
from threading import Timer

import feedparser

from webapp import keep_alive

keep_alive()

SEARCH = "https://old.reddit.com/search/.rss?q=subreddit%3AAskReddit&restrict_sr=&sort=new&t=all"
SEARCH2 = "https://old.reddit.com/search/.rss?q=subreddit%3ADiscord_Bots+flair%3A\"Bot+Request+%5BPaid%5D\"&sort=new&restrict_sr=&t=all"
REPEAT = 10

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False



latest = ""

async def sendToMatthew(string):
  matthew = await client.get_or_fetch_user(576031405037977600)
  await matthew.send("<@576031405037977600> " + string)

def getFeed():
    global latest
    RedditFeed = feedparser.parse(SEARCH)
    print(datetime.datetime.now())
    print("Number of RSS posts :", len(RedditFeed.entries))
    if (latest != "" and latest.link != RedditFeed.entries[0].link):
      global client
      print("New post!")
      print(RedditFeed.entries[0].link)
      asyncio.run(sendToMatthew(RedditFeed.entries[0].link))
      
    latest = RedditFeed.entries[0]
    




intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  print("Tracking reddit feed...")
  getFeed()
  rt = RepeatedTimer(REPEAT,getFeed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$latest'):
        await message.channel.send(latest.link)

client.run(os.environ.get("TOKEN"))


