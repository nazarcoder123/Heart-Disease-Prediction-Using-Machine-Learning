# -*- coding: utf-8 -*-
"""heart-diesease-prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rJ8xcluJGDcx2ryg86UfV0Mo0689B9Yx
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("/kaggle/input/cardiovascular-diseases-risk-prediction-dataset/CVD_cleaned.csv")

df.shape

df.head()

le = LabelEncoder()
df["Heart_Disease"] = le.fit_transform(df["Heart_Disease"])

df.columns

df["General_Health"].unique()

oe = OrdinalEncoder(categories=[["Poor","Very Good","Good","Fair","Excellent"]])

df["General_Health"] = oe.fit_transform(df["General_Health"].values.reshape(-1,1))

df["Checkup"].unique()

oe = OrdinalEncoder(categories=[['Within the past 2 years', 'Within the past year',
       '5 or more years ago', 'Within the past 5 years', 'Never']])

df["Checkup"] = oe.fit_transform(df["Checkup"].values.reshape(-1,1))

df["Exercise"].unique()

le = LabelEncoder()
df["Exercise"] = le.fit_transform(df["Exercise"])

df["Heart_Disease"].unique()

df["Skin_Cancer"].unique()

le = LabelEncoder()
df["Skin_Cancer"] = le.fit_transform(df["Skin_Cancer"])

df["Other_Cancer"].unique()

le = LabelEncoder()
df["Other_Cancer"] = le.fit_transform(df["Other_Cancer"])

df["Depression"].unique()

le = LabelEncoder()
df["Depression"] = le.fit_transform(df["Depression"])

df["Diabetes"].unique()

oe = OrdinalEncoder(categories="auto")
df["Diabetes"] = oe.fit_transform(df["Diabetes"].values.reshape(-1,1))

df["Arthritis"].unique()

le = LabelEncoder()
df["Arthritis"] = le.fit_transform(df["Arthritis"])

df.columns

df["Sex"].unique()

le = LabelEncoder()
df["Sex"] = le.fit_transform(df["Sex"])

df["Age_Category"].unique()

df["Smoking_History"].unique()

le = LabelEncoder()
df["Smoking_History"] = le.fit_transform(df["Smoking_History"])

oe = OrdinalEncoder()
df["Age_Category"] = oe.fit_transform(df["Age_Category"].values.reshape(-1,1))

"""## lets declare x and y"""

x = df.drop(columns="Heart_Disease")
y = df["Heart_Disease"]

from sklearn.model_selection import train_test_split,cross_val_score

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

from sklearn.preprocessing import Normalizer

n = Normalizer()

x_train_n = n.fit_transform(x_train)
x_test_n = n.transform(x_test)

sns.distplot(x_train_n)

from sklearn.preprocessing import PowerTransformer,FunctionTransformer

pt = FunctionTransformer(func=np.log1p)

x_train_pt = pt.fit_transform(x_train_n)
x_test_pt = pt.transform(x_test_n)

sns.distplot(x_train_pt)

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()

lr.fit(x_train_pt,y_train)

y_pred = lr.predict(x_test_pt)

from sklearn.metrics import accuracy_score

accuracy_score(y_pred,y_test)

cross_val_score(lr,x_train_n,y_train).mean()

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(max_depth=100)

dt.fit(x_train_n,y_train)

y_pred1 = dt.predict(x_test_n)

accuracy_score(y_pred1,y_test)

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()

rf.fit(x_train_n,y_train)

y_pred2 = rf.predict(x_test_n)

accuracy_score(y_pred2,y_test)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()

knn.fit(x_train_n,y_train)

y_pred_3 = knn.predict(x_test_n)

accuracy_score(y_pred_3,y_test)

from sklearn.svm import SVC

s = SVC()

s.fit(x_train_n,y_train)

y_pred_4 = s.predict(x_test_n)

accuracy_score(y_pred_4,y_test)

from sklearn.ensemble import VotingClassifier

lr_classifier = LogisticRegression()
dt_classifier = DecisionTreeClassifier()
rf_classifier = RandomForestClassifier()
knn_classifier = KNeighborsClassifier()
svc_classifier = SVC()

vc = VotingClassifier(estimators=[("lr",LogisticRegression),("dt",DecisionTreeClassifier),("rf",RandomForestClassifier),("knn",KNeighborsClassifier),("s",SVC)],voting="hard")

# Create the Voting Classifier
vc = VotingClassifier(estimators=[
    ("lr", lr_classifier),
    ("dt", dt_classifier),
    ("rf", rf_classifier),
    ("knn", knn_classifier),
    ("s", svc_classifier)
], voting="hard")

# Fit the Voting Classifier to the training data
vc.fit(x_train_n, y_train)

n_pred = vc.predict(x_test_n)

accuracy_score(n_pred,y_test)