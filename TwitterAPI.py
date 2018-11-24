import tweepy
import xlsxwriter
from TweetClassifier import TweetClassifier
from DataCleaner import DataCleaner
import pandas as pd
import os

class TwitterAPI:

    tweets = None
    query = None
    number_of_tweets = None
    date = None
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_secret = ""
    data_clean = DataCleaner()
    tweets_classifier = TweetClassifier()

    def __init__(self):

        return



    def Auth(self):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        api = tweepy.API(auth)
        return api


    # def retrieve_tweets(self , query , api):
    #
    #     tweets = {}
    #     for tweet in tweepy.Cursor(api.search, q=query).items(200):
    #         tweets.update({'{}'.format(tweet.text): None})
    #     return tweets

    def retrieve_tweets(self, query, api):
        tweets = []
        for tweet in tweepy.Cursor(api.search, q=query).items(500):
            if tweet.text not in tweets:
               tweets.append(tweet.text)
        return tweets


   







    def classify(self,tweets,filename):


       

        clean_tweets = self.data_clean.prepare_data_list(list(tweets))
        classifier = self.tweets_classifier.load_classifier()
        vectorizer = self.tweets_classifier.put_word_features()
        tfidf = vectorizer.transform(clean_tweets)
        result = classifier.predict(tfidf)
        data_predicted = []
        for tweet ,label in zip(tweets,result):
            data_predicted.append({'tweets':tweet ,'class':label})
        data_predicted = pd.DataFrame(data_predicted)
        path= os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\historical_files', filename)
        if filename.lower().endswith(('.xlsx', '.xls')):
           data_predicted.to_excel(path,index=False)
        elif filename.lower().endswith(('.csv')):
           data_predicted.to_csv(path ,index=False,encoding='utf-8')

    def classify_real_time(self, tweets, filename):

         

            clean_tweets = self.data_clean.prepare_data_list(list(tweets))
            classifier = self.tweets_classifier.load_classifier()
            vectorizer = self.tweets_classifier.put_word_features()
            tfidf = vectorizer.transform(clean_tweets)
            result = classifier.predict(tfidf)
            data_predicted = []
            for tweet, label in zip(tweets, result):
                data_predicted.append({'tweets': tweet, 'class': label})
            data_predicted = pd.DataFrame(data_predicted)
            path = os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\real_files', filename)
            data_predicted.to_excel(path, index=False)


    def read_real_time(self,filename):
        path = os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\real_files',filename)
        dataframe = pd.read_excel(path, names=['class', 'tweets'])

        return dataframe

    def read_file(self,filename):
        path = os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\historical_files',filename)
        if filename.lower().endswith(('.xlsx', '.xls')):
          dataframe = pd.read_excel(path, names=['class', 'tweets'])
        elif filename.lower().endswith(('.csv')):
            dataframe = pd.read_csv(path ,names=['class' ,'tweets'])

        return dataframe




