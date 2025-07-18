#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:47:00 2022

@author: salonibhardwaj

Reddit scraping

"""


import pandas as pd
import numpy as np

# misc
from pprint import pprint
from itertools import chain

# reddit API wrapper
import praw

# sentiment analysis
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

import nltk


# plotting & viz
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='whitegrid', palette='Dark2')

# =============================================================================
# #Reddit API access: 
#     ## Refer here for detailed instructions on usage: https://praw.readthedocs.io/en/stable/
# =============================================================================

reddit_read = praw.Reddit(client_id='8irm8e4_0gHQxjviGmsleA', client_secret='hlQbs_0QN_iLnGBGZl3oPgpuU-8YUA', 
                     user_agent='gender-scrape')
 

posts = []
mr_subreddit = reddit_read.subreddit('MensRights+antifeminists')
for post in mr_subreddit.hot(limit=None):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

print(posts)

posts['title'] = posts['title'].astype('str') 

posts['body'] = posts['body'].astype('str') 

title_list = posts['title'].tolist()  #converting both title and body text to list for nlp processing
body_list = posts['body'].tolist()

text_list = title_list + body_list

text_list = [i for i in text_list if i]  #removing empty strings from the list

#function to calculate polarity of list items

nlp = spacy.load("en_core_web_sm")

nlp.add_pipe('spacytextblob')


def calc_polarity(item):
    pol_score = nlp(item)
    polarity = pol_score._.blob.polarity 
    return polarity

text_pol = []

# running loop over the text list
for t in range(len(text_list)):
    txt = text_list[t]
    score = calc_polarity(txt)
    text_pol.append(score)


df_dict = {'Text from reddit':text_list,'Polarity calculated':text_pol}

polarity_df = pd.DataFrame(df_dict)


posts.to_csv('reddit_data_raw.csv', sep=',', index=False)

#calculating polarity of just the titles

title_pol = []
for tx in range(len(title_list)):
    item = title_list[tx]
    title_score = calc_polarity(item)
    title_pol.append(title_score)
    

title_pol_df = pd.DataFrame()

title_pol_df['Post Titles'] = title_list

title_pol_df['Polarity Score'] = title_pol

title_pol_df['Post Score'] = posts['score']


fig, ax = plt.subplots()
 
plt.scatter(title_pol_df['Polarity Score'], title_pol_df['Post Score'])

ax.set_ylabel('Post Score')
ax.set_xlabel('Title Polarity')
ax.set_title('Title Polarity vs Post Score of Top posts in Mensrights & antifeminist subreddits')
plt.show() 

plt.savefig('Title Polarity_vs_Post Score.jpg')


# =============================================================================
# 
# FOR THE GRADER: As discussed in office hours:: This part of the code is slightly experimental/additional.
# We have tried a few things using the Python NLTK Library. In using spacy, we realised there were some 
# elements of subjectivity that is common with online user communities such as subreddits 
# that were not captured by the polarity score option within spacy. This section presents our results
# from the Sentiment Intensity Analysis funcationality within Nltk sentimentvader
# Reference: 
#    https://realpython.com/python-nltk-sentiment-analysis/
#   https://www.learndatasci.com/tutorials/sentiment-analysis-reddit-headlines-pythons-nltk/
#   
# =============================================================================


headlines = set()  #empty set of the top titles in both subreddits

for submission in reddit_read.subreddit('antifeminists+MensRights').new(limit=None):
    headlines.add(submission.title)
    

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()  #inititialise nltk SIobject
pol_results = []

for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    pol_results.append(pol_score)

pol_results_df = pd.DataFrame(pol_results)
pol_results_df.head()

#Below we set the threshold for labeling a post as positive / negative / neutral, 
# based on the group's discretion the following thresholds were selected

pol_results_df['label'] = 0   #initialises a default value for the column for 'neutral' label

#subsetting based on compound values

pol_results_df.loc[pol_results_df['compound'] > 0.3, 'label'] = 1  # Positive sentiment in title
pol_results_df.loc[pol_results_df['compound'] < -0.1, 'label'] = -1 # Negative sentiment in title
pol_results_df.head()

df2 = pol_results_df[['headline', 'label']]
df2.to_csv('reddit_headlines_labels.csv', mode='a', encoding='utf-8', index=False)

print("Positive posts:\n")
pprint(list(pol_results_df[pol_results_df['label'] == 1].headline)[:5], width=200)

print("\nNegative posts:\n")
pprint(list(pol_results_df[pol_results_df['label'] == -1].headline)[:5], width=200)

print(pol_results_df.label.value_counts())

print(pol_results_df.label.value_counts(normalize=True) * 100)

fig, ax = plt.subplots(figsize=(8, 8))

counts = pol_results_df.label.value_counts(normalize=True) * 100

sns.barplot(x=counts.index, y=counts, ax=ax)

ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")
ax.set_title('%age of posts with sentiment labels')


plt.show()

plt.savefig('Sentiment_dist.png')

