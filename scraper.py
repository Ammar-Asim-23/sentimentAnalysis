import praw
import os
from constants import *
import pandas as pd
from praw.models import MoreComments
import datetime
import time
'''
Please add your own client_id, user_agent and client_secret. You can get those by setting up a reddit Project.
'''
reddit = praw.Reddit(client_id = client_id,
                    client_secret = client_id_secret,
                    user_agent = user_agent)

subreddit = reddit.subreddit("politics")



def get_subreddit_info(subreddit):
    # Display the name of the Subreddit
    print("Display Name:", subreddit.display_name)
 
    # Display the title of the Subreddit
    print("Title:", subreddit.title)
 
    # Display the description of the Subreddit
    print("Description:", subreddit.description)

def getHeadlines(subreddit):
    print("Getting headlines...")
    startTime = time.time()
    # Collecting latest headlines
    headlines = set()
    for submission in reddit.subreddit('politics').new(limit=None):
        headlines.add(submission.title)
    # print(posts_data)
    endTime = time.time()
    elapsedTime = endTime - startTime
    return headlines, elapsedTime



get_subreddit_info(subreddit)
pastWeekPosts, timeTaken = getHeadlines(subreddit)
headlines_df = pd.DataFrame(pastWeekPosts)
print("Done")
print("Time taken: ", timeTaken)
print("Number of Headlines collected: ", len(headlines_df.index))
file = "redditData/headlines.csv"
headlines_df.to_csv(file, index = False, mode='a')

