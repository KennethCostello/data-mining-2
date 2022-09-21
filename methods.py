import time
import creds
import praw
import pprint as pp
import pandas as pd
import string
import numpy as np
import re
from nltk.corpus import stopwords
stop = set(stopwords.words("english"))

#reddit creds
reddit = praw.Reddit(client_id = creds.client_id,
                        client_secret = creds.client_secret,
                        user_agent = creds.user_agent,
                        username = creds.username,
                        password = creds.password)

def lookAtSubreddit(topic):
    id_list = []
    title_list = []
    comment_list = []
    # direct to subreddit and select top / new / hot
    sub = reddit.subreddit(topic).hot(limit = 15)
    # add id and title lists
    for comment in sub:
        id_list.append(comment.id)
        title_list.append(comment.title)
    # add id and title to dataframe
    df = pd.DataFrame({"ids": id_list, "text": title_list})
    return df

def harvestCommentReplies(id_list = []):
    comment_id = []
    body_list = []
    #go through all ids
    for id in id_list:
        sub = reddit.submission(id = id)
        # add id and body to lists
        for comment in sub.comments:
            comment_id.append(comment.parent_id)
            body_list.append(comment.body)
    # add id and body to dataframe
    df = pd.DataFrame({"ids": comment_id, "text": body_list})
    return df

def cleanText(row):
    sent = []
    # clean text to remove special characters & stopwords
    for term in row.split():
        term = re.sub('[^a-zA-Z]', "", term.lower())
        sent.append(term)
    sent = [word for word in sent if word not in stop]
    return " ".join(sent)
