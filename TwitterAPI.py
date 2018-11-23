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
    consumer_key = "YzOvqcRjnMmuILUmDD2OCPatM"
    consumer_secret = "lWTZjwzY6X6IIgcIlya1fY1XTF1JuNXxOaHGcyt1ygJrLz8QBw"
    access_token = "777478550572130304-6DDnkvSWZQt9Hyx5MVMI9vBb6GbD6ry"
    access_secret = "m1vuJoc4GDEblpDXoLm0DVD7MgmhFlq5b2HolSRBFurgG"
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


    # def realtime_file(self, tweets):
    #
    #
    #     self.tweets_classifier.put_word_features()
    #     classifier = self.tweets_classifier.load_classifier()
    #
    #     # clean_tweets = self.data_clean.prepare_data_set(tweets)
    #
    #     workbook = xlsxwriter.Workbook(r"C:\Users\Mohammed\Desktop\new.xlsx")
    #     worksheet = workbook.add_worksheet('Sheet1')
    #
    #     for row,tweet in enumerate(tweets):
    #         if tweet != str(tweet):
    #             row+=1
    #         else:
    #             clean_tweet = self.data_clean.prepare_data_list(str(tweet).split())
    #             key = classifier.classify(self.tweets_classifier.extract_features(clean_tweet))
    #             worksheet.write(row, 0, tweet)
    #             worksheet.write(row, 1, key)


        #dataframe = pd.read_excel(r"C:\Users\Mohamed\Desktop\new.xlsx" , names=['tweets', 'class'])


       # return dataframe







    def classify(self,tweets,filename):


        # text = self.data_clean.prepare_data_list(list(text1))
        # classifier = self.tweets_classifier.load_classifier()
        # vectorizer = self.tweets_classifier.put_word_features()
        # tfidf= vectorizer.transform(text)
        # result = classifier.predict(tfidf)
        # print(result)

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

            # text = self.data_clean.prepare_data_list(list(text1))
            # classifier = self.tweets_classifier.load_classifier()
            # vectorizer = self.tweets_classifier.put_word_features()
            # tfidf= vectorizer.transform(text)
            # result = classifier.predict(tfidf)
            # print(result)

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




