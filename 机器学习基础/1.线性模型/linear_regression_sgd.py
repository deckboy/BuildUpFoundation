# -*- coding: utf-8 -*-
"""
@author: CJM
"""

import numpy as np

class LinearRegSGD():
    
    def __init__(self):
        self.coef_ = None;
        self.intercept_ = 0;
        
    def gradW(self, X, y, W):
        """grad = X.T*(X*W-y)"""
        return X.T.dot(X.dot(W)-y)
        
    def fit(self, X, y, lr=0.01, maxIter=100):
        """ linear regression with SGD
        """
        # data process: w*X+b ==> w_*X_temp, that is w_ = [w,b], X_temp=[X,1]
        num_x = np.shape(X)[0]
        X_temp = np.concatenate((X, np.ones((num_x, 1))), axis=1)
        W_temp = np.random.randn(X_temp.shape[1]) # zero initialization?
        ## XTX checks is necessary ?
        # Stochastic gradient descent
        for _ in range(maxIter):
            for xx,yy in zip(X_temp,y):
                W_temp -= lr*self.gradW(xx, yy, W_temp)
        self.coef_ = W_temp[:-1]
        self.intercept_ = W_temp[-1]
        
    def predict(self, X):
        if self.coef_ is None:
            print('error: the model had not been trained')
            return #should raise the expection
        return self.coef_.dot(X.T) + self.intercept_