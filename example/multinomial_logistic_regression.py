#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:04:13 2019

@author: jasonahchuen
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('jason-alouda', 'EO00dgp6GwVdqYqEriWD')
 
# Dataset Path
DATASET_PATH = "train_data_new.csv"
 
 
def scatter_with_color_dimension_graph(feature, target, layout_labels):
    """
    Scatter with color dimension graph to visualize the density of the
    Given feature with target
    :param feature:
    :param target:
    :param layout_labels:
    :return:
    """
    trace1 = go.Scatter(
        y=feature,
        mode='markers',
        marker=dict(
            size='16',
            color=target,
            colorscale='Viridis',
            showscale=True
        )
    )
    layout = go.Layout(
        title=layout_labels[2],
        xaxis=dict(title=layout_labels[0]), yaxis=dict(title=layout_labels[1]))
    data = [trace1]
    fig = Figure(data=data, layout=layout)
    # plot_url = py.plot(fig)
    py.image.save_as(fig, filename=layout_labels[1] + '_Density.png')
 
 
def create_density_graph(dataset, features_header, target_header):
    """
    Create density graph for each feature with target
    :param dataset:
    :param features_header:
    :param target_header:
    :return:
    """
    for feature_header in features_header:
        print("Creating density graph for feature:: {} ".format(feature_header))
        layout_headers = ["Number of Observation", feature_header + " & " + target_header,
                          feature_header + " & " + target_header + " Density Graph"]
        scatter_with_color_dimension_graph(dataset[feature_header], dataset[target_header], layout_headers)
 
 
if __name__ == '__main__':
    surface_data_headers = ["sd1", "sd2", "sd3", "amp", "freq", "surface"]
    surface_data = pd.read_csv(DATASET_PATH)
 
    print("Number of observations :: ", len(surface_data.index))
    print("Number of columns :: ", len(surface_data.columns))
    print("Headers :: ", surface_data.columns.values)
    print("Target ::\n", surface_data[surface_data_headers[-1]])
    

 
    train_x, test_x, train_y, test_y = train_test_split(surface_data[surface_data_headers[:-1]],
                                                        surface_data[surface_data_headers[-1]], train_size=0.7)
    
    # Train multi-classification model with logistic regression
    lr = linear_model.LogisticRegression()
    lr.fit(train_x, train_y)
 
    # Train multinomial logistic regression model
    mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)
 
    print("Logistic regression Train Accuracy :: ", metrics.accuracy_score(train_y, lr.predict(train_x)))
    print("Logistic regression Test Accuracy :: ", metrics.accuracy_score(test_y, lr.predict(test_x)))
 
    print("Multinomial Logistic regression Train Accuracy :: ", metrics.accuracy_score(train_y, mul_lr.predict(train_x)))
    print("Multinomial Logistic regression Test Accuracy :: ", metrics.accuracy_score(test_y, mul_lr.predict(test_x)))
    
    print(test_y)
    print(mul_lr.predict(test_x))
    
    # save model to disk
    filename = 'multinomial_model.sav'
    joblib.dump(mul_lr, filename)
 