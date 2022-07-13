import pandas as pd
import numpy as np
import pickle
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
import os
df=pd.read_csv('jad.csv')
lr=LogisticRegression()
from sklearn.model_selection import train_test_split
train,test=train_test_split(df,test_size=0.2)
col=df.shape[1]
train_feat=train.iloc[:,:(col-1)]
train_targ=train["res"]
lr.max_iter=200
lr.fit(train_feat,train_targ)
pickle.dump(lr, open("m1.py", 'wb'))
