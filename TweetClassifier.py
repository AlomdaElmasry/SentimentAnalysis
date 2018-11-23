
from os.path import join, dirname, realpath
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os

import pickle
from DataCleaner import DataCleaner

class TweetClassifier:

    final_file = None
    word_features = None
    data_clean =DataCleaner()

    def __init__(self):

        return

    # def classify_real_time_tweets(self, tweet):
    #
    #     tweeter_api = TwitterAPI()
    #
    #
    #
    #     return


    def get_tweets(self,file_name):
        # file = open_workbook(file_name)
        #Text = []
        # Polarity = []
        # for sheet in file.sheets():
        #     if sheet.name == "Sheet1":
        #         for row in range(sheet.nrows):
        #             for col in range(sheet.ncols):
        #                 data = sheet.cell(row,col).value
        #                 if(col == 0):
        #                     Text.append(data)
        #                 elif(col == 1):
        #                     Polarity.append(data)
        #
        # dic = dict(zip(Text,Polarity))
        dataframe = pd.read_excel(file_name)
        Text = list(dataframe['tweets'])
        #Polarity = list(dataframe['class'])
        #dic = dict(zip(Text, Polarity))
        return Text






    #
    # def get_words(self,tweets):
    #     all_words = []
    #     for (word ,sentiment)in tweets:
    #       all_words.extend(word)
    #
    #     return all_words

    # def get_word_freq(self, wordlist):
    #     wordlist =nltk.FreqDist(wordlist)
    #     word_features = wordlist.keys()
    #     return word_features



    # def extract_features(self,document):
    #     document_word = set(document)
    #     features = {}
    #     for word in self.word_features:
    #         features['Word(%s)' %word]= (word in document_word)
    #     return features

    # training_set = nltk.classify.apply_features(extract_features ,train_data)
    # #test_set = nltk.classify.apply_features(extract_features ,test_data)
    # tel_classifier = nltk.NaiveBayesClassifier.train(training_set)
    #
    #
    def save_classifier(self,classifier):
         UPLOADS_PATH = join(dirname(realpath(__file__)), 'Classifiers/tel_classifier2.pickle')
         f = open(UPLOADS_PATH,'wb')
         pickle.dump(classifier ,f ,-1)
         f.close()

    def save_classifier_dev(self,classifier ,NameOfAlgo):
         UPLOADS_PATH = join(dirname(realpath(__file__)), 'dev_folder/'+NameOfAlgo+'.pickle')
         f = open(UPLOADS_PATH,'wb')
         pickle.dump(classifier ,f ,-1)
         f.close()

    def load_classifier_dev(self,NameOfAlgo):
        UPLOADS_PATH = join(dirname(realpath(__file__)), 'dev_folder/'+NameOfAlgo+'.pickle')
        f = open(UPLOADS_PATH, 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier

    def load_classifier( self ):
        UPLOADS_PATH = join(dirname(realpath(__file__)), 'Classifiers/tel_classifier2.pickle')
        f = open(UPLOADS_PATH, 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier



    # def put_word_features(self):
    #
    #     training = self.get_tweets(r'C:\Users\Mohammed\Desktop\train_data.xlsx')
    #     train_data = self.data_clean.prepare_data_set(training)
    #     self.word_features = self.get_word_freq(self.get_words(train_data))

    def feature_extraction(self , data):
        vectorizer = TfidfVectorizer(min_df=3, max_df=0.85, ngram_range=(1, 3))
        tfidf_data = vectorizer.fit_transform(data)
        return tfidf_data



    # def data_transform(self,data):
    #
    #     vectorizer = TfidfVectorizer(min_df=3, max_df=0.85, ngram_range=(1, 3))
    #     tfidf_data = vectorizer.transform(data)
    #     return tfidf_data

    def fit_data(self,filename):
        vectorizer = TfidfVectorizer(min_df=3, max_df=0.85, ngram_range=(1, 3))
        training = self.get_tweets(filename)
        train_data = self.data_clean.prepare_data_list(training)
        vectorizer.fit_transform(train_data)
        return vectorizer


    def build_pickle(self,train, train_label , algo):
        x_train, y_train = train, train_label
        classifier = algo
        classifier.fit(x_train, y_train)
        # classifier = twitterCal.load_classifier()
        self.save_classifier(classifier)
        # predict = cross_val_predict(classifier,x_test,y_test,cv=10)
        # scores = cross_val_score(classifier ,x_test , y_test,cv=10)
        # print(scores)
        # print('Accuracy of %s %0.2f (+/- %0.2f)'%( classifier ,scores.mean(),scores.std()*2))
        # print(classification_report(y_test ,predict))

        return classifier






    def learining(self,train, train_label , algo,NameOfAlgo):
        x_train, y_train = train, train_label
        classifier = algo
        classifier.fit(x_train, y_train)
        # classifier = twitterCal.load_classifier()
        self.save_classifier_dev(classifier,NameOfAlgo)
        # predict = cross_val_predict(classifier,x_test,y_test,cv=10)
        # scores = cross_val_score(classifier ,x_test , y_test,cv=10)
        # print(scores)
        # print('Accuracy of %s %0.2f (+/- %0.2f)'%( classifier ,scores.mean(),scores.std()*2))
        # print(classification_report(y_test ,predict))

        return classifier



    def put_word_features(self):
        vectorizer = TfidfVectorizer(min_df=3, max_df=0.85, ngram_range=(1, 3))
        training = self.get_tweets(r'C:\Users\Mohammed\PycharmProjects\new_GP\Classifiers\train_data.xlsx')
        train_data = self.data_clean.prepare_data_list(training)
        vectorizer.fit_transform(train_data)
        return vectorizer




    def predict(self,tweets, filename,NameOfAlgo):

        classifier = self.load_classifier_dev(NameOfAlgo)
        clean_tweets = self.data_clean.prepare_data_list(list(tweets))
        vectorizer = self.put_word_features()
        tfidf = vectorizer.transform(clean_tweets)
        result = classifier.predict(tfidf)
        data_predicted = []
        for tweet, label in zip(tweets, result):
            data_predicted.append({'tweets': tweet, 'class': label})
        data_predicted = pd.DataFrame(data_predicted)
        path = os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\dev_folder\predicted', filename)
        data_predicted.to_excel(path, index=False)


    def read_file_dev(self,filename):
        try:
            path = os.path.join(r'C:\Users\Mohammed\PycharmProjects\new_GP\dev_folder',filename)
            if filename.lower().endswith(('.xlsx', '.xls')):
              dataframe = pd.read_excel(path, names=['tweets'])
            elif filename.lower().endswith(('.csv')):
                dataframe = pd.read_csv(path ,names=['tweets'])

            return dataframe
        except Exception as e:
            return False