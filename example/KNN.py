#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 02:53:23 2019

@author: jasonahchuen
"""

# Import LabelEncoder
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.externals import joblib

fields = ['sd1', 'sd2', 'sd3', 'amp', 'freq','surface']
data = pd.read_csv("train_data_new.csv", skipinitialspace = True, usecols = fields)

# Assigning features and label variables


# First Feature

std1 = data.sd1

# Second Feature

std2 = data.sd2

# Third Feature

std3 = data.sd3

# Fourth feature and fifth feature from fourier graph

amp = data.amp
freq = data.freq

# target variable
surface = data.surface
# Creating label encoder
le = preprocessing.LabelEncoder()
# Converting string labels into numbers.
#std_encoded = le.fit_transform(std)
#amp_encoded = le.fit_transform(amp)
surface = le.fit_transform(surface)

# Combine std and amp into single list of tuples
features=list(zip(std1,std2,std3,amp, freq))

# Build KNN classifier model
model = KNeighborsClassifier(n_neighbors=2)

# Train the model using the training sets
model.fit(features,surface)

# Printing out how accurate the model is
#print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

#Predict Output for one set
#predicted= model.predict([[8.5, 0, 5.6, 2441, 0.188]])
#print(predicted)

#Testing accuracy
surface_data_headers = ["sd1", "sd2", "sd3", "amp", "freq", "surface"]
surface_data = pd.read_csv("train_data_new.csv")
train_x, test_x, train_y, test_y = train_test_split(surface_data[surface_data_headers[:-1]],
                                                    surface_data[surface_data_headers[-1]], train_size=0)

#from sklearn.model_selection import GridSearchCV
#from sklearn import neighbors
#params = {'n_neighbors':[2,3,4,5,6,7,8,9]}
#knn = neighbors.KNeighborsRegressor()
#model = GridSearchCV(knn, params, cv=2)
#model.fit(train_x,train_y)
#model.best_params_


y_pred = model.predict(test_x)
print(y_pred)
test_y_encoded = le.fit_transform(test_y)
print(test_y_encoded)
print("KNN Test Accuracy :: ", metrics.accuracy_score(test_y_encoded, y_pred))
# save model to disk
filename = 'KNN_model.sav'
joblib.dump(model, filename)