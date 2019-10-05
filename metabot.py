import asyncio
import discord
import logging
import praw
import time
from discord.ext import commands

bot = commands.Bot()

logging.basicConfig(
    filename="output.log",
    filemode='a',
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO
)

reddit = praw.Reddit(
    client_id="", # Replace with your Reddit app client ID
    client_secret="", # Replace with your Reddit app client secret
    user_agent="" # Replace with descriptive user agent for Reddit
)

subreddit = "fortnitebrmeta"

async def check_for_posts():
    await bot.wait_until_ready()
    bot_started_at = time.time()
    logging.info(f"Logged into Discord as user: {bot.user.name}.")

    cache = []
    for submission in reddit.subreddit(subreddit).new(limit=10):
        cache.append(submission.id)

    try:
        while True:
            for submission in reddit.subreddit(subreddit).new(limit=10):
                if submission.id not in cache:
                    if submission.created > bot_started_at:
                        logging.info(f"{submission.title} was posted by /u/{submission.author.name}")
                        channel = bot.get_channel(00000000000000000) # Replace with Discord channel ID

                        embed = discord.Embed(
                            title=submission.title,
                            url=submission.url,
                            color=discord.Color(0xff460a),
                            description=submission.selftext[0:250]
                        )

                        embed.set_author(name=f"/u/{submission.author.name}", url=f"https://reddit.com/u/{submission.author.name}")
                        embed.set_footer(text="Please don't forget to leave a ✅ react on this message when claiming the post!")

                        if len(embed.description) > 250:
                            embed.description = embed.description + "..."

                    await channel.send(embed=embed)
                    cache.append(submission.id)

            await asyncio.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        logging.error(e)
        time.sleep(30)
        pass


bot.loop.create_task(check_for_posts())
bot.run("") # Discord bot token