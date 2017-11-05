# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:43:02 2017

@author: kalifou
"""

from IRmodel import IRmodel
from Weighter import TF
import numpy as np

class Okapi(IRmodel):
    """BM25 - Okapi : classical Probilistic model for Information Retrieval"""
    
    def __init__(self,index):
        """Setting the params"""
        self.k1 = np.random.uniform(1,2)
        self.b = 0.75
        self.tf = TF(index)
        self.index = index
        
        # Collecting docs length
        self.L = {}
        self.L_moy = 0.0
        for doc_id in self.index.docFrom.keys():
            self.L[doc_id] = float(self.index.docFrom[doc_id][2])
            self.L_moy += self.L[doc_id]
        self.L_moy = self.L_moy / self.tf.N # Check that the mean length is okay !!
        print 'L moy : ',self.L_moy
        
        # Calculating all probabilistic ids for all stems        
        self.idf_probabilistic = self.idf_probabilistic()
        #print 'Proba. IDFs : ',self.idf_probabilistic
        
    def idf_probabilistic(self):
        """ Probabilistic Inverse Document Frequency
            TODO : add this function to __init__() in Weighter class with a switch parameter 
                   such as probabilistic = True | False 
        """
        idf = {}
        N = self.tf.N 
        for stem in self.index.stems.keys():
            tfs = self.index.getTfsForStem(stem)
            df_t = float(len(tfs))
            r = np.log(( N - df_t + .5 ) / ( df_t + .5) )
            idf[stem] = max(0, r)
        return idf
        
    def f(self,q,d):
        """Score measuring how well Query q matches Document d"""
        score = 0.0        
        for t in q:
            num = (self.k1 + 1)*  self.tf.getDocWeightsForStem(t).get(d,0.)
            denom = self.k1 * ( (1-self.b) + self.b * self.L[d] / self.L_moy) \
                                + self.tf.getDocWeightsForStem(t).get(d,0.)
            print 'denom :',denom
            score += self.idf_probabilistic[t] * (num / denom)                                        
        return score        
    
    def getScores(self,query):
        """compute doncument's scores for a given query"""
        pass

    def getRanking(self,query):
        pass