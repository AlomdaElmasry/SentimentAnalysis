from Result import Result
from TwitterAPI import TwitterAPI
from DataCleaner import DataCleaner
from TweetClassifier import TweetClassifier
from sklearn.model_selection import cross_val_score , cross_val_predict
from sklearn.metrics import classification_report , confusion_matrix
import os
try:
    # Python 3.x
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
except ImportError:
    # Python 2.x
    from tkinter import *
    import tkFileDialog

import pandas as pd


class User :

    result = Result()
    api = TwitterAPI()
    datacleaner = DataCleaner()
    tweet_classifier = TweetClassifier()
    tk = Tk()
    email = None
    file = NONE


    def __init__(self):
        return

    def search(self, query):

        auth = self.api.Auth()
        tweets = self.api.retrieve_tweets(query, auth)
        return tweets

    def upload(self ,filename):
     try:
            name = filename
            fname = r'C:\Users\Mohammed\PycharmProjects\new_GP\uploads'
            filename = os.path.join(fname, filename)
            #filename = filedialog.askopenfilename(filetypes=[('excel file', '.xlsx'),('excel file', '.xls'),('excel file', '.csv')])
            if filename:
               if filename.lower().endswith(('.xlsx' , '.xls')):
                   dataframe = pd.read_excel(filename , names=['tweets'])
                   if  len(dataframe.columns)==1:
                       self.api.classify(list(dataframe['tweets']),name)
                       prediction_file = self.api.read_file(name)
                       prediction_file.columns = ['class' ,'tweets']
                       self.file = prediction_file
                   else:
                       return False

               elif filename.lower().endswith(('.csv' )):
                   dataframe = pd.read_csv(filename, names=['tweets'])
                   if len(dataframe.columns)==1:
                       self.api.classify(list(dataframe['tweets']), name)
                       prediction_file = self.api.read_file(name)
                       prediction_file.columns = ['class', 'tweets']
                       self.file = prediction_file
                   else:
                       return False
               else:
                   return False
            else:
                return False

            return True
     except Exception as e:
           return False

    def get_train_file_for_build_algo(self, train_file, algo):

        fname = r'C:\Users\Mohammed\PycharmProjects\new_GP\Classifiers'
        train_filename = os.path.join(fname, train_file)
        dataframe = pd.read_excel(train_filename, names=['tweets', 'class'])

        dataframe.tweets = self.datacleaner.prepare_data_list(list(dataframe.tweets))
        data, label = list(dataframe['tweets']), list(dataframe['class'])
        tfidf = self.tweet_classifier.feature_extraction(data)
        classifier = self.tweet_classifier.build_pickle(tfidf ,label ,algo)

        return classifier

    def get_train_file(self,train_file,algo,NameOfAlgo):

        fname = r'C:\Users\Mohammed\PycharmProjects\new_GP\dev_folder'
        train_filename = os.path.join(fname, train_file)
        dataframe = pd.read_excel(train_filename, names=['tweets', 'class'])

        dataframe.tweets = self.datacleaner.prepare_data_list(list(dataframe.tweets))
        data, label = list(dataframe['tweets']), list(dataframe['class'])
        tfidf = self.tweet_classifier.feature_extraction(data)
        classifier = self.tweet_classifier.learining(tfidf,label,algo,NameOfAlgo)

        return classifier


    def get_test_file(self,test_file):
       try:
            fname = r'C:\Users\Mohammed\PycharmProjects\new_GP\dev_folder'
            test_filename  = os.path.join(fname, test_file)
            dataframe = pd.read_excel(test_filename, names=['tweets', 'class'])
            dataframe.tweets = self.datacleaner.prepare_data_list(list(dataframe.tweets))
            data, label = list(dataframe['tweets']), list(dataframe['class'])
            vectorizer = self.tweet_classifier.fit_data(test_filename)
            tfidf = vectorizer.transform(data)

            return tfidf ,label
       except Exception as e:
           return False


    def accuracy(self,train_file ,test_file,algo,NameOfAlgo):
        try:

            classifier = self.get_train_file(train_file,algo,NameOfAlgo)

            tfidf , label = self.get_test_file(test_file)

            scores = cross_val_score(classifier, tfidf, label)

            label_predict = cross_val_predict(classifier ,tfidf ,label)


            matrix = classification_report(label ,label_predict)


            result = [scores.mean()*100 , matrix]

            return result

        except Exception as e:
            return False





