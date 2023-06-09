# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:48:44 2022

@author: Harry McNinson
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score
from sklearn.preprocessing import LabelBinarizer,StandardScaler,OrdinalEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from scipy.stats import boxcox
from sklearn.linear_model import LogisticRegression,RidgeClassifier, PassiveAggressiveClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import plot_importance
from matplotlib import pyplot
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
import joblib
from fancyimpute import KNN, SoftImpute
import operator

import six
import sys
sys.modules['sklearn.externals.six'] = six
import sklearn.neighbors._base
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from sklearn.utils import _safe_indexing
sys.modules['sklearn.utils.safe_indexing'] = sklearn.utils._safe_indexing
from imblearn.over_sampling import SMOTE


test = pd.read_csv('data/test_data.csv')

cat_cols = ['Term','Years in current job','Home Ownership','Purpose']

for c in cat_cols:
    test[c] = pd.factorize(test[c])[0]
    
    
#Imputing missing data with soft impute
updated_test_data=pd.DataFrame(data=SoftImpute().fit_transform(test[test.columns[3:19]],), columns=test[test.columns[3:19]].columns, index=test.index)

#Getting the dataset ready pd.get dummies function for dropping the dummy variables
test_data = pd.get_dummies(updated_test_data, drop_first=True)

gbm_pickle = joblib.load('model/GBM_Model_version1.pkl')

y_pred = gbm_pickle.predict(test_data)
y_pred = gbm_pickle.predict_proba(test_data)

y_pred_1=np.where(y_pred ==0, 'Loan Approved', 'Loan Rejected')

test['Loan Status']=y_pred_1

test.to_csv('Output_Test.csv',index=False)

y_pred_1
