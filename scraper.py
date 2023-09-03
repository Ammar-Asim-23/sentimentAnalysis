import praw
import os
from constants import *
import pandas as pd
from praw.models import MoreComments
import datetime
import time


reddit = praw.Reddit(client_id = client_id,
                    client_secret = client_id_secret,
                    user_agent = user_agent)

subreddit = reddit.subreddit("onepiece")

def get_subreddit_info(subreddit):
    # Display the name of the Subreddit
    print("Display Name:", subreddit.display_name)
 
    # Display the title of the Subreddit
    print("Title:", subreddit.title)
 
    # Display the description of the Subreddit
    print("Description:", subreddit.description)

def getPosts(subreddit, time_filter, limit):
    print("Getting posts...")
    startTime = time.time()
    posts_data = {"ID" : [], "url" : [], "Title" : [], "Total Comments" : [], "Score" : []}
    # Collecting data from the past week
    for post in subreddit.top(time_filter = time_filter, limit = limit):
        posts_data["ID"].append(post.id)
        posts_data["url"].append(post.url)
        posts_data["Title"].append(post.title)
        posts_data["Total Comments"].append(post.num_comments)
        posts_data["Score"].append(post.score)
    # print(posts_data)
    endTime = time.time()
    elapsedTime = endTime - startTime
    return posts_data, elapsedTime

# Saving the past weeks posts data into a dataframe
# top_posts_df = pd.DataFrame(posts_data)
# top_posts_df.to_csv("Top_This_Week.csv", index=False)

def getComments(posts):
    print("Getting comments...")
    startTime = time.time()
    comments = {"Post ID" : [], "Title" : [], "Date" : [], "Comment" : [], "Length" : []}
    postIDs = posts["ID"]
    for i in range(len(postIDs)):
        submission = reddit.submission(id = postIDs[i])
        for commentInstance in submission.comments[1:]:
            if isinstance(commentInstance, MoreComments):
                continue
            id =  postIDs[i]
            date = datetime.datetime.utcfromtimestamp(submission.created_utc)
            title = submission.title
            comments["Post ID"].append(id)
            comments["Title"].append(title)
            comments["Date"].append(date)
            comments["Comment"].append(commentInstance.body)
            comments["Length"].append(len(commentInstance.body))
    endTime = time.time()
    timeElapsed = endTime - startTime


    return comments, timeElapsed

current_datetime = datetime.date.today()
str_current_datetime = current_datetime.strftime('%m/%d/%Y')

pastWeekPosts, timeTaken = getPosts(subreddit, "month", 100)
posts_df = pd.DataFrame(pastWeekPosts)
print("Done")
print("Time taken: ", timeTaken)
print("Number of Posts collected: ", len(posts_df.index))
file = "server/Data/redditData/post.csv"
posts_df.to_csv(file, index = False)

pastWeekComments, timeTaken = getComments(pastWeekPosts)
comments_df = pd.DataFrame(pastWeekComments)
print("Done")
print("Time taken: ", timeTaken)
print("Number of Comments collected: ", len(comments_df.index))
file = "server/Data/redditData/comment.csv"
comments_df.to_csv(file, index = False)