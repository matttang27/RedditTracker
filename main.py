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
import nest_asyncio
from discord.ext import commands, tasks

from webapp import keep_alive

nest_asyncio.apply()
#constants
SEARCH2 = "https://old.reddit.com/search/.rss?q=subreddit%3AAskReddit&restrict_sr=&sort=new&t=all"
SEARCH = "https://old.reddit.com/search/.rss?q=subreddit%3ADiscord_Bots+flair%3A\"Bot+Request+%5BPaid%5D\"&sort=new&restrict_sr=&t=all"
REPEAT = 10



async def repeater():
  while (True):
    await getFeed()
    asyncio.sleep(10)



latest = ""

async def sendToMatthew(string):
  matthew = await client.get_or_fetch_user(576031405037977600)
  await matthew.send("<@576031405037977600> " + string)


async def getFeed():
    global latest
    RedditFeed = feedparser.parse(SEARCH)
    print(datetime.datetime.now())
    print("Number of RSS posts :", len(RedditFeed.entries))
    if (latest != "" and latest.link != RedditFeed.entries[0].link):
      global client
      print("New post!")
      print(RedditFeed.entries[0].link)
      await sendToMatthew(RedditFeed.entries[0].link)
    
    latest = RedditFeed.entries[0]
    
async def main():
  
  keep_alive()
  client.run(os.environ.get("TOKEN"))
  #asyncio.create_task(repeater())

@tasks.loop(seconds=10)
async def test():
  await getFeed()

test.start()
intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  print("Tracking reddit feed...")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$latest'):
        await message.channel.send(latest.link)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


