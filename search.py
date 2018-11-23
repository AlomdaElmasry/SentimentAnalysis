# import tweepy
# import pandas as pd
# import re
# from TwitterAPI import TwitterAPI
# import os
# twitter = TwitterAPI()
#
# def clean(txt):
#     # clean = re.sub(r'(?is)[-_]', " ", str(txt))
#     clean = re.sub(r'(?is)[^أ-ي ❤☻☺]', '', str(txt))
#     clean = re.sub("[إأٱآا]", "ا", clean)
#     clean = re.sub("[إأٱآا]+", 'ا', clean)
#     clean = re.sub("ى", "ي", clean)
#     clean = re.sub("ؤ", "ء", clean)
#     clean = re.sub("ئ", "ء", clean)
#     noise = re.compile(""" ّ    | # Tashdid
#                                 َ    | # Fatha
#                                 ً    | # Tanwin Fath
#                                 ُ    | # Damma
#                                 ٌ    | # Tanwin Damm
#                                 ِ    | # Kasra
#                                 ٍ    | # Tanwin Kasr
#                                 ْ    | # Sukun
#                                 ـ     # Tatwil/Kashida
#                             """, re.VERBOSE)
#     clean = re.sub(noise, '', clean)
#     return clean
#
#
# api = twitter.Auth()
#
# def retrieve_tweets(query, api):
#     tweets = []
#     names = []
#     for tweet in tweepy.Cursor(api.search, q=query).items(500):
#         if clean(tweet.text) not in tweets:
#            tweets.append(clean(tweet.text))
#         names.append(tweet.user.name)
#     return zip(tweets ,names)
#
#
# tweets = retrieve_tweets('هجرة AND مصر' ,api)
# data = []
# for tweet, name in tweets:
#     data.append({'tweets': tweet, 'username': name})
# data = pd.DataFrame(data)
# print(data)
# path = os.path.join(r'C:\Users\Mohammed\Desktop', 'new.xlsx')
# data.to_excel(path)
#
#
# def retrieve_tweets1(query, api):
#     tweets = []
#     names = []
#     for tweet in tweepy.Cursor(api.search, q=query).items(500):
#         tweets.append(tweet.text)
#         names.append(tweet.user.name)
#     return zip(tweets ,names)
#
#
# tweets1 = retrieve_tweets1('هجرة ' ,api)
# data1 = []
# for tweet, name in tweets1:
#     data1.append({'tweets': tweet, 'username': name})
# data1 = pd.DataFrame(data1)
# print(data)
# path1 = os.path.join(r'C:\Users\Mohammed\Desktop', 'new1.xlsx')
# data1.to_excel(path1)

from User import User
import pandas as pd
from sklearn.naive_bayes import MultinomialNB ,BernoulliNB
from sklearn.svm import SVC ,LinearSVC


dataframe ="train_data.xlsx"

user  = User()

classifier = user.get_train_file_for_build_algo(dataframe ,LinearSVC())

print(classifier)