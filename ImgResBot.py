import praw
from PIL import Image
import requests
from io import BytesIO
import time

# Made by /u/DiamondxCrafting.

try:
    reddit = praw.Reddit(client_id='', client_secret='',
                         username='', password='',
                         user_agent='')
except Exception as e:
    print("#Login failed.", e)

try:
    open('postid.txt', 'r')
except FileNotFoundError:
    open('postid.txt', 'w')


# Check if the submission id is in the postid list.
def postidcheck(postid):
    postidlist = open('postid.txt', 'r+').read().split('\n')
    for post in postidlist:
        if postid == post:
            return post
            break


# Get the dimensions of the image using the submission link.
def getdimensions(link):
    photo = requests.get(link)
    with Image.open(BytesIO(photo.content)) as img:
        width, height = img.size
        return width, height

# Subreddit list.
sublist = ['spacefans', 'exposurefans', 'mostbeautiful']

while True:
    # Go through each subreddit.
    for sub in sublist:
        subreddit = reddit.subreddit(sub)
        # Go through 100 newest submissions (can be changed to 'None' for the max of 1000).
        for submission in subreddit.new(limit=100):
            # Postidcheck function.
            if submission.id == postidcheck(submission.id):
                continue
            # Check if post is a url and not a self text submission.
            if submission.is_self:
                continue
            # Grabbing image dimensions.
            try:
                width, height = getdimensions(submission.url)
                submission.reply(f'{width}x{height}')
                open('postid.txt', 'a+').write(f'{submission.id}\n')
            except Exception as e:
                print(f'Getting dimensions failed. {e}')
            # Bot cooldown
            time.sleep(600)  # remove this if the bot is allowed to post with no cooldown.
            time.sleep(10)
