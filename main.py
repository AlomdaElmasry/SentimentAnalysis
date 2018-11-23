from flask import Flask, request, render_template,flash,redirect,session,url_for,Markup
from bokeh.charts import TimeSeries ,show,output_file
from bokeh.embed import components
from User import User
from TwitterAPI import TwitterAPI
from Result import Result
from werkzeug.utils import secure_filename
from TweetClassifier import TweetClassifier
import os
from sklearn.naive_bayes import MultinomialNB ,BernoulliNB
from sklearn.svm import SVC ,LinearSVC
from sklearn.linear_model import LogisticRegression,SGDClassifier
from flask_pymongo import PyMongo
import pandas as pd
from datetime import datetime

app = Flask(__name__)

display = None

user = User()
api = TwitterAPI()
result = Result()
app.config["MONGO_DBNAME"] = 'sentipedia'
mongo = PyMongo(app)
tweet_classify = TweetClassifier()
UPLOAD_FOLDER = r'C:\Users\Mohammed\PycharmProjects\new_GP/uploads'
DEV_FOLDER = r'C:\Users\Mohammed\PycharmProjects\new_GP/dev_folder'
ALLOWED_EXTENSIONS = set(['xlsx','xls','csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEV_FOLDER'] = DEV_FOLDER


def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST'])
def login():

    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({"username": request.form['username']})
        if login_user:
            if request.form['password'].encode('utf-8') == login_user['password']:
                session['username'] = request.form['username']
                session['user_type'] = login_user['user_type']
                return render_template("index.html")
        session.clear()
        return render_template('login_error.html')



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    result.bar_chart1 = False
    result.pie_chart1 = False
    return render_template("index.html")




@app.route('/py_register', methods=['POST', 'GET'])
def py_register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            if request.form['password'] != "" and request.form['full_name'] != "" and request.form['phone'] != "" and request.form['email'] != "":
                user_type = request.form['user_type']
                username = request.form['username']
                password = request.form['password'].encode('utf-8')
                full_name = request.form['full_name']
                phone = request.form['phone']
                email = request.form['email']
                #session_value = {current_time: [{"positive": "12"}, {"negative": "21"}, {"neutral": "54"}]}
                user_session = []

                users.insert({'username': username, 'password': password, 'full_name': full_name, 'phone': phone, 'email': email, 'user_type': user_type, 'user_session': user_session})
                session['username'] = username
                session['user_type'] = user_type
                return redirect(url_for('index'))

            return 'Please fill the required Fields'

        return 'That username already exists!'
    session.clear()
    return render_template('index.html')



@app.route("/register")
def register():
      return render_template("register.html")

@app.route("/user_register")
def user_register():
      return render_template("user_register.html")




@app.route("/test_algo_dev/<algorithm>")
def test_algo_dev(algorithm):

    return render_template("dev_historical.html" ,algorithm = algorithm)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
        global display
        display = True
        if request.method == 'POST':
            # check if the post request has the file part
            file = request.files['file']

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return render_template('file_empty.html')
            if file and allowed_file(file.filename) and 'username' in session:
                filename = secure_filename(file.filename)
                new_fn = session['username']+'_'+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_fn))
                file = user.upload(new_fn)
                if(file):
                    dataframe = user.file
                    result.report(dataframe)
                    bar=result.bar_chart()
                    pie= result.pie_chart()
                    bar_words = result.bar_chart_most_words()
                    pie_words = result.pie_chart_most_words()
                    time = time_series()
                    if time:
                     return render_template('result.html', result1=result, bar=bar, pie=pie,bar_words=bar_words, pie_words=pie_words ,time=time, display=True)
                    else:
                        return render_template('result.html', result1=result, bar=bar, pie=pie, bar_words=bar_words,
                                               pie_words=pie_words, time=False, display=True)
                else:
                    return render_template('file_type_error.html')
            return render_template('500.html')
        return render_template('500.html')


@app.route('/dev_test',methods = ['POST','GET'])

def dev_test():
    try:
         global display
         display = True
         if request.method == 'POST':
            alogrithm = request.form.get('algorithm')
            file = request.files['file']
            if file.filename =='':
                flash('No selected file')
                return render_template('file_empty.html')
            if file and allowed_file(file.filename) and 'username' in session:
                filename = secure_filename(file.filename)
                filename1 = session['username']+'_'+filename
                file.save(os.path.join(app.config['DEV_FOLDER'], filename1))
                NameOfAlgo = session['username']+'_'+alogrithm
                dataframe = tweet_classify.read_file_dev(filename1)
                tweet_classify.predict(list(dataframe['tweets']) ,filename1 ,NameOfAlgo)
                predicted_file = r"C:\Users\Mohammed\PycharmProjects\new_GP\dev_folder\predicted/"+filename1
                dataframe = pd.read_excel(predicted_file ,names =['class','tweets'])
                result.report(dataframe)
                bar = result.bar_chart()
                pie = result.pie_chart()
                bar_words = result.bar_chart_most_words()
                pie_words = result.pie_chart_most_words()


                time = time_series()

            return render_template('result.html', result1=result, bar=bar, pie=pie, bar_words=bar_words,pie_words=pie_words ,time =time, display=display)
    except Exception as e:
         return render_template("file_type_error.html",error = e)











