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
import random, string


def create_dataset(dataset,past=5): # relating 5th day and 1st day
    dataX, dataY = [], []
    for i in range(len(dataset)-past-1):
        j = dataset[i:(i+past), 0]
        dataX.append(j)
        dataY.append(dataset[i + past, 0])
    return np.array(dataX), np.array(dataY)

from sklearn.preprocessing import MinMaxScaler
def testandtrain(prices):
    prices = prices.reshape(len(prices), 1)
    prices.shape
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = scaler.fit_transform(prices)
    trainsize = int(len(prices)*0.80)
    testsize = len(prices) - trainsize
    train, test = prices[0:trainsize,:], prices[trainsize:len(prices),:]
    print(len(train), len(test))
    x_train,y_train = create_dataset(train,1)
    x_test,y_test = create_dataset(test,1)
    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
    return x_train,y_train, x_test,y_test


def trainingmodel(model, trainX, trainY):
    model = Sequential()
    model.add(LSTM(5, input_shape=(1,1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='rmsprop')
    model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
    return model


from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler


from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

def predicting(prices,testX,testY,trainX,model):
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = prices.reshape(len(prices), 1)
    prices.shape
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = scaler.fit_transform(prices)
    testPredict = model.predict(testX)
    error = math.sqrt(mean_squared_error(testY, testPredict))
    print('Test RMSE: %.3f' % error)
    plt.figure()
    plt.plot(testPredict,color="blue")
    x = 'p'.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)).join('.jpg')
    plt.savefig('static/'+x)
    return testPredict,x