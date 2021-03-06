# -*- coding: utf-8 -*-
"""Naive Bayes and Bayesian Inference.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1paTFnIXqT7a8NyPmcmHiq9jNVafsKetm

## Import libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")
from scipy.stats import multivariate_normal as mvn

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings('ignore')
# %config InlineBackend.figure_format = 'svg'

"""## Import trainning and tes



"""

data_train=pd.read_csv("/content/drive/MyDrive/Enhance it/Cesar Perez - MNIST_train.csv")

data_test=pd.read_csv("/content/drive/MyDrive/Enhance it/Cesar Perez - MNIST_test.csv")

X_train=data_train.iloc[:,3:]
y_train=data_train.iloc[:,2]

X_test=data_test.iloc[:,3:]
y_test=data_test.iloc[:,2]

class GaussNB():
  def fit(self, X, y, epsilon=1e-3):
    self.likelihoods = dict()
    self.priors=dict()

    self.K=set(y.astype(int))

    for k in self.K:
      X_k=X[y==k, :]
      self.likelihoods[k]={"mean":X_k.mean(axis=0), "cov":X_k.var(axis=0)+epsilon}
      self.priors[k]=len(X_k)/len(X)

  def predict(self,X):

    N,D=X.shape
    P_hat=np.zeros((N, len(self.K)))

    for k, l in self.likelihoods.items():
      P_hat[:,k]=mvn.logpdf(X, l['mean'], l["cov"])+np.log(self.priors[k])

    return P_hat.argmax(axis=1)

class GaussBayes():
  def fit(self, X, y, epsilon=1e-3):
  
    self.likelihoods=dict()
    self.priors=dict()
    self.K=set(y.astype(int))

    for k in self.K:

      X_k=X[y==k,:]
      N_k, D=X_k.shape
      mu_k=X_k.mean(axis=0)

      self.likelihoods[k]={'mean':X_k.mean(axis=0),'cov':(1/(N_k-1))*np.matmul((X_k-mu_k).T, X_k-mu_k)+epsilon*np.identity(D)}
      self.priors[k]=len(X_k)/len(X)
  
  def predict(self,X):

    N,D=X.shape
    P_hat=np.zeros((N, len(self.K)))

    for k, l in self.likelihoods.items():
      P_hat[:,k]=mvn.logpdf(X, l['mean'], l["cov"])+np.log(self.priors[k])
    
    return P_hat.argmax(axis=1)

def accuracy(y, y_hat):
  return np.mean(y==y_hat)

gauss=GaussBayes()

gauss.fit((X_train/255).to_numpy(), y_train.to_numpy())

y_hat=gauss.predict(X_test.to_numpy())

accuracy( y_test.to_numpy(), y_hat)

y_hat=pd.DataFrame(y_hat, columns=["y_hat"])

y_test=pd.DataFrame(y_test)

confusion_matrix=pd.concat([y_hat,y_test], axis=1)

confusion_matrix

y=[]
for j in range(10):
  x=[]
  for i in range(10):
    a=confusion_matrix[(confusion_matrix["y_hat"]==j)
    &(confusion_matrix["labels"]==i)].shape[0]
    x.append(a)
  y.append(x)
y

confusion_matrix[(confusion_matrix["y_hat"]==0)&(confusion_matrix["labels"]==0)]

confusion_matrix=pd.DataFrame(y)

import seaborn as sn
sn.heatmap(confusion_matrix, annot=True, cmap="YlGnBu", fmt="d");



