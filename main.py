from flask import Flask, request, render_template, flash, session, redirect, url_for
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
app = Flask(__name__,template_folder='template')
import os
@app.route('/', methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('dashboard.html')


@app.route('/dashboard',methods=['GET','POST'])
def CheckCredentials():
    if request.form['username'] != 'admin' or \
        request.form['password'] != 'admin':
        error = 'Invalid username or password. Please try again!'
    else:
        flash('You were successfully logged in')
        return render_template('dashboard.html', name = "John Doe")
    return render_template('login.html', error = error)

@app.route('/login', methods=['GET','POST'])
def Login():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/registration', methods=['GET','POST'])
def registration():
    if len(request.form) < 2:
        error = 'Name too short'
        return render_template('register.html',error=error)
    if request.form['password'] != request.form['confirmpassword']:
        error = 'Passwords do not match'
        return render_template('register.html',error=error)
    error = 'Registration Successful! Please Login'    
    return render_template('register.html',error=error)


@app.route('/process')
def process():
    dfT= pd.read_csv('https://www.quandl.com/api/v3/datasets/NSE/'+request.args.get('sym')+'.csv?api_key=17qo2ogx-1KC1jEoox8d')
    prices = dfT['Close'].values.astype('float32')
    model = Sequential()   
    trainX, trainY, testX, testY=testandtrain(prices)
    model = trainingmodel(model, trainX, trainY)
    predictingY=predicting(prices,testX,testY,trainX,model)
    result=''
    if predictingY[0][0]<predictingY[3][0]:
        result='profit'
    else:
        result='loss'
    return render_template('predict.html',plot='plot.jpg',res=result)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)    