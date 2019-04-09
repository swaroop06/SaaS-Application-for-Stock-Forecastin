from flask import Flask, request, render_template, flash, session, redirect, url_for,g
from functions import *
import pandas as pd
from keras.models import Sequential
import numpy as np
import scipy as sp
import pandas as pd
from subprocess import check_output
import time, json
from datetime import date
import time
import math
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
import numpy as np
import pandas as pd
import sklearn.preprocessing as prep
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import sqlite3

app = Flask(__name__,template_folder='template')
import os

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
    return db

@app.route('/', methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('dashboard.html')


@app.route('/dashboard',methods=['GET','POST'])
def CheckCredentials():
    return render_template('dashboard.html', name = session['username'])

@app.route('/login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        con = get_db()
        user = con.execute('SELECT * FROM users where email = ? and password = ?',(email,password)).fetchone()
        if user is not None:
            session['login'] = True
            session['username'] = user[0]
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/registration', methods=['POST'])
def registration():
    con = get_db()
    if len(request.form) < 2:
        error = 'Name too short'
        return render_template('register.html',error=error)
    if request.form['password'] != request.form['confirmpassword']:
        error = 'Passwords do not match'
        return render_template('register.html',error=error)
    try:
        name = request.form['name']
        email = request.form['email'].lower()
        password = request.form['password']
        phone = request.form['phone']
        age = request.form['age']
        cur = con.cursor()
        cur.execute("INSERT INTO users (name,email,password,phone,age) VALUES (?,?,?,?,?)",(name,email,password,phone,age)) 
        con.commit()
        print("Record successfully added")
        return redirect('/login')
    except:
        con.rollback()
        print("error in insert operation")
        return redirect('/register')

@app.route('/process')
def process():
    dfT= pd.read_csv('https://www.quandl.com/api/v3/datasets/NSE/'+request.args.get('sym')+'.csv?api_key=17qo2ogx-1KC1jEoox8d')
    prices = dfT['Close'].values.astype('float32')
    model = Sequential()   
    trainX, trainY, testX, testY=testandtrain(prices)
    model = trainingmodel(model, trainX, trainY)
    predictingY,graph=predicting(prices,testX,testY,trainX,model)
    result=''
    if predictingY[0][0]<predictingY[3][0]:
        result='profit'
    else:
        result='loss'
    if predictingY[len(predictingY)-1][0]<predictingY[0][0]:
        longResult='loss'
    else:
        longResult='profit'
    return render_template('predict.html',plot=graph+'.png',res=result, longRes=longResult)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)    


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()