@app.route('/upload_dev', methods=['GET','POST'])
def upload_dev():
     # try:
         if request.method == 'POST':
             # check if the post request has the file part
             train_file = request.files['train_file']
             test_file = request.files['test_file']
             # if user does not select file, browser also
             # submit a empty part without filename
             if train_file.filename == '' and test_file.filename == '':
                 flash('No selected file')
                 return render_template("file_empty.html")
             if train_file and allowed_file(train_file.filename) and test_file and allowed_file(test_file.filename) and 'username' in session:
                 train_filename = secure_filename(train_file.filename)
                 test_filename = secure_filename(test_file.filename)
                 new_train_fn = session['username']+'_'+ train_filename
                 new_test_fn = session['username']+'_'+ test_filename
                 train_file.save(os.path.join(app.config['DEV_FOLDER'], new_train_fn))
                 test_file.save(os.path.join(app.config['DEV_FOLDER'], new_test_fn))
                 algo_list = ["MultinomialNB", "BernoulliNB", "SVC", 'LinearSVC', "LogisticRegression", "SGDClassifier"]
                 algo_dic = {"MultinomialNB": None, "BernoulliNB": None, "SVC": None, 'LinearSVC': None,
                             "LogisticRegression": None, "SGDClassifier": None}
                 for counter, checkbox in enumerate(algo_list):
                     algo = request.form.get(checkbox)
                     algo_dic[algo_list[counter]] = algo
                     lista = []
                     lista2 = []
                 for k, v in algo_dic.items():
                     if v != None:
                         if k == 'MultinomialNB':
                             name = session['username']+'_'+'MultinomialNB'
                             result = user.accuracy(new_train_fn, new_test_fn, MultinomialNB(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')
                         if k == 'BernoulliNB':
                             name = session['username'] + '_' + 'BernoulliNB'
                             result = user.accuracy(new_train_fn, new_test_fn, BernoulliNB(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')
                         if k == 'SVC':
                             name = session['username'] + '_' + 'SVC'
                             result = user.accuracy(new_train_fn, new_test_fn, SVC(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')
                         if k == 'LinearSVC':
                             name = session['username'] + '_' + 'LinearSVC'
                             result = user.accuracy(new_train_fn, new_test_fn, LinearSVC(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')
                         if k == 'LogisticRegression':
                             name = session['username'] + '_' + 'LogisticRegression'
                             result = user.accuracy(new_train_fn, new_test_fn, LogisticRegression(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')
                         if k == 'SGDClassifier':
                             name = session['username'] + '_' + 'SGDClassifier'
                             result = user.accuracy(new_train_fn, new_test_fn, SGDClassifier(),name)
                             if result ==False:
                                 return render_template('file_type_error_dev.html')

                         lista.append(result)
                         lista2.append(k)
                 if len(lista)==0 or len(lista2)==0:
                     return render_template('error_algo.html')




                 return render_template("dev_result.html", lista=lista, lista2=lista2)
             else:
                 return render_template("file_empty.html")
         else:
             return render_template("500.html")
     # except Exception as e:
     #      return render_template("500.html",error = e)






@app.route('/upload_dev_data')
def upload_dev_data():
     return render_template("upload_dev_data.html")




@app.route('/search' ,methods = ["POST" ,"GET"] )
def search():
    try:
         text = request.form['word']
         if text == '' :
             return render_template("error_word.html")
         tweets = user.search(text)
         if tweets:
             api.classify_real_time(tweets ,text+'.xlsx')
             dataframe = api.read_real_time(text+'.xlsx')
             result.report(dataframe)
             bar = result.bar_chart()
             pie = result.pie_chart()
             bar_words = result.bar_chart_most_words()
             pie_words = result.pie_chart_most_words()
             time = time_series()
             if time:
               return render_template("result.html" ,result1 = result,bar = bar ,pie =pie, bar_words=bar_words,pie_words=pie_words,time =time)
             else:
               return render_template("result.html", result1=result, bar=bar, pie=pie, bar_words=bar_words, pie_words=pie_words, time = False)
         else:
             return render_template('error_search.html')
    except Exception as e:
        return render_template("error_search.html", error=e)


@app.route('/dashboard')
def dashboard():
   try:
        if result.bar_chart1 and result.pie_chart1 and 'username' in session :
            try:
                bar = result.bar_chart()
                pie = result.pie_chart()
                bar_words = result.bar_chart_most_words()
                pie_words = result.pie_chart_most_words()
                time = time_series()
                return render_template("result.html" ,result1 = result,bar = bar ,pie =pie, bar_words=bar_words,pie_words=pie_words,time =time, display=display)
            except Exception as e:
                return render_template("500.html", error=e)

        else:
            return render_template("error_file.html")
   except Exception as e:
          return render_template("500.html", error=e)


@app.route('/table' )
def table():
    if result.bar_chart1 and result.pie_chart1 and 'username' in session:
        try:
            bar = result.bar_chart()
            pie = result.pie_chart()
            pie_words = result.pie_chart_most_words()
            bar_words = result.bar_chart_most_words()
            time = time_series()
            return render_template("table.html", result1=result, bar=bar, pie=pie, bar_words=bar_words,pie_words=pie_words,time=time)
        except Exception as e:
            return render_template("500.html", error=e)

    else:
        return render_template("error_file.html")

@app.route('/')
@app.route('/index')
def index():
    # try:

        return render_template("index.html")
    # except Exception as e:
    #     return render_template("500.html", error=e)

@app.route('/sport_home')
def sport_home():
    try:
       return render_template("sport_home.html")
    except Exception as e:
        return render_template("500.html", error=e)

@app.route('/telecom_home')
def telecom_home():
    try:
     return render_template("telecom_home.html")
    except Exception as e:
        return render_template("500.html", error=e)

@app.route('/sport_historical')
def sport_historical():
    try:
       return render_template("sport_historical.html")
    except Exception as e:
        return render_template("500.html", error=e)

@app.route('/sport_realtime')
def sport_realtime():
    try:
      return render_template("sport_realtime.html")
    except Exception as e:
        return render_template("500.html", error=e)

@app.route('/telecom_historical')
def telecom_historical():
    try:
       return render_template("telecom_historical.html")
    except Exception as e:
        return render_template("500.html", error=e)

@app.route('/telecom_realtime')
def telecom_realtime():
    try:
       return render_template("telecom_realtime.html")
    except Exception as e:
        return render_template("500.html", error=e)


@app.route('/about_us')
def about_us():
    try:
       return render_template("about_us.html")
    except Exception as e:
        return render_template("500.html", error=e)


@app.route('/contact_us')
def contact_us():
    # try:

      return render_template("contact_us.html")
    # except Exception as e:
    #     return render_template("500.html", error=e)

@app.route('/time_series')
def time_series():
    try:
        if 'username' in session:
            users = mongo.db.users
            existing_user = users.find_one({"username": session["username"]})

            if existing_user :
                object =users.find_one({"username" : session["username"]})
                user_session= object["user_session"]
                neu =[]
                pos =[]
                neg =[]
                time =[]
                data ={}
                for dic in user_session:
                    for k , v in dic.items():
                        if k != 'Algorithm':
                            time.append(k)
                            for k1 ,v1 in v[0].items():
                                if k1=="neutral":
                                    neu.append(float(v1))
                                elif k1=='negative':
                                    neg.append(float(v1))
                                else:
                                    pos.append(float(v1))
                            data.update(Date=time,Neutral=neu ,Positive =pos ,Negative = neg)
                dataframe=pd.DataFrame(data)


                # output_file("timeseries.html")

                p = TimeSeries(dataframe, x='Date', y = ['Neutral' ,'Negative' ,'Positive'], color =['Neutral' ,'Negative' ,'Positive'] ,dash=['Neutral', 'Negative' ,'Positive'] ,title="User History", ylabel='Classes')
                script_p, div_p = components(p)
                script_p = Markup(script_p)
                div_p = Markup(div_p)
                page = [script_p, div_p]
                return page
    except Exception as e:
        return False



@app.route('/save_result', methods=['POST'])
def save_result():
    global display
    display = False
    positive_num = request.form['positive']
    negative_num = request.form['negative']
    neutral_num = request.form['neutral']

    users = mongo.db.users
    existing_user = users.find_one({'username': session['username']})

    if existing_user:
        user_session = existing_user['user_session']
        username = existing_user['username']
        password = existing_user['password']
        full_name = existing_user['full_name']
        phone = existing_user['phone']
        email = existing_user['email']
        user_type = existing_user['user_type']
        current_time = datetime.now().strftime("%Y/%m/%d")
        session_value = {current_time: [{"positive": str(positive_num), "negative": str(negative_num),
                                         "neutral": str(neutral_num)}], 'Algorithm': "MultinomialNB"}

        user_session.append(session_value)

        users.update(
            {"username": username},
            {"username": username, "password": password, "full_name": full_name, "phone": phone,
             "email": email, "user_type": user_type, "user_session": user_session})

        bar = result.bar_chart()
        pie = result.pie_chart()
        bar_words = result.bar_chart_most_words()
        pie_words = result.pie_chart_most_words()
        time = time_series()
        if time:
         return render_template("result.html", result1=result, bar=bar, pie=pie, bar_words=bar_words,
                               pie_words=pie_words, time=time, display=display)
        else:
            return render_template("result.html", result1=result, bar=bar, pie=pie, bar_words=bar_words,
                                   pie_words=pie_words, time=False, display=display)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()