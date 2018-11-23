import matplotlib.pyplot as plt ; plt.rcdefaults()
import pandas as pd
from DataCleaner import DataCleaner
from collections import Counter
from bokeh.charts import Bar,Donut,TimeSeries
from bokeh.embed import components
from flask import Markup



class Result:
    bar_chart1 = False
    pie_chart1 = False
    all = []
    tweets_num = 0
    positive_tweets_num = 0
    negative_tweets_num = 0
    neutral_tweets_num = 0
    most_words = []
    dataclean = DataCleaner()
    def __init__(self):

        return



    def report(self,dataframe):

        dataframe_class ,dataframe_tweets = dataframe['class'] ,dataframe['tweets']

        dataframe_value_count = dataframe_class.value_counts()

        dictionary = dict(zip(dataframe_value_count.index, dataframe_value_count.values))

        for key,value in dictionary.items():
            if key == "neg":
                self.negative_tweets_num = value
            elif key == "pos":
                self.positive_tweets_num = value
            else:
                self.neutral_tweets_num = value

        self.tweets_num = dataframe_class.count()
        dataframe_tweets = self.dataclean.prepare_data_set_without_stem(list(dataframe_tweets))
        self.most_words = Counter(dataframe_tweets).most_common(15)
        self.all = dataframe_tweets
        self.pie_chart1 = True
        self.bar_chart1 = True
        valuable_words = pd.read_excel(r'C:\Users\Mohammed\PycharmProjects\new_GP\Classifiers\words.xlsx')
        valuable_words = valuable_words.Term
        most = []
        # for word in words :
        #     if word in list(valuable_words):
        #         most.append(word)
        # print(most)
        # print(self.all)

        for word in self.all:
            if word in list(valuable_words):
                most.append(word)
        self.most_words = Counter(most).most_common(15)
        return  dataframe_value_count


    def pie_chart(self):

       data = {'Class':['Negative','Positive','Neutral'],
                'Numbers':[self.negative_tweets_num ,self.positive_tweets_num , self.neutral_tweets_num]}


       dataframe = pd.DataFrame(data)
       pie = Donut(dataframe, 'Class', values='Numbers', title="Pie Chart For Tweets" ,color=['#75D9EF', '#4B96D8', '#33D59F'])

       script_pie, div_pie = components(pie)
       script_pie = Markup(script_pie)
       div_pie = Markup(div_pie)
       page = [script_pie, div_pie]


       return page

    def pie_chart_most_words(self):

        most_words = pd.DataFrame(sorted(self.most_words), columns=['Word', 'Freq'])
        # words =list(most_words.Word)
        # words = self.dataclean.remove_stops(words)

        pie = Donut(most_words,'Word', values='Freq' ,title="Pie Chart For Tweets",
                    color=['#f20f32', '#39f20f', '#76dfe7','#af0132', '#f39f29', '#3FC0CF','#75D9EF', '#4B96D8', '#33D59F','#33A9D5', '#94A2F3', '#687EFC','#68FCCF', '#68FCEC', '#75D3F9'])

        script_pie, div_pie = components(pie)
        script_pie = Markup(script_pie)
        div_pie = Markup(div_pie)
        page = [script_pie, div_pie]
        return page





    def bar_chart(self):

       data = {'Class':['Negative','Positive','Neutral'],
                'Numbers':[self.negative_tweets_num ,self.positive_tweets_num , self.neutral_tweets_num]}
       dataframe = pd.DataFrame(data)
       bar = Bar(dataframe, 'Class', values='Numbers', title="Bar Chart For Tweets",legend='top_right', agg='median',color="#33A9D5")

       script, div = components(bar)
       script = Markup(script)
       div = Markup(div)
       page = [script, div]


       return page


    def bar_chart_most_words(self):

        most_words = pd.DataFrame(self.most_words ,columns=['Words' , "Freq"])
        bar = Bar(most_words ,"Words",values="Freq" ,title="Bar Chart For Tweets", legend='top_right', agg='median',color=["#75D3F9","#75F9F7","#75D9F9"])

        script, div = components(bar)
        script = Markup(script)
        div = Markup(div)
        page = [script, div]
        return page